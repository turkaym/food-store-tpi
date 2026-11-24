import inspect

from app.core.base_repository import BaseRepository
from app.core.deps import get_current_user
from app.main import app
from app.models import Categoria, Usuario
from app.modules.categorias.repository import CategoryRepository
from app.modules.categorias.router import get_category_service
from app.modules.categorias.service import CategoryService
from app.modules.categorias.unit_of_work import CategoryUnitOfWork


def test_category_layers_have_required_responsibilities():
    assert issubclass(CategoryRepository, BaseRepository)
    assert "with self.uow() as uow:" in inspect.getsource(CategoryService)
    assert issubclass(CategoryUnitOfWork, object)

    router_source = inspect.getsource(
        __import__("app.modules.categorias.router", fromlist=["router"])
    )
    assert "Depends(get_category_service)" in router_source
    assert "session" not in router_source
    assert "commit(" not in router_source


def test_list_and_detail_only_return_active_categories(client, session_factory):
    with session_factory() as session:
        active = Categoria(nombre="Active", descripcion="Visible")
        inactive = Categoria(nombre="Inactive", descripcion="Hidden", activo=False)
        session.add(active)
        session.add(inactive)
        session.commit()
        session.refresh(inactive)
        inactive_id = inactive.id

    list_response = client.get("/api/v1/categorias")
    detail_response = client.get(f"/api/v1/categorias/{inactive_id}")

    assert list_response.status_code == 200
    assert [item["nombre"] for item in list_response.json()] == ["Active"]
    assert detail_response.status_code == 404


def test_create_rejects_duplicate_name(client, session_factory, admin: Usuario):
    app.dependency_overrides[get_current_user] = lambda: admin
    with session_factory() as session:
        session.add(Categoria(nombre="Unique", descripcion="Original"))
        session.commit()

    response = client.post(
        "/api/v1/categorias",
        json={"nombre": "Unique", "descripcion": "Duplicate"},
    )

    assert response.status_code == 409


def test_put_is_partial_and_delete_is_logical(
    client, session_factory, admin: Usuario
):
    app.dependency_overrides[get_current_user] = lambda: admin
    with session_factory() as session:
        category = Categoria(nombre="Original", descripcion="Keep me")
        session.add(category)
        session.commit()
        session.refresh(category)
        category_id = category.id

    update_response = client.put(
        f"/api/v1/categorias/{category_id}",
        json={"nombre": "Renamed"},
    )
    delete_response = client.delete(f"/api/v1/categorias/{category_id}")

    assert update_response.status_code == 200
    assert update_response.json()["descripcion"] == "Keep me"
    assert delete_response.status_code == 204
    assert delete_response.content == b""
    with session_factory() as session:
        stored = session.get(Categoria, category_id)
        assert stored is not None
        assert stored.activo is False
