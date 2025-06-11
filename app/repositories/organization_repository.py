from flask_sqlalchemy.session import Session

from app.models.organization_models.organization_model import OrganizationModel
from app.repositories.repository import Repository, T


class OrganisationRepository(Repository[OrganizationModel]):
    def __init__(self, session: Session):
        super().__init__(session, OrganizationModel)

    def validate(self, entity: T) -> bool:
        return True