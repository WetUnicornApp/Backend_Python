from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from app.models.organization_models.employee import Employee
from app.repositories.repository import Repository, T


class EmployeeRepository(Repository[Employee]):

    def __init__(self, session: Session):
        super().__init__(session, Employee)


    def validate(self, entity: T) -> bool:
        return True
