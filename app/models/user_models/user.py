from dataclasses import dataclass

from app.models.user_models.user_model import UserModel


@dataclass
class User(UserModel):
    first_name: str = ''
    last_name: str = ''
    email: str = ''
    password: str = ''
