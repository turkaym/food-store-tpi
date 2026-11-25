from sqlmodel import Session

from app.core.base_repository import BaseRepository
from app.models import Usuario


class UserRepository(BaseRepository[Usuario]):
    def __init__(self, session: Session):
        super().__init__(session, Usuario)
