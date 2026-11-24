from contextlib import contextmanager

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.core.deps import require_role
from app.models import Usuario
from app.modules.catalog.schemas import CategoryCreate, CategoryRead, CategoryUpdate
from app.modules.categorias.service import (
    CategoryNotFoundError,
    CategoryService,
    DuplicateCategoryNameError,
)

router = APIRouter(prefix="/categorias", tags=["Categories"])


def get_category_service() -> CategoryService:
    return CategoryService()


@contextmanager
def translate_category_errors():
    try:
        yield
    except CategoryNotFoundError as error:
        raise HTTPException(404, "Category not found") from error
    except DuplicateCategoryNameError as error:
        raise HTTPException(409, "Category name already exists") from error


@router.get("", response_model=list[CategoryRead])
def list_categories(service: CategoryService = Depends(get_category_service)):
    return service.list()


@router.get("/{category_id}", response_model=CategoryRead)
def get_category(category_id: int, service: CategoryService = Depends(get_category_service)):
    with translate_category_errors():
        return service.get(category_id)


@router.post("", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(data: CategoryCreate, _: Usuario = Depends(require_role("admin")), service: CategoryService = Depends(get_category_service)):
    with translate_category_errors():
        return service.create(data)


@router.put("/{category_id}", response_model=CategoryRead)
def update_category(category_id: int, data: CategoryUpdate, _: Usuario = Depends(require_role("admin")), service: CategoryService = Depends(get_category_service)):
    with translate_category_errors():
        return service.update(category_id, data)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, _: Usuario = Depends(require_role("admin")), service: CategoryService = Depends(get_category_service)):
    with translate_category_errors():
        service.delete(category_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
