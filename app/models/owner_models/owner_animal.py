from typing import Optional
from attr import dataclass, field

from app.models.animal_models.animal import Animal
from app.models.owner_models.owner import Owner
from app.models.owner_models.owner_model import OwnerModel


@dataclass
class OwnerAnimal(OwnerModel):
    """
    A model representing the relationship between the owner and the animal.

    In the future, it can be expanded with additional information, e.g. type of relationship,
    date of acquisition, owner permissions, etc.
    """

    animal_id: int = field(default=0)
    owner_id: int = field(default=0)

    animal: Optional[Animal] = field(default=None)
    owner: Optional[Owner] = field(default=None)
