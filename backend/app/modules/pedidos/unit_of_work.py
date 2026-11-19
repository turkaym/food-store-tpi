from app.core.unit_of_work import UnitOfWork
from app.core.base_repository import BaseRepository
from app.models import Pedido, Producto
from app.modules.pedidos.repository import OrderRepository


class OrderUnitOfWork(UnitOfWork):
    def __enter__(self) -> "OrderUnitOfWork":
        super().__enter__()
        self.orders = OrderRepository(self.session)
        self.products = BaseRepository(self.session, Producto)
        return self
