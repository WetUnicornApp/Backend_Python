from flask_sqlalchemy.session import Session

from app.models.visit_models.visit_employee import VisitEmployee
from app.schemas.schema import Schema


class VisitEmployeeSchema(Schema):
    visit_id : int
    employee_id : int