from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import Field
from sqlmodel import SQLModel


OrderState = Literal["PENDIENTE", "EN_PREPARACION", "ENTREGADO", "CANCELADO"]
PaymentMethod = Literal["EFECTIVO", "TRANSFERENCIA"]


class OrderItemCreate(SQLModel):
    producto_id: int
    cantidad: int = Field(ge=1)


class OrderCreate(SQLModel):
    items: list[OrderItemCreate] = Field(min_length=1)
    forma_pago: PaymentMethod
    direccion_entrega: str = Field(min_length=5, max_length=200)
    notas: str | None = None


class OrderItemRead(SQLModel):
    producto_id: int
    nombre_producto: str
    precio_unitario: Decimal
    cantidad: int
    subtotal: Decimal


class OrderRead(SQLModel):
    id: int
    usuario_id: int
    estado: str
    forma_pago: str
    direccion_entrega: str
    notas: str | None
    total: Decimal
    created_at: datetime
    updated_at: datetime
    items: list[OrderItemRead]


class OrderPage(SQLModel):
    total: int
    items: list[OrderRead]


class OrderStateChange(SQLModel):
    estado: OrderState


class OrderSummary(SQLModel):
    pendientes: int
    en_preparacion: int
    entregados: int
    cancelados: int
    pedidos_hoy: int
    ingresos_entregados: Decimal
