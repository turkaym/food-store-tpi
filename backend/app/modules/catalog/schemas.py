from pydantic import Field, HttpUrl
from sqlmodel import SQLModel


class CategoryCreate(SQLModel):
    nombre: str = Field(min_length=2, max_length=100)
    descripcion: str = ""


class CategoryUpdate(SQLModel):
    nombre: str | None = Field(default=None, min_length=2, max_length=100)
    descripcion: str | None = None


class CategoryRead(CategoryCreate):
    id: int
    activo: bool


class ProductCreate(SQLModel):
    categoria_id: int
    nombre: str = Field(min_length=1, max_length=120)
    descripcion: str = ""
    precio_base: float = Field(ge=0)
    imagen_url: str = ""
    stock: int = Field(default=0, ge=0)
    disponible: bool = True


class ProductUpdate(SQLModel):
    categoria_id: int | None = None
    nombre: str | None = Field(default=None, min_length=1, max_length=120)
    descripcion: str | None = None
    precio_base: float | None = Field(default=None, ge=0)
    imagen_url: str | None = None
    stock: int | None = Field(default=None, ge=0)
    disponible: bool | None = None


class ProductStockUpdate(SQLModel):
    stock: int = Field(ge=0)
    disponible: bool | None = None


class ProductRead(ProductCreate):
    id: int
    activo: bool
    categoria: CategoryRead


class ProductPage(SQLModel):
    total: int
    items: list[ProductRead]
