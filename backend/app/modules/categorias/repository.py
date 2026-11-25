from sqlmodel import Session, select

from app.core.base_repository import BaseRepository
from app.models import Categoria


class CategoryRepository(BaseRepository[Categoria]):
    def __init__(self, session: Session):
        super().__init__(session, Categoria)

    def list_active(self) -> list[Categoria]:
        return list(self.session.exec(select(Categoria).where(Categoria.activo)))

    def get_active_by_id(self, category_id: int) -> Categoria | None:
        return self.session.exec(
            select(Categoria).where(
                Categoria.id == category_id,
                Categoria.activo,
            )
        ).first()

    def get_by_name(self, name: str) -> Categoria | None:
        return self.session.exec(
            select(Categoria).where(Categoria.nombre == name)
        ).first()
