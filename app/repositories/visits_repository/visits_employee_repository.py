from flask_sqlalchemy.session import Session

from app.models.visit_models.visit_employee import VisitEmployee
from app.repositories.repository import Repository, T


class VisitEmployeeRepository(Repository[VisitEmployee]):
    def __init__(self, session: Session):
        super().__init__(session, VisitEmployee)

    def validate(self, entity: T) -> bool:
        return True