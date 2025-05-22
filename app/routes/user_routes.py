from flask import Blueprint, request
from sqlalchemy.orm import Session
from pydantic import ValidationError

from app.models.user_models.user import User
from app.repositories.user_repositories.user_repository import UserRepository
from app.schemas.user_schemas.register_schema import RegisterSchema
from app.utils.api_response import ApiResponse
from config.database import SessionLocal


user_bp = Blueprint('user', __name__)


@user_bp.route('/register', methods=['POST'])
def register():
    try:
        data = {'first_name': 'Anna', 'last_name': 'Kowalska', 'email': 'a.kowalska@wp.pl', 'password': 'Haslo123',
             'repeat_password': 'Haslo123'}

        # data = request.get_json()
        schema = RegisterSchema.convert_to_schema(data)

        db: Session = SessionLocal()
        repo = UserRepository.instance(db)

        user = User(
            first_name=schema.first_name,
            last_name=schema.last_name,
            email=schema.email,
            password=schema.password
        )

        response = repo.create(user)
        return response.return_response(), 201

    except ValidationError as e:
        return ApiResponse("Validation error", False, e.errors()).return_response(), 400
    except Exception as e:
        return ApiResponse("Error during registration", False, str(e)).return_response(), 500

@user_bp.route('/login', methods=['POST'])
def login():
    # data = LoginSchema.convert_to_schema(request.get_json())
    data = {'id': 1, "first_name": "Anna", "last_name": "Kowalska", "email": "anna.kowalska@email.pl"}
    # TEMP DATA
    return ApiResponse('OK', True, data).return_response(), 201
