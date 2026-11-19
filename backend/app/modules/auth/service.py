from fastapi import HTTPException
from sqlmodel import Session, select

from app.core.security import hash_password, verify_password
from app.models import Usuario
from app.modules.auth.schemas import UserCreate, UserPublic


def public_user(user: Usuario) -> UserPublic:
    return UserPublic.model_validate(user)


def register(session: Session, data: UserCreate) -> UserPublic:
    exists = session.exec(select(Usuario).where((Usuario.username == data.username) | (Usuario.email == data.email))).first()
    if exists:
        raise HTTPException(status_code=409, detail="Username or email already exists")
    user = Usuario(username=data.username, full_name=data.full_name, email=data.email, hashed_password=hash_password(data.password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return public_user(user)


def authenticate(session: Session, username: str, password: str) -> Usuario:
    user = session.exec(select(Usuario).where(Usuario.username == username)).first()
    if user is None or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    if user.disabled:
        raise HTTPException(status_code=400, detail="Cuenta de usuario desactivada")
    return user
