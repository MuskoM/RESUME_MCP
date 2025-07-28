from abc import ABC
from collections.abc import Iterable
from typing import Protocol, TypeVar
from uuid import UUID

from sqlalchemy.orm import Session

from schema import Base, Posting

Model = TypeVar("Model", bound=Base)


class IRepository(Protocol[Model]):
    def get_one(self, item_id: int | UUID) -> Model | None: ...

    def get_multiple(self, items_id: Iterable[int | UUID]) -> Iterable[Model]: ...

    def add_one(self, item: Model) -> None: ...

    def add_many(self, items: Iterable[Model]) -> None: ...

    def delete_one(self, item_id: int | UUID) -> None: ...

    def delete_many(self, items_id: Iterable[int | UUID]) -> None: ...


class BaseDBRepository(IRepository[Model], ABC):
    def __init__(self, db_session: Session, model: type[Model]) -> None:
        self.session = db_session
        self._model = model

    def get_all(self) -> Iterable[Model]:
        return self.session.query(self._model).all()

    def get_one(self, item_id: int | UUID) -> Model | None:
        return self.session.query(self._model).first()

    def get_multiple(self, items_id: Iterable[int | UUID]) -> Iterable[Model]:
        return self.session.query(self._model).filter(self._model.id.in_(items_id))

    def add_one(self, item: Model) -> None:
        self.session.add(item)

    def add_many(self, items: Iterable[Model]) -> None:
        self.session.add_all(items)

    def delete_one(self, item_id: int | UUID) -> None:
        object_to_delete = self.session.query(self._model).first()
        self.session.delete(object_to_delete)

    def delete_many(self, items_id: Iterable[int | UUID]) -> None:
        for item_id in items_id:
            self.delete_one(item_id)


class PostingRepository(BaseDBRepository[Posting]): ...
