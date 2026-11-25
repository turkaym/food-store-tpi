from collections.abc import Callable

from app.models import Producto
from app.modules.catalog.schemas import (
    ProductCreate,
    ProductPage,
    ProductRead,
    ProductStockUpdate,
    ProductUpdate,
)
from app.modules.productos.unit_of_work import ProductUnitOfWork


class ProductNotFoundError(Exception):
    pass


class ProductCategoryNotFoundError(Exception):
    pass


class ProductService:
    def __init__(
        self,
        uow: Callable[[], ProductUnitOfWork] = ProductUnitOfWork,
    ):
        self.uow = uow

    def list(
        self,
        skip: int,
        limit: int,
        search: str | None,
        category_id: int | None,
        available: bool | None,
    ) -> ProductPage:
        with self.uow() as uow:
            total, rows = uow.products.search(
                max(skip, 0),
                min(limit, 100),
                search,
                category_id,
                available,
            )
            return ProductPage(
                total=total,
                items=[ProductRead.model_validate(row) for row in rows],
            )

    def get(self, product_id: int) -> ProductRead:
        with self.uow() as uow:
            product = self._get_active(uow, product_id)
            return ProductRead.model_validate(product)

    def create(self, data: ProductCreate) -> ProductRead:
        with self.uow() as uow:
            self._require_active_category(uow, data.categoria_id)
            product = uow.products.add(Producto.model_validate(data))
            return ProductRead.model_validate(product)

    def update(self, product_id: int, data: ProductUpdate) -> ProductRead:
        with self.uow() as uow:
            product = self._get_active(uow, product_id)
            values = data.model_dump(exclude_unset=True)
            if "categoria_id" in values:
                self._require_active_category(uow, values["categoria_id"])
            for key, value in values.items():
                setattr(product, key, value)
            uow.products.add(product)
            return ProductRead.model_validate(product)

    def update_stock(
        self,
        product_id: int,
        data: ProductStockUpdate,
    ) -> ProductRead:
        with self.uow() as uow:
            product = self._get_active(uow, product_id)
            product.stock = data.stock
            if data.disponible is not None:
                product.disponible = data.disponible
            uow.products.add(product)
            return ProductRead.model_validate(product)

    def delete(self, product_id: int) -> None:
        with self.uow() as uow:
            product = self._get_active(uow, product_id)
            product.activo = False
            uow.products.add(product)

    @staticmethod
    def _get_active(uow: ProductUnitOfWork, product_id: int) -> Producto:
        product = uow.products.get_active_by_id(product_id)
        if product is None:
            raise ProductNotFoundError
        return product

    @staticmethod
    def _require_active_category(uow: ProductUnitOfWork, category_id: int) -> None:
        if uow.categories.get_active_by_id(category_id) is None:
            raise ProductCategoryNotFoundError
