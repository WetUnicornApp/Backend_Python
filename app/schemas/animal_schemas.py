from datetime import date
from typing import Optional

from app.schemas.schema import Schema
from app.models.animal_models.gender import Gender
from app.models.animal_models.type import Type

class AnimalSchema(Schema):
    name: Optional[str] = ''
    date_of_birth: Optional[date] = None
    gender: Gender
    description: Optional[str] = ''
    type: Type
    owner_id: Optional[int] = None