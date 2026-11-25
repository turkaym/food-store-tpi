from app.core.unit_of_work import UnitOfWork
from app.modules.categorias.repository import CategoryRepository
from app.modules.productos.repository import ProductRepository


class ProductUnitOfWork(UnitOfWork):
    def __enter__(self) -> "ProductUnitOfWork":
        super().__enter__()
        self.products = ProductRepository(self.session)
        self.categories = CategoryRepository(self.session)
        return self
