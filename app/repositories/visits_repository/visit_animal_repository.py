from flask_sqlalchemy.session import Session

from app.models.visit_models.visit_animal import VisitAnimal
from app.repositories.animal_repository import AnimalRepository
from app.repositories.repository import Repository, T


class VisitAnimalRepository(Repository[VisitAnimal]):
    def __init__(self, session: Session):
        super().__init__(session, VisitAnimal)

    def validate(self, entity: T) -> bool:
        return True