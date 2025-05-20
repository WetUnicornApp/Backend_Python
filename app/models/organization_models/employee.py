from dataclasses import dataclass
from typing import Optional
from app.models.organization_models.organization_model import OrganizationModel

from app.models.user_models.user import User


@dataclass
class Employee(OrganizationModel):
    user_id: int = 0  #
    user: Optional[User] = None
