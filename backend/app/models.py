from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import Column, Numeric
from sqlmodel import Field, Relationship, SQLModel


class Usuario(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True, max_length=50)
    full_name: str = Field(max_length=120)
    email: str = Field(unique=True, index=True, max_length=255)
    hashed_password: str = Field(max_length=255)
    role: str = Field(default="user", max_length=10)
    disabled: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    pedidos: list["Pedido"] = Relationship(back_populates="usuario")


class Categoria(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True, index=True, min_length=2, max_length=100)
    descripcion: str = ""
    activo: bool = True
    productos: list["Producto"] = Relationship(back_populates="categoria")


class Producto(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    categoria_id: int = Field(foreign_key="categoria.id")
    nombre: str = Field(index=True, max_length=120)
    descripcion: str = ""
    precio_base: Decimal = Field(sa_column=Column(Numeric(12, 2), nullable=False))
    imagen_url: str = ""
    stock: int = Field(default=0, ge=0)
    disponible: bool = True
    activo: bool = True
    categoria: Categoria = Relationship(back_populates="productos")
    detalles: list["DetallePedido"] = Relationship(back_populates="producto")


class Pedido(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id")
    estado: str = "PENDIENTE"
    forma_pago: str
    direccion_entrega: str = Field(min_length=5, max_length=200)
    notas: str | None = None
    total: Decimal = Field(default=Decimal("0.00"), sa_column=Column(Numeric(12, 2), nullable=False))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    usuario: Usuario = Relationship(back_populates="pedidos")
    items: list["DetallePedido"] = Relationship(back_populates="pedido")


class DetallePedido(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    pedido_id: int = Field(foreign_key="pedido.id")
    producto_id: int = Field(foreign_key="producto.id")
    cantidad: int = Field(ge=1)
    nombre_producto: str
    precio_unitario: Decimal = Field(sa_column=Column(Numeric(12, 2), nullable=False))
    subtotal: Decimal = Field(sa_column=Column(Numeric(12, 2), nullable=False))
    pedido: Pedido = Relationship(back_populates="items")
    producto: Producto = Relationship(back_populates="detalles")
