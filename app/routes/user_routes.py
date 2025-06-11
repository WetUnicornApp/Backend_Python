from flask import Blueprint, request

from app.models.user_models.user import User
from app.repositories.user_repositories.user_repository import UserRepository
from app.schemas.user_schemas.register_schema import RegisterSchema
from app.services.service import Service
from app.services.user_service import UserService
from app.utils.api_response import ApiResponse
from config.database import SessionLocal

user_bp = Blueprint('user', __name__)


@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    db = SessionLocal()
    repo = UserRepository.instance(db)
    if repo.get_by('email', data.get('email')):
        return ApiResponse("Email already registered", False).return_response(),400

    service = Service(User, RegisterSchema, UserRepository)
    response = service.create(data)
    return response.return_response(), 201 if response.success else 400


@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return ApiResponse("Missing data", False).return_response(), 400

    response = UserService.authenticate(data)
    return response.return_response(), 200 if response.success else 400


@user_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('new_password'):
        return ApiResponse("Missing data", False).return_response(), 400

    db = SessionLocal()
    repo = UserRepository.instance(db)
    user = repo.get_by('email', data.get('email'))
    if not user:
        return ApiResponse("User not found", False).return_response(), 400

    hashed_password = UserService.hash_password(data['new_password'])
    user.password = hashed_password
    db.commit()
    return ApiResponse('OK', True, {}).return_response(), 200
