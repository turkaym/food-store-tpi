from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.core.database import get_session
from app.core.deps import get_current_active_user
from app.core.security import create_access_token
from app.models import Usuario
from app.modules.auth.schemas import UserCreate, UserPublic
from app.modules.auth.service import authenticate, public_user, register

router = APIRouter(prefix="/auth", tags=["Auth"])


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
