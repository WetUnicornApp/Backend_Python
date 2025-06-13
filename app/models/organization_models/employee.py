from dataclasses import dataclass

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.models.model import Model  #a



@dataclass
class Employee(Model):
    __tablename__ = "employees"
    user_id: int = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="employees")
    organization_id = Column(Integer, ForeignKey('organization.id'))
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "organization_id": self.organization_id
        }

    pass



