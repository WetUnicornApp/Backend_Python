from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Type

from Backend_Python.app.models.model import Model

T = TypeVar("T", bound=Model)


class IRepository(Generic[T], ABC):
    """
    Generic abstract repository interface for working with models of type T.
    """

    def __init__(self, session):
        self.session = session

    @classmethod
    def get_repo(cls: Type['IRepository[T]'], session) -> 'IRepository[T]':
        """
        Return a new instance of this repository with the given session.
        """
        return cls(session)

    @abstractmethod
    def validate(self, model: T) -> bool:
        """
        Validate the given model before performing operations.
        """
        pass

    @abstractmethod
    def create(self, model: T) -> T:
        """
        Create and persist a new model instance.
        """
        pass

    @abstractmethod
    def delete(self, model: T) -> T:
        """
        Mark the model as deleted or remove it from storage.
        """
        pass

    @abstractmethod
    def update(self, model: T) -> T:
        """
        Update the model in storage.
        """
        pass
