import pytest

from app.core.deps import get_current_user
from app.main import app
from app.models import Pedido, Producto, Usuario


def order_payload(product_id: int, quantity: int = 1) -> dict:
    return {
        "items": [{"producto_id": product_id, "cantidad": quantity}],
        "forma_pago": "EFECTIVO",
        "direccion_entrega": "Test address",
    }


def test_duplicate_product_returns_400(client, product: Producto):
    payload = order_payload(product.id)
    payload["items"].append(payload["items"][0].copy())

    response = client.post("/api/v1/pedidos", json=payload)

    assert response.status_code == 400


@pytest.mark.parametrize(
    ("field", "value"),
    [("disponible", False), ("stock", 0)],
)
def test_product_business_violation_returns_400(
    client, session_factory, product: Producto, field: str, value
):
    with session_factory() as session:
        stored = session.get(Producto, product.id)
        setattr(stored, field, value)
        session.add(stored)
        session.commit()

    response = client.post("/api/v1/pedidos", json=order_payload(product.id))

    assert response.status_code == 400


def test_invalid_transition_returns_400(client, admin: Usuario, order: Pedido):
    app.dependency_overrides[get_current_user] = lambda: admin

    response = client.patch(
        f"/api/v1/pedidos/{order.id}/estado",
        json={"estado": "ENTREGADO"},
    )

    assert response.status_code == 400


def test_invalid_cancellation_returns_400(client, session_factory, order: Pedido):
    with session_factory() as session:
        stored = session.get(Pedido, order.id)
        stored.estado = "EN_PREPARACION"
        session.add(stored)
        session.commit()

    response = client.patch(f"/api/v1/pedidos/{order.id}/cancelar")

    assert response.status_code == 400


def test_missing_product_returns_404(client):
    response = client.post("/api/v1/pedidos", json=order_payload(9999))

    assert response.status_code == 404


def test_inactive_product_returns_404(client, session_factory, product: Producto):
    with session_factory() as session:
        stored = session.get(Producto, product.id)
        stored.activo = False
        session.add(stored)
        session.commit()

    response = client.post("/api/v1/pedidos", json=order_payload(product.id))

    assert response.status_code == 404


def test_foreign_order_returns_403(client, session_factory, order: Pedido):
    with session_factory() as session:
        other_user = Usuario(
            username="other",
            full_name="Other Customer",
            email="other@example.com",
            hashed_password="unused",
        )
        session.add(other_user)
        session.commit()
        session.refresh(other_user)
        stored_order = session.get(Pedido, order.id)
        stored_order.usuario_id = other_user.id
        session.add(stored_order)
        session.commit()

    response = client.get(f"/api/v1/pedidos/{order.id}")

    assert response.status_code == 403


def test_schema_validation_remains_422(client, product: Producto):
    payload = order_payload(product.id, quantity=0)

    response = client.post("/api/v1/pedidos", json=payload)

    assert response.status_code == 422
