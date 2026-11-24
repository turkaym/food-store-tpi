from app.core.unit_of_work import UnitOfWork
from app.modules.categorias.repository import CategoryRepository


class CategoryUnitOfWork(UnitOfWork):
    def __enter__(self) -> "CategoryUnitOfWork":
        super().__enter__()
        self.categories = CategoryRepository(self.session)
        return self
