import uuid
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Type, Optional
from sqlalchemy.orm import Session
from app.models.model import Model
from app.utils.api_response import ApiResponse

T = TypeVar("T", bound=Model)


class Repository(Generic[T], ABC):
    _instances: dict[type, "Repository"] = {}

    def __init__(self, session: Session, model_cls: Type[T]):
        self.session = session
        self.model_cls = model_cls

    @classmethod
    def instance(cls, session: Session) -> "Repository":
        if cls not in cls._instances:
            cls._instances[cls] = cls(session)
        else:
            cls._instances[cls].session = session
        return cls._instances[cls]

    def create(self, entity: T) -> ApiResponse:
        if not isinstance(entity, self.model_cls):
            raise Exception(f"Wrong service. Entity must be {self.model_cls.__name__}, got {type(entity).__name__}")

        entity.identifier = uuid.uuid4().hex

        if not self.validate(entity):
            raise Exception("VALIDATOR_ERROR")

        self.session.add(entity)
        self.session.commit()
        return ApiResponse(f"{self.model_cls.__name__} was created", True, entity)

    def update(self, entity: T) -> ApiResponse:
        if not isinstance(entity, self.model_cls):
            raise Exception(f"Wrong service. Entity must be {self.model_cls.__name__}, got {type(entity).__name__}")

        if not self.validate(entity):
            raise Exception("VALIDATOR_ERROR")

        existing = self.get_by("identifier", entity.identifier)
        if existing is None:
            raise Exception("Entity not found")

        entity.id = existing.id  # Zachowaj ID
        self.session.merge(entity)
        self.session.commit()
        return ApiResponse(f"{self.model_cls.__name__} was updated", True, entity)

    def delete(self, entity: T) -> ApiResponse:
        if entity is None:
            raise Exception("Entity cannot be None")

        existing = self.get_by("identifier", entity.identifier)
        if existing is None:
            raise Exception("Entity not found")

        self.set_deleted(existing)
        self.session.commit()
        return ApiResponse(f"{self.model_cls.__name__} was deleted", True, existing)

    def get_by(self, field: str, value) -> Optional[T]:
        attr = getattr(self.model_cls, field, None)
        if not attr:
            raise Exception(f"Model {self.model_cls.__name__} has no field '{field}'")
        return self.session.query(self.model_cls).filter(attr == value).first()

    def set_deleted(self, entity: T):
        if hasattr(entity, "is_deleted"):
            entity.is_deleted = True
        else:
            self.session.delete(entity)

    @abstractmethod
    def validate(self, entity: T) -> bool:
        pass
