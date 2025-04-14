from dataclasses import dataclass, field
from datetime import datetime
import uuid
from typing import TypeVar, Type
from Backend_Python.app.repositories.repository import Repository


@dataclass
class Model:
    id: int = 0
    datetime_created: datetime = field(default_factory=datetime.utcnow)
    is_deleted: bool = False

    def __eq__(self, other):
        if isinstance(other, Model):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)
