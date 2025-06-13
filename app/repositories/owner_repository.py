from flask_sqlalchemy.session import Session

from app.models.owner_models.owner import Owner
from app.repositories.repository import Repository, T


class OwnerRepository(Repository[Owner]):
    def __init__(self, session: Session):
        super().__init__(session, Owner)


    def validate(self, entity: T) -> bool:
        return True