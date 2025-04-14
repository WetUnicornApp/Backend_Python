from dataclasses import field

from attr import dataclass

from Backend_Python.app.models.animal_models.animal import Animal
from Backend_Python.app.models.visit_models.visit import Visit
from Backend_Python.app.models.visit_models.visit_model import VisitModel


@dataclass
class VisitAnimal(VisitModel):
    """
    a class combining a visit with an animal
    """
    visit_id: int = field(default=0)
    animal_id: int = field(default=0)

    visit: Visit = field(default=None)
    animal: Animal = field(default=None)
