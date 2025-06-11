from dataclasses import dataclass
from typing import Optional

from sqlalchemy import Integer, Column

from app.models.organization_models.organization_model import OrganizationModel

from app.models.user_models.user import User


@dataclass
class Employee(OrganizationModel):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    user_id: int = 0  #
    user: Optional[User] = None
