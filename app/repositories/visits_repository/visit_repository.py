from flask_sqlalchemy.session import Session

from app.models.visit_models.visit import Visit
from app.repositories.repository import Repository, T


class VisitRepository(Repository[Visit]):
    def __init__(self, session: Session):
        super().__init__(session, Visit)

    def validate(self, entity: T) -> bool:
        return True