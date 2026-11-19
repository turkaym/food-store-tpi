from typing import Callable

from fastapi import Cookie, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.database import get_session
from app.core.security import decode_access_token
from app.models import Usuario


def get_current_user(access_token: str | None = Cookie(default=None), session: Session = Depends(get_session)) -> Usuario:
    username = decode_access_token(access_token or "")
    user = session.exec(select(Usuario).where(Usuario.username == username)).first() if username else None
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing session")
    return user


def get_current_active_user(user: Usuario = Depends(get_current_user)) -> Usuario:
    if user.disabled:
        raise HTTPException(status_code=400, detail="Cuenta de usuario desactivada")
    return user


def require_role(*roles: str) -> Callable:
    def dependency(user: Usuario = Depends(get_current_active_user)) -> Usuario:
        if user.role not in roles:
            raise HTTPException(status_code=403, detail="Insufficient role")
        return user
    return dependency
