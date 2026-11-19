from fastapi import APIRouter, Depends, status

from app.core.deps import get_current_active_user, require_role
from app.models import Usuario
from app.modules.pedidos.schemas import OrderCreate, OrderPage, OrderRead, OrderSummary, OrderStateChange
from app.modules.pedidos.service import OrderService


router = APIRouter(prefix="/pedidos", tags=["Orders"])


def get_order_service() -> OrderService:
    return OrderService()


@router.post("", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(data: OrderCreate, user: Usuario = Depends(get_current_active_user), service: OrderService = Depends(get_order_service)):
    return service.create(user, data)


@router.get("", response_model=OrderPage)
def list_orders(skip: int = 0, limit: int = 20, estado: str | None = None, user: Usuario = Depends(get_current_active_user), service: OrderService = Depends(get_order_service)):
    return service.list(user, skip, limit, estado)


@router.get("/resumen", response_model=OrderSummary)
def order_summary(_: Usuario = Depends(require_role("admin")), service: OrderService = Depends(get_order_service)):
    return service.summary()


@router.get("/{order_id}", response_model=OrderRead)
def get_order(order_id: int, user: Usuario = Depends(get_current_active_user), service: OrderService = Depends(get_order_service)):
    return service.get(user, order_id)


@router.patch("/{order_id}/estado", response_model=OrderRead)
def change_order_state(order_id: int, data: OrderStateChange, _: Usuario = Depends(require_role("admin")), service: OrderService = Depends(get_order_service)):
    return service.change_state(order_id, data)


@router.patch("/{order_id}/cancelar", response_model=OrderRead)
def cancel_order(order_id: int, user: Usuario = Depends(get_current_active_user), service: OrderService = Depends(get_order_service)):
    return service.cancel(user, order_id)
