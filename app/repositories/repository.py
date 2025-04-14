from dataclasses import dataclass
from typing import Type, Generic, TypeVar

from Backend_Python.app.models.model import Model

T = TypeVar("T", bound=Model)


@dataclass
class Repository(Generic[T]):
    pass
