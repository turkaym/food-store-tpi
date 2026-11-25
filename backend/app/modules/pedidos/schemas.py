from datetime import datetime
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
    precio_unitario: float = Field(ge=0)
    cantidad: int
    subtotal: float = Field(ge=0)


class OrderRead(SQLModel):
    id: int
    usuario_id: int
    estado: str
    forma_pago: str
    direccion_entrega: str
    notas: str | None
    total: float = Field(ge=0)
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
    ingresos_entregados: float = Field(ge=0)
