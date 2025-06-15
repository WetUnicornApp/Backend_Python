from dataclasses import dataclass, field

from sqlalchemy import Column, Integer, ForeignKey

from app.models.organization_models.employee import Employee
from app.models.visit_models.visit import Visit
from app.models.visit_models.visit_model import VisitModel



class VisitEmployee(VisitModel):
    __tablename__ = "visit_employees"

    visit_id = Column(Integer, ForeignKey("visits.id"))
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True)

    def to_dict(self):
        return {
            "visit_id": self.visit_id,
            "employee_id": self.employee_id,
        }
