from app.models.user_models.user import User
from app.schemas.schema import Schema
from app.services.user_service import UserService


class RegisterSchema(Schema):
    first_name: str = ''
    last_name: str = ''
    email: str = ''
    password: str = ''
    repeat_password: str = ''

    def to_model(self) -> User:
        return User(
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            password=UserService.hash_password(self.password),
        )


