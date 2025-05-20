from dataclasses import dataclass
from typing import Optional

from app.models.owner_models.owner_model import OwnerModel
from app.models.user_models.user import User


@dataclass
class Owner(OwnerModel):
    user_id: int = 0
    user: Optional[User] = None
