from flask_sqlalchemy.session import Session

from app.models.animal_models.animal import Animal
from app.repositories.repository import Repository, T
from app.utils.api_response import ApiResponse


class AnimalRepository(Repository[Animal]):
    def __init__(self, session: Session):
        super().__init__(session, Animal)


    def validate(self, entity: T) -> bool:
        return True

