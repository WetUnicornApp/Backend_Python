from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from sqlalchemy import Column, Integer, String, Date, Enum as PgEnum, ForeignKey, Text
from app.models.animal_models.gender import Gender
from app.models.animal_models.type import Type
from sqlalchemy.orm import relationship
from app.models.animal_models.animal_model import AnimalModel



class Animal(AnimalModel):
    __tablename__ = 'animal'
    name = Column(String(100), default='')
    date_of_birth = Column(Date, default=date.today)
    type_id = Column(Integer, ForeignKey('types.id'), nullable=False)
    gender = Column(PgEnum(Gender), default=Gender.OTHER)
    description = Column(Text, nullable=True)

    type = relationship("Type", backref="animals")
