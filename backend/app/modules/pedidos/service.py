from datetime import datetime, timezone
from decimal import Decimal

from fastapi import HTTPException
from sqlmodel import select

from app.models import DetallePedido, Pedido, Producto, Usuario
from app.modules.pedidos.schemas import OrderCreate, OrderPage, OrderRead, OrderSummary, OrderStateChange
from app.modules.pedidos.unit_of_work import OrderUnitOfWork


TRANSITIONS = {
    "PENDIENTE": {"EN_PREPARACION", "CANCELADO"},
    "EN_PREPARACION": {"ENTREGADO", "CANCELADO"},
    "ENTREGADO": set(),
    "CANCELADO": set(),
}


def order_read(order: Pedido) -> OrderRead:
    return OrderRead(
        id=order.id,
        usuario_id=order.usuario_id,
        estado=order.estado,
        forma_pago=order.forma_pago,
        direccion_entrega=order.direccion_entrega,
        notas=order.notas,
        total=order.total,
        created_at=order.created_at,
        updated_at=order.updated_at,
        items=[
            {
                "producto_id": item.producto_id,
                "nombre_producto": item.nombre_producto,
                "precio_unitario": item.precio_unitario,
                "cantidad": item.cantidad,
                "subtotal": item.subtotal,
            }
            for item in order.items
        ],
    )


class OrderService:
    def __init__(self, uow: type[OrderUnitOfWork] = OrderUnitOfWork):
        self.uow = uow

    def create(self, user: Usuario, data: OrderCreate) -> OrderRead:
        product_ids = [item.producto_id for item in data.items]
        if len(product_ids) != len(set(product_ids)):
            raise HTTPException(409, "A product cannot be repeated in an order")
        with self.uow() as uow:
            order = Pedido(
                usuario_id=user.id,
                forma_pago=data.forma_pago,
                direccion_entrega=data.direccion_entrega,
                notas=data.notas,
            )
            uow.session.add(order)
            uow.session.flush()
            total = Decimal("0.00")
            for requested in data.items:
                product = uow.products.get_by_id(requested.producto_id)
                if product is None or not product.activo:
                    raise HTTPException(404, "Product not found")
                if not product.disponible:
                    raise HTTPException(409, "Product is not available")
                if product.stock < requested.cantidad:
                    raise HTTPException(409, "Insufficient stock")
                product.stock -= requested.cantidad
                subtotal = product.precio_base * requested.cantidad
                uow.session.add(DetallePedido(
                    pedido_id=order.id,
                    producto_id=product.id,
                    cantidad=requested.cantidad,
                    nombre_producto=product.nombre,
                    precio_unitario=product.precio_base,
                    subtotal=subtotal,
                ))
                total += subtotal
            order.total = total
            uow.session.flush()
            uow.session.refresh(order)
            return order_read(order)

    def list(self, user: Usuario, skip: int, limit: int, state: str | None) -> OrderPage:
        if state is not None and state not in TRANSITIONS:
            raise HTTPException(422, "Invalid order state")
        with self.uow() as uow:
            total, rows = uow.orders.list(None if user.role == "admin" else user.id, max(skip, 0), min(limit, 100), state)
            return OrderPage(total=total, items=[order_read(row) for row in rows])

    def get(self, user: Usuario, order_id: int) -> OrderRead:
        with self.uow() as uow:
            order = uow.orders.get_by_id(order_id)
            if order is None:
                raise HTTPException(404, "Order not found")
            if user.role != "admin" and order.usuario_id != user.id:
                raise HTTPException(403, "Order belongs to another user")
            return order_read(order)

    def change_state(self, order_id: int, data: OrderStateChange) -> OrderRead:
        with self.uow() as uow:
            order = uow.orders.get_by_id(order_id)
            if order is None:
                raise HTTPException(404, "Order not found")
            if data.estado not in TRANSITIONS.get(order.estado, set()):
                raise HTTPException(409, "Invalid order state transition")
            if data.estado == "CANCELADO":
                self._restore_stock(uow, order)
            order.estado = data.estado
            order.updated_at = datetime.now(timezone.utc)
            uow.session.add(order)
            uow.session.flush()
            return order_read(order)

    def cancel(self, user: Usuario, order_id: int) -> OrderRead:
        with self.uow() as uow:
            order = uow.orders.get_by_id(order_id)
            if order is None:
                raise HTTPException(404, "Order not found")
            if user.role != "admin" and order.usuario_id != user.id:
                raise HTTPException(403, "Order belongs to another user")
            allowed_states = {"PENDIENTE", "EN_PREPARACION"} if user.role == "admin" else {"PENDIENTE"}
            if order.estado not in allowed_states:
                raise HTTPException(409, "Order cannot be cancelled from its current state")
            self._restore_stock(uow, order)
            order.estado = "CANCELADO"
            order.updated_at = datetime.now(timezone.utc)
            uow.session.add(order)
            uow.session.flush()
            return order_read(order)

    def summary(self) -> OrderSummary:
        with self.uow() as uow:
            return OrderSummary(**uow.orders.summary())

    @staticmethod
    def _restore_stock(uow: OrderUnitOfWork, order: Pedido) -> None:
        for item in order.items:
            product = uow.products.get_by_id(item.producto_id)
            if product is not None:
                product.stock += item.cantidad
