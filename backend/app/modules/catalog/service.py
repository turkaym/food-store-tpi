from datetime import datetime, timezone

from fastapi import HTTPException
from sqlmodel import Session, select

from app.core.base_repository import BaseRepository
from app.core.unit_of_work import UnitOfWork
from app.models import Categoria, Producto
from app.modules.catalog.schemas import CategoryCreate, CategoryRead, CategoryUpdate, ProductCreate, ProductRead, ProductStockUpdate, ProductUpdate


def category_read(category: Categoria) -> CategoryRead:
    return CategoryRead.model_validate(category)


def product_read(product: Producto) -> ProductRead:
    return ProductRead.model_validate(product)


class CatalogService:
    def __init__(self, uow: type[UnitOfWork] = UnitOfWork):
        self.uow = uow

    def categories(self) -> list[CategoryRead]:
        with self.uow() as uow:
            rows = uow.session.exec(select(Categoria).where(Categoria.activo)).all()
            return [category_read(row) for row in rows]

    def category(self, category_id: int) -> CategoryRead:
        with self.uow() as uow:
            row = uow.session.get(Categoria, category_id)
            if row is None or not row.activo:
                raise HTTPException(404, "Category not found")
            return category_read(row)

    def create_category(self, data: CategoryCreate) -> CategoryRead:
        with self.uow() as uow:
            if uow.session.exec(select(Categoria).where(Categoria.nombre == data.nombre)).first():
                raise HTTPException(409, "Category name already exists")
            row = Categoria.model_validate(data)
            uow.session.add(row)
            uow.session.flush()
            return category_read(row)

    def update_category(self, category_id: int, data: CategoryUpdate) -> CategoryRead:
        with self.uow() as uow:
            row = uow.session.get(Categoria, category_id)
            if row is None or not row.activo:
                raise HTTPException(404, "Category not found")
            if data.nombre and data.nombre != row.nombre and uow.session.exec(select(Categoria).where(Categoria.nombre == data.nombre)).first():
                raise HTTPException(409, "Category name already exists")
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(row, key, value)
            uow.session.add(row)
            uow.session.flush()
            return category_read(row)

    def delete_category(self, category_id: int) -> None:
        with self.uow() as uow:
            row = uow.session.get(Categoria, category_id)
            if row is None or not row.activo:
                raise HTTPException(404, "Category not found")
            row.activo = False
            uow.session.add(row)

    def products(self, skip: int, limit: int, search: str | None, categoria_id: int | None, disponible: bool | None) -> dict:
        with self.uow() as uow:
            query = select(Producto).where(Producto.activo)
            if search:
                query = query.where(Producto.nombre.ilike(f"%{search}%"))
            if categoria_id is not None:
                query = query.where(Producto.categoria_id == categoria_id)
            if disponible is not None:
                query = query.where(Producto.disponible == disponible)
            rows = list(uow.session.exec(query))
            return {"total": len(rows), "items": [product_read(row) for row in rows[skip:skip + limit]]}

    def product(self, product_id: int) -> ProductRead:
        with self.uow() as uow:
            row = uow.session.get(Producto, product_id)
            if row is None or not row.activo:
                raise HTTPException(404, "Product not found")
            return product_read(row)

    def create_product(self, data: ProductCreate) -> ProductRead:
        with self.uow() as uow:
            category = uow.session.get(Categoria, data.categoria_id)
            if category is None or not category.activo:
                raise HTTPException(404, "Category not found")
            row = Producto.model_validate(data)
            uow.session.add(row)
            uow.session.flush()
            return product_read(row)

    def update_product(self, product_id: int, data: ProductUpdate) -> ProductRead:
        with self.uow() as uow:
            row = uow.session.get(Producto, product_id)
            if row is None or not row.activo:
                raise HTTPException(404, "Product not found")
            values = data.model_dump(exclude_unset=True)
            if "categoria_id" in values:
                category = uow.session.get(Categoria, values["categoria_id"])
                if category is None or not category.activo:
                    raise HTTPException(404, "Category not found")
            for key, value in values.items():
                setattr(row, key, value)
            uow.session.add(row)
            uow.session.flush()
            return product_read(row)

    def update_stock(self, product_id: int, data: ProductStockUpdate) -> ProductRead:
        return self.update_product(product_id, ProductUpdate(stock=data.stock, disponible=data.disponible))

    def delete_product(self, product_id: int) -> None:
        with self.uow() as uow:
            row = uow.session.get(Producto, product_id)
            if row is None or not row.activo:
                raise HTTPException(404, "Product not found")
            row.activo = False
            uow.session.add(row)
