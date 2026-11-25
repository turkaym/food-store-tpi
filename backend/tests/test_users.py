import inspect

from app.core.base_repository import BaseRepository
from app.core.deps import get_current_user
from app.main import app
from app.models import Usuario
from app.modules.usuarios.repository import UserRepository
from app.modules.usuarios.service import UserService


def test_user_layers_have_required_responsibilities():
    assert issubclass(UserRepository, BaseRepository)
    assert "with self.uow() as uow:" in inspect.getsource(UserService)

    router_source = inspect.getsource(
        __import__("app.modules.usuarios.router", fromlist=["router"])
    )
    assert "Depends(get_user_service)" in router_source
    assert "session" not in router_source
    assert "commit(" not in router_source


def test_admin_can_list_and_disable_users(
    client,
    session_factory,
    admin: Usuario,
    user: Usuario,
):
    app.dependency_overrides[get_current_user] = lambda: admin

    list_response = client.get("/api/v1/admin/usuarios")
    disable_response = client.post(
        f"/api/v1/admin/usuarios/{user.id}/desactivar"
    )

    assert list_response.status_code == 200
    assert {item["username"] for item in list_response.json()} == {
        "admin-test",
        "customer",
    }
    assert disable_response.status_code == 200
    assert disable_response.json()["disabled"] is True
    with session_factory() as session:
        stored = session.get(Usuario, user.id)
        assert stored is not None
        assert stored.disabled is True


def test_admin_cannot_disable_itself(client, admin: Usuario):
    app.dependency_overrides[get_current_user] = lambda: admin

    response = client.post(
        f"/api/v1/admin/usuarios/{admin.id}/desactivar"
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "An admin cannot disable itself"


def test_non_admin_cannot_manage_users(client):
    response = client.get("/api/v1/admin/usuarios")

    assert response.status_code == 403
