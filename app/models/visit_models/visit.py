from dataclasses import field

from typing import Optional, Text
from app.models.calendar_models.calendar import Calendar
from attr import dataclass
from sqlalchemy import Column, Integer, ForeignKey,String

from app.models.visit_models.visit_model import VisitModel



class Visit(VisitModel):
    __tablename__ = "visits"

    name = Column(String(100), default='', nullable=True)
    description = Column(String(100), nullable=True)
    calendar_id = Column(Integer, ForeignKey("calendar.id"), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "calendar_id": self.calendar_id
        }