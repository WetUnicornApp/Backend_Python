import bcrypt

from app.repositories.user_repositories.user_repository import UserRepository
from app.utils.api_response import ApiResponse
from config.database import SessionLocal


class UserService:
    def __init__(self):
        pass

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str):
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    @staticmethod
    def authenticate(json_data: dict) -> ApiResponse:
        session = SessionLocal()
        user_repo = UserRepository.instance(session)
        user = user_repo.get_by('email', json_data['email'])
        if user is None:
            return ApiResponse(success=False, message='USER_NOT_FOUND')

        if not UserService.verify_password(json_data['password'], user.password):
            return ApiResponse(success=False, message='INCORRECT_PASSWORD')

        return ApiResponse(success=True, message='OK', data=user.to_dict())
