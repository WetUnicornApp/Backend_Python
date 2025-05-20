from dataclasses import dataclass, field

from app.models.organization_models.employee import Employee
from app.models.visit_models.visit import Visit
from app.models.visit_models.visit_model import VisitModel


@dataclass
class VisitEmployee(VisitModel):
    """
        a class combining a visit with an employee
    """

    visit_id: int = field(default=0)
    employee_id: int = field(default=0)

    visit: Visit = field(default=None)
    employee: Employee = field(default=None)
