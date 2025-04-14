from dataclasses import dataclass, field
from datetime import date
from typing import Optional

from Backend_Python.app.models.animal_models.gender import Gender
from Backend_Python.app.models.animal_models.type import Type

from Backend_Python.app.models.animal_models.animal_model import AnimalModel


@dataclass
class Animal(AnimalModel):
    """patients of the clinic"""
    name: str = field(default='')
    date_of_birth: date = field(default=date.today())
    type_id: int = field(default=0)
    gender: Gender = field(default=Gender.OTHER)

    type: Optional[Type] = field(default=None)
    description: Optional[str] = field(default=None)
