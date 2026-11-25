from datetime import datetime

from pydantic import EmailStr
from sqlmodel import SQLModel


class UserPublic(SQLModel):
    id: int
    username: str
    full_name: str
    email: EmailStr
    role: str
    disabled: bool
    created_at: datetime
