from dataclasses import field
from typing import Optional

from attr import dataclass

from Backend_Python.app.models.visit_models.visit_model import VisitModel


@dataclass
class Visit(VisitModel):
    """
    base class for the visit, it should be referenced when
    a given object refers to the visit
    """

    calendar_id: Optional[int] = field(default=0)
    description: Optional[str] = field(default=None)
    name: Optional[str] = field(default=None)
