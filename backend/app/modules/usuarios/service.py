from collections.abc import Callable

from app.modules.usuarios.schemas import UserPublic
from app.modules.usuarios.unit_of_work import UserUnitOfWork


class UserNotFoundError(Exception):
    pass


class SelfDeactivationError(Exception):
    pass


class UserService:
    def __init__(self, uow: Callable[[], UserUnitOfWork] = UserUnitOfWork):
        self.uow = uow

    def list(self) -> list[UserPublic]:
        with self.uow() as uow:
            return [UserPublic.model_validate(user) for user in uow.users.get_all()]

    def set_disabled(
        self,
        user_id: int,
        disabled: bool,
        current_user_id: int,
    ) -> UserPublic:
        if disabled and current_user_id == user_id:
            raise SelfDeactivationError
        with self.uow() as uow:
            user = uow.users.get_by_id(user_id)
            if user is None:
                raise UserNotFoundError
            user.disabled = disabled
            uow.users.add(user)
            return UserPublic.model_validate(user)
