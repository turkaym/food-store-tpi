from app.core.unit_of_work import UnitOfWork
from app.modules.usuarios.repository import UserRepository


class UserUnitOfWork(UnitOfWork):
    def __enter__(self) -> "UserUnitOfWork":
        super().__enter__()
        self.users = UserRepository(self.session)
        return self
