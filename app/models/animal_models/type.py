from sqlalchemy import Column, Integer, String

from sqlalchemy import Column

from app.models.animal_models.animal_model import AnimalModel


class Type(AnimalModel):
    """cat, dog ..."""
    __tablename__ = 'types'
    name = Column(String(100), default='')

