from fastapi import APIRouter, Depends, Response, status

from app.core.deps import require_role
from app.models import Usuario
from app.modules.catalog.schemas import CategoryCreate, CategoryRead, CategoryUpdate
from app.modules.catalog.service import CatalogService

router = APIRouter(prefix="/categorias", tags=["Categories"])


def get_service() -> CatalogService:
    return CatalogService()


@router.get("", response_model=list[CategoryRead])
def list_categories(service: CatalogService = Depends(get_service)):
    return service.categories()


@router.get("/{category_id}", response_model=CategoryRead)
def get_category(category_id: int, service: CatalogService = Depends(get_service)):
    return service.category(category_id)


@router.post("", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(data: CategoryCreate, _: Usuario = Depends(require_role("admin")), service: CatalogService = Depends(get_service)):
    return service.create_category(data)


@router.put("/{category_id}", response_model=CategoryRead)
def update_category(category_id: int, data: CategoryUpdate, _: Usuario = Depends(require_role("admin")), service: CatalogService = Depends(get_service)):
    return service.update_category(category_id, data)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, _: Usuario = Depends(require_role("admin")), service: CatalogService = Depends(get_service)):
    service.delete_category(category_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
