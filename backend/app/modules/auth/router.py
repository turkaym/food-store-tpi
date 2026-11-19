from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.core.database import get_session
from app.core.deps import get_current_active_user, require_role
from app.core.security import create_access_token
from app.models import Usuario
from app.modules.auth.schemas import UserCreate, UserPublic
from app.modules.auth.service import authenticate, public_user, register

router = APIRouter(prefix="/auth", tags=["Auth"])
admin_router = APIRouter(prefix="/admin/usuarios", tags=["Users"])


@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def register_user(data: UserCreate, session: Session = Depends(get_session)):
    return register(session, data)


@router.post("/token")
def login(response: Response, form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = authenticate(session, form.username, form.password)
    response.set_cookie("access_token", create_access_token(user.username), httponly=True, samesite="lax", max_age=1800)
    return {"message": "Login exitoso"}


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logout exitoso"}


@router.get("/me", response_model=UserPublic)
def me(user: Usuario = Depends(get_current_active_user)):
    return public_user(user)


@admin_router.get("", response_model=list[UserPublic])
def list_users(_: Usuario = Depends(require_role("admin")), session: Session = Depends(get_session)):
    return [public_user(user) for user in session.exec(select(Usuario))]


@admin_router.post("/{user_id}/activar", response_model=UserPublic)
def activate(user_id: int, _: Usuario = Depends(require_role("admin")), session: Session = Depends(get_session)):
    return _set_disabled(user_id, False, session)


@admin_router.post("/{user_id}/desactivar", response_model=UserPublic)
def deactivate(user_id: int, current: Usuario = Depends(require_role("admin")), session: Session = Depends(get_session)):
    if current.id == user_id:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="An admin cannot disable itself")
    return _set_disabled(user_id, True, session)


def _set_disabled(user_id: int, disabled: bool, session: Session) -> UserPublic:
    from fastapi import HTTPException
    user = session.get(Usuario, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.disabled = disabled
    session.add(user)
    session.commit()
    session.refresh(user)
    return public_user(user)
