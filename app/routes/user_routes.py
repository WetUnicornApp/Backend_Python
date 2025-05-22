from flask import Blueprint, request
from sqlalchemy.orm import Session
from pydantic import ValidationError

from app.models.user_models.user import User
from app.repositories.user_repositories.user_repository import UserRepository
from app.schemas.user_schemas.register_schema import RegisterSchema
from app.services.service import Service
from app.utils.api_response import ApiResponse

user_bp = Blueprint('user', __name__)


@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    service = Service(User, RegisterSchema, UserRepository)
    response = service.create(data)
    return response.return_response(), 201 if response.success else 400


@user_bp.route('/login', methods=['POST'])
def login():
    # data = LoginSchema.convert_to_schema(request.get_json())
    data = {'id': 1, "first_name": "Anna", "last_name": "Kowalska", "email": "anna.kowalska@email.pl"}
    # TEMP DATA
    return ApiResponse('OK', True, data).return_response(), 201
