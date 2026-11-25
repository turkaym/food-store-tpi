from datetime import datetime, timezone

from sqlalchemy import func
from sqlmodel import Session, select

from app.core.base_repository import BaseRepository
from app.models import Pedido


class OrderRepository(BaseRepository[Pedido]):
    def __init__(self, session: Session):
        super().__init__(session, Pedido)

    def list(self, user_id: int | None, skip: int, limit: int, state: str | None) -> tuple[int, list[Pedido]]:
        query = select(Pedido)
        count_query = select(func.count()).select_from(Pedido)
        if user_id is not None:
            query = query.where(Pedido.usuario_id == user_id)
            count_query = count_query.where(Pedido.usuario_id == user_id)
        if state is not None:
            query = query.where(Pedido.estado == state)
            count_query = count_query.where(Pedido.estado == state)
        total = self.session.exec(count_query).one()
        rows = list(self.session.exec(query.order_by(Pedido.created_at.desc()).offset(skip).limit(limit)))
        return total, rows

    def summary(self) -> dict[str, int | float]:
        today = datetime.now(timezone.utc).date()
        counts = {}
        for state in ("PENDIENTE", "EN_PREPARACION", "ENTREGADO", "CANCELADO"):
            counts[state] = self.session.exec(
                select(func.count()).select_from(Pedido).where(Pedido.estado == state)
            ).one()
        delivered_revenue = self.session.exec(
            select(func.coalesce(func.sum(Pedido.total), 0))
            .where(Pedido.estado == "ENTREGADO")
        ).one()
        today_count = self.session.exec(
            select(func.count()).select_from(Pedido).where(func.date(Pedido.created_at) == today)
        ).one()
        return {
            "pendientes": counts["PENDIENTE"],
            "en_preparacion": counts["EN_PREPARACION"],
            "entregados": counts["ENTREGADO"],
            "cancelados": counts["CANCELADO"],
            "pedidos_hoy": today_count,
            "ingresos_entregados": delivered_revenue,
        }
