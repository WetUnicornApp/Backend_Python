from dataclasses import dataclass, field

from Backend_Python.app.models.organization_models.employee import Employee
from Backend_Python.app.models.visit_models.visit import Visit
from Backend_Python.app.models.visit_models.visit_model import VisitModel


@dataclass
class VisitEmployee(VisitModel):
    """
        a class combining a visit with an employee
    """

    visit_id: int = field(default=0)
    employee_id: int = field(default=0)

    visit: Visit = field(default=None)
    employee: Employee = field(default=None)
