from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from app.core import unit_of_work
from app.core.deps import get_current_user
from app.main import app
from app.models import Categoria, Pedido, Producto, Usuario


@pytest.fixture
def session_factory(monkeypatch: pytest.MonkeyPatch):
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    def factory() -> Session:
        return Session(engine)

    monkeypatch.setattr(unit_of_work, "session_factory", factory)
    yield factory
    SQLModel.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def user(session_factory) -> Usuario:
    with session_factory() as session:
        user = Usuario(
            username="customer",
            full_name="Test Customer",
            email="customer@example.com",
            hashed_password="unused",
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        session.expunge(user)
        return user


@pytest.fixture
def admin(session_factory) -> Usuario:
    with session_factory() as session:
        admin = Usuario(
            username="admin-test",
            full_name="Test Admin",
            email="admin@example.com",
            hashed_password="unused",
            role="admin",
        )
        session.add(admin)
        session.commit()
        session.refresh(admin)
        session.expunge(admin)
        return admin


@pytest.fixture
def client(user: Usuario) -> Iterator[TestClient]:
    app.dependency_overrides[get_current_user] = lambda: user
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


@pytest.fixture
def product(session_factory) -> Producto:
    with session_factory() as session:
        category = Categoria(nombre="Meals", descripcion="Prepared meals")
        session.add(category)
        session.flush()
        product = Producto(
            categoria_id=category.id,
            nombre="Test meal",
            precio_base=10,
            stock=5,
        )
        session.add(product)
        session.commit()
        session.refresh(product)
        session.expunge(product)
        return product


@pytest.fixture
def order(session_factory, user: Usuario, product: Producto) -> Pedido:
    with session_factory() as session:
        order = Pedido(
            usuario_id=user.id,
            forma_pago="EFECTIVO",
            direccion_entrega="Test address",
        )
        session.add(order)
        session.commit()
        session.refresh(order)
        session.expunge(order)
        return order
