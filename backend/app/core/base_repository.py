from typing import Generic, TypeVar

from sqlmodel import Session, SQLModel, select

ModelT = TypeVar("ModelT", bound=SQLModel)


class BaseRepository(Generic[ModelT]):
    def __init__(self, session: Session, model: type[ModelT]):
        self.session = session
        self.model = model

    def get_by_id(self, item_id: int) -> ModelT | None:
        return self.session.get(self.model, item_id)

    def get_all(self) -> list[ModelT]:
        return list(self.session.exec(select(self.model)))

    def add(self, item: ModelT) -> ModelT:
        self.session.add(item)
        self.session.flush()
        return item

    def delete(self, item: ModelT) -> None:
        self.session.delete(item)
