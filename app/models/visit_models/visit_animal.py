from dataclasses import field

from attr import dataclass
from sqlalchemy import Column, Integer, ForeignKey

from app.models.animal_models.animal import Animal
from app.models.visit_models.visit import Visit
from app.models.visit_models.visit_model import VisitModel



class VisitAnimal(VisitModel):
    __tablename__ = "visit_animals"
    visit_id = Column(Integer, ForeignKey("visits.id"))
    animal_id = Column(Integer, ForeignKey("animal.id"), nullable=True)

    def to_dict(self):
        return {
            "visit_id": self.visit_id,
            "animal_id": self.animal_id
        }