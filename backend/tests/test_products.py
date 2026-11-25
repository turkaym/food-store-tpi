import inspect

import pytest

from app.core.base_repository import BaseRepository
from app.core.deps import get_current_user
from app.main import app
from app.models import Categoria, Producto, Usuario
from app.modules.productos.repository import ProductRepository
from app.modules.productos.router import get_product_service
from app.modules.productos.service import ProductService
from app.modules.productos.unit_of_work import ProductUnitOfWork


def product_payload(category_id: int, name: str = "Test product") -> dict:
    return {
        "categoria_id": category_id,
        "nombre": name,
        "descripcion": "Product description",
        "precio_base": 15.50,
        "imagen_url": "",
        "stock": 8,
        "disponible": True,
    }


def test_product_layers_have_required_responsibilities():
    assert issubclass(ProductRepository, BaseRepository)
    assert "with self.uow() as uow:" in inspect.getsource(ProductService)
    assert issubclass(ProductUnitOfWork, object)

    router_source = inspect.getsource(
        __import__("app.modules.productos.router", fromlist=["router"])
    )
    assert "Depends(get_product_service)" in router_source
    assert "session" not in router_source
    assert "commit(" not in router_source


def test_list_searches_filters_and_paginates_with_nested_category(
    client, session_factory
):
    with session_factory() as session:
        first_category = Categoria(nombre="Meals")
        second_category = Categoria(nombre="Drinks")
        session.add(first_category)
        session.add(second_category)
        session.flush()
        session.add(
            Producto(
                categoria_id=first_category.id,
                nombre="Spicy Burger",
                precio_base=20,
                stock=3,
            )
        )
        session.add(
            Producto(
                categoria_id=second_category.id,
                nombre="Spicy Soda",
                precio_base=5,
                stock=3,
            )
        )
        session.add(
            Producto(
                categoria_id=first_category.id,
                nombre="Inactive Burger",
                precio_base=10,
                activo=False,
            )
        )
        session.commit()
        category_id = first_category.id

    response = client.get(
        "/api/v1/productos",
        params={
            "search": "SPICY",
            "categoria_id": category_id,
            "disponible": True,
            "skip": 0,
            "limit": 1,
        },
    )

    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["items"][0]["nombre"] == "Spicy Burger"
    assert response.json()["items"][0]["categoria"]["nombre"] == "Meals"


@pytest.mark.parametrize(
    "params",
    [
        {"skip": -1},
        {"limit": 0},
        {"limit": 101},
    ],
)
def test_list_rejects_invalid_pagination(client, params: dict[str, int]):
    response = client.get("/api/v1/productos", params=params)

    assert response.status_code == 422


def test_list_accepts_pagination_boundaries(client):
    response = client.get(
        "/api/v1/productos",
        params={"skip": 0, "limit": 100},
    )

    assert response.status_code == 200


def test_create_requires_an_active_category(
    client, session_factory, admin: Usuario
):
    app.dependency_overrides[get_current_user] = lambda: admin
    with session_factory() as session:
        category = Categoria(nombre="Archived", activo=False)
        session.add(category)
        session.commit()
        session.refresh(category)
        category_id = category.id

    response = client.post(
        "/api/v1/productos",
        json=product_payload(category_id),
    )

    assert response.status_code == 404


def test_put_is_partial_and_stock_patch_updates_both_fields(
    client, session_factory, admin: Usuario, product: Producto
):
    app.dependency_overrides[get_current_user] = lambda: admin

    update_response = client.put(
        f"/api/v1/productos/{product.id}",
        json={"nombre": "Renamed product"},
    )
    stock_response = client.patch(
        f"/api/v1/productos/{product.id}/stock",
        json={"stock": 25, "disponible": False},
    )

    assert update_response.status_code == 200
    assert update_response.json()["descripcion"] == product.descripcion
    assert stock_response.status_code == 200
    assert stock_response.json()["stock"] == 25
    assert stock_response.json()["disponible"] is False


def test_delete_is_logical_and_inactive_product_returns_404(
    client, session_factory, admin: Usuario, product: Producto
):
    app.dependency_overrides[get_current_user] = lambda: admin

    delete_response = client.delete(f"/api/v1/productos/{product.id}")
    detail_response = client.get(f"/api/v1/productos/{product.id}")
    update_response = client.put(
        f"/api/v1/productos/{product.id}",
        json={"nombre": "Unavailable"},
    )

    assert delete_response.status_code == 204
    assert delete_response.content == b""
    assert detail_response.status_code == 404
    assert update_response.status_code == 404
    with session_factory() as session:
        stored = session.get(Producto, product.id)
        assert stored is not None
        assert stored.activo is False
