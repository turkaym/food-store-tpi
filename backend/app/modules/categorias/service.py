from collections.abc import Callable

from app.models import Categoria
from app.modules.catalog.schemas import CategoryCreate, CategoryRead, CategoryUpdate
from app.modules.categorias.unit_of_work import CategoryUnitOfWork


class CategoryNotFoundError(Exception):
    pass


class DuplicateCategoryNameError(Exception):
    pass


class CategoryService:
    def __init__(
        self,
        uow: Callable[[], CategoryUnitOfWork] = CategoryUnitOfWork,
    ):
        self.uow = uow

    def list(self) -> list[CategoryRead]:
        with self.uow() as uow:
            return [CategoryRead.model_validate(row) for row in uow.categories.list_active()]

    def get(self, category_id: int) -> CategoryRead:
        with self.uow() as uow:
            category = self._get_active(uow, category_id)
            return CategoryRead.model_validate(category)

    def create(self, data: CategoryCreate) -> CategoryRead:
        with self.uow() as uow:
            if uow.categories.get_by_name(data.nombre) is not None:
                raise DuplicateCategoryNameError
            category = uow.categories.add(Categoria.model_validate(data))
            return CategoryRead.model_validate(category)

    def update(self, category_id: int, data: CategoryUpdate) -> CategoryRead:
        with self.uow() as uow:
            category = self._get_active(uow, category_id)
            values = data.model_dump(exclude_unset=True)
            new_name = values.get("nombre")
            existing = uow.categories.get_by_name(new_name) if new_name else None
            if existing is not None and existing.id != category.id:
                raise DuplicateCategoryNameError
            for key, value in values.items():
                setattr(category, key, value)
            uow.categories.add(category)
            return CategoryRead.model_validate(category)

    def delete(self, category_id: int) -> None:
        with self.uow() as uow:
            category = self._get_active(uow, category_id)
            category.activo = False
            uow.categories.add(category)

    @staticmethod
    def _get_active(uow: CategoryUnitOfWork, category_id: int) -> Categoria:
        category = uow.categories.get_active_by_id(category_id)
        if category is None:
            raise CategoryNotFoundError
        return category
