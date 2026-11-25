from contextlib import contextmanager

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from app.core.deps import require_role
from app.models import Usuario
from app.modules.catalog.schemas import ProductCreate, ProductPage, ProductRead, ProductStockUpdate, ProductUpdate
from app.modules.productos.service import (
    ProductCategoryNotFoundError,
    ProductNotFoundError,
    ProductService,
)

router = APIRouter(prefix="/productos", tags=["Products"])


def get_product_service() -> ProductService:
    return ProductService()


@contextmanager
def translate_product_errors():
    try:
        yield
    except ProductNotFoundError as error:
        raise HTTPException(404, "Product not found") from error
    except ProductCategoryNotFoundError as error:
        raise HTTPException(404, "Category not found") from error


@router.get("", response_model=ProductPage)
def list_products(skip: int = Query(default=0, ge=0), limit: int = Query(default=20, ge=1, le=100), search: str | None = None, categoria_id: int | None = None, disponible: bool | None = None, service: ProductService = Depends(get_product_service)):
    return service.list(skip, limit, search, categoria_id, disponible)


@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, service: ProductService = Depends(get_product_service)):
    with translate_product_errors():
        return service.get(product_id)


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(data: ProductCreate, _: Usuario = Depends(require_role("admin")), service: ProductService = Depends(get_product_service)):
    with translate_product_errors():
        return service.create(data)


@router.put("/{product_id}", response_model=ProductRead)
def update_product(product_id: int, data: ProductUpdate, _: Usuario = Depends(require_role("admin")), service: ProductService = Depends(get_product_service)):
    with translate_product_errors():
        return service.update(product_id, data)


@router.patch("/{product_id}/stock", response_model=ProductRead)
def update_stock(product_id: int, data: ProductStockUpdate, _: Usuario = Depends(require_role("admin")), service: ProductService = Depends(get_product_service)):
    with translate_product_errors():
        return service.update_stock(product_id, data)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, _: Usuario = Depends(require_role("admin")), service: ProductService = Depends(get_product_service)):
    with translate_product_errors():
        service.delete(product_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
