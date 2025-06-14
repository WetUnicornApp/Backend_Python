from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from sqlalchemy import Column, Integer, String, Date, Enum as PgEnum, ForeignKey, Text
from app.models.animal_models.gender import Gender
from app.models.animal_models.type import Type
from sqlalchemy.orm import relationship
from app.models.animal_models.animal_model import AnimalModel



class Animal(AnimalModel):
    __tablename__ = "animal"
    name = Column(String(100), default='')
    date_of_birth = Column(Date, default=date.today)
    gender = Column(PgEnum(Gender, name="gender_enum", native_enum=False), nullable=False, default=Gender.OTHER)
    description = Column(Text, nullable=True)
    type = Column(PgEnum(Type, name="animal_type_enum", native_enum=False), default=Type.CAT)
    owner_id = Column(Integer, ForeignKey("owner.id"), nullable=False)
    owner = relationship("Owner", back_populates="animals")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "date_of_birth": self.date_of_birth.isoformat() if self.date_of_birth else None,
            "gender": self.gender.value if self.gender else None,
            "description": self.description,
            "type": self.type.value if self.type else None,
            "owner": self.owner_id,
        }