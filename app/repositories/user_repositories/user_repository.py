from sqlalchemy.orm import Session

from app.repositories.repository import Repository
from app.models.user_models.user import User


class UserRepository(Repository[User]):
    def __init__(self, session: Session):
        super().__init__(session, User)

    def validate(self, entity: User) -> bool:
        return True

