from contextlib import contextmanager

from fastapi import APIRouter, Depends, HTTPException

from app.core.deps import require_role
from app.models import Usuario
from app.modules.usuarios.schemas import UserPublic
from app.modules.usuarios.service import (
    SelfDeactivationError,
    UserNotFoundError,
    UserService,
)

router = APIRouter(prefix="/admin/usuarios", tags=["Users"])


def get_user_service() -> UserService:
    return UserService()


@contextmanager
def translate_user_errors():
    try:
        yield
    except UserNotFoundError as error:
        raise HTTPException(404, "User not found") from error
    except SelfDeactivationError as error:
        raise HTTPException(400, "An admin cannot disable itself") from error


@router.get("", response_model=list[UserPublic])
def list_users(
    _: Usuario = Depends(require_role("admin")),
    service: UserService = Depends(get_user_service),
):
    return service.list()


@router.post("/{user_id}/activar", response_model=UserPublic)
def activate(
    user_id: int,
    current: Usuario = Depends(require_role("admin")),
    service: UserService = Depends(get_user_service),
):
    with translate_user_errors():
        return service.set_disabled(user_id, False, current.id)


@router.post("/{user_id}/desactivar", response_model=UserPublic)
def deactivate(
    user_id: int,
    current: Usuario = Depends(require_role("admin")),
    service: UserService = Depends(get_user_service),
):
    with translate_user_errors():
        return service.set_disabled(user_id, True, current.id)
