from fastapi import APIRouter, Depends, Response, status

from app.core.deps import require_role
from app.models import Usuario
from app.modules.catalog.schemas import ProductCreate, ProductPage, ProductRead, ProductStockUpdate, ProductUpdate
from app.modules.catalog.service import CatalogService

router = APIRouter(prefix="/productos", tags=["Products"])


def get_service() -> CatalogService:
    return CatalogService()


@router.get("", response_model=ProductPage)
def list_products(skip: int = 0, limit: int = 20, search: str | None = None, categoria_id: int | None = None, disponible: bool | None = None, service: CatalogService = Depends(get_service)):
    if limit > 100:
        limit = 100
    return service.products(max(skip, 0), limit, search, categoria_id, disponible)


@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, service: CatalogService = Depends(get_service)):
    return service.product(product_id)


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(data: ProductCreate, _: Usuario = Depends(require_role("admin")), service: CatalogService = Depends(get_service)):
    return service.create_product(data)


@router.put("/{product_id}", response_model=ProductRead)
def update_product(product_id: int, data: ProductUpdate, _: Usuario = Depends(require_role("admin")), service: CatalogService = Depends(get_service)):
    return service.update_product(product_id, data)


@router.patch("/{product_id}/stock", response_model=ProductRead)
def update_stock(product_id: int, data: ProductStockUpdate, _: Usuario = Depends(require_role("admin")), service: CatalogService = Depends(get_service)):
    return service.update_stock(product_id, data)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, _: Usuario = Depends(require_role("admin")), service: CatalogService = Depends(get_service)):
    service.delete_product(product_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
