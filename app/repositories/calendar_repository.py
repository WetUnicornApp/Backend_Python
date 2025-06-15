from flask_sqlalchemy.session import Session

from app.models.calendar_models.calendar import Calendar
from app.repositories.repository import Repository, T


class CalenderRepository(Repository[Calendar]):
    def __init__(self, session: Session):
        super().__init__(session, Calendar)

    def validate(self, entity: T) -> bool:
        return True