from sqlalchemy import func
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from app.core.base_repository import BaseRepository
from app.models import Producto


class ProductRepository(BaseRepository[Producto]):
    def __init__(self, session: Session):
        super().__init__(session, Producto)

    def search(
        self,
        skip: int,
        limit: int,
        search: str | None,
        category_id: int | None,
        available: bool | None,
    ) -> tuple[int, list[Producto]]:
        filters = [Producto.activo]
        if search:
            filters.append(Producto.nombre.ilike(f"%{search}%"))
        if category_id is not None:
            filters.append(Producto.categoria_id == category_id)
        if available is not None:
            filters.append(Producto.disponible == available)

        count_query = select(func.count()).select_from(Producto).where(*filters)
        query = (
            select(Producto)
            .where(*filters)
            .options(selectinload(Producto.categoria))
            .order_by(Producto.id)
            .offset(skip)
            .limit(limit)
        )
        total = self.session.exec(count_query).one()
        return total, list(self.session.exec(query))

    def get_active_by_id(self, product_id: int) -> Producto | None:
        return self.session.exec(
            select(Producto)
            .where(Producto.id == product_id, Producto.activo)
            .options(selectinload(Producto.categoria))
        ).first()
