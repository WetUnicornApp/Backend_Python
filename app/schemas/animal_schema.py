import types
from datetime import date

from app.models.animal_models.gender import Gender
from app.models.animal_models.type import Type
from app.schemas.schema import Schema


class AnimalSchema(Schema):
    name: str = ''
    date_of_birth: date = date.today()
    gender: Gender = Gender.OTHER
    description: str = ''
    type: Type = Type.CAT
    owner_id: int