import uuid
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Type, Optional

from sqlalchemy.orm import Session

from Backend_Python.app.models.model import Model
from Backend_Python.app.repositories.irepository import IRepository
from Backend_Python.app.utils.response import Response  # zakładam, że masz coś takiego

T = TypeVar("T", bound=Model)


class Repository(Generic[T], IRepository):
    def __init__(self, session: Session, model_cls: Type[T]):
        self.session = session
        self.model_cls = model_cls

    def create(self, entity: T) -> Response:
        if not isinstance(entity, self.model_cls):
            raise Exception(f"Wrong service. Entity has to be instance of {self.model_cls.__name__}, but got {type(entity).__name__}")

        entity.identifier = uuid.uuid4().hex

        if not self.validate(entity):
            raise Exception("Validator exception. Incorrect data")

        self.session.add(entity)
        self.session.commit()
        return Response(f"{self.model_cls.__name__} was created", True, entity)

    def update(self, entity: T) -> Response:
        if not isinstance(entity, self.model_cls):
            raise Exception(f"Wrong service. Entity has to be instance of {self.model_cls.__name__}, but got {type(entity).__name__}")

        if not self.validate(entity):
            raise Exception("Validator exception. Incorrect data")

        existing: Optional[T] = self.get_by("identifier", entity.identifier)
        if existing is None:
            raise Exception("Cannot find entity")

        entity.id = existing.id
        self.session.merge(entity)
        self.session.commit()
        return Response(f"{self.model_cls.__name__} was edited", True, entity)

    def delete(self, entity: T) -> Response:
        if entity is None:
            raise Exception("Entity cannot be None")

        existing: Optional[T] = self.get_by("identifier", entity.identifier)
        if existing is None:
            raise Exception("Cannot find entity")

        self.set_deleted(existing)
        self.session.commit()
        return Response(f"{self.model_cls.__name__} was deleted", True, existing)

    def get_by(self, field: str, value) -> Optional[T]:
        return self.session.query(self.model_cls).filter(getattr(self.model_cls, field) == value).first()

    def set_deleted(self, entity: T):
        if hasattr(entity, "is_deleted"):
            entity.is_deleted = True
        else:
            self.session.delete(entity)

    @abstractmethod
    def validate(self, entity: T) -> bool:
        pass
