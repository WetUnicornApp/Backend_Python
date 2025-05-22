from flask import Blueprint, request, jsonify
from flask_sqlalchemy.session import Session
from pydantic import ValidationError

from app.models.user_models.user import User
from app.schemas.user_schemas.register_schema import RegisterSchema
from app.utils.api_response import ApiResponse
from config.database import SessionLocal

#from Backend_Python.app.schemas.user_schemas.login_schema import LoginSchema
#from Backend_Python.app.schemas.user_schemas.register_schema import RegisterSchema
#from Backend_Python.app.utils.api_response import ApiResponse

user_bp = Blueprint('user', __name__)


@user_bp.route('/register', methods=['POST'])
def register():
    ## ! DO POPRAWY
    #data = RegisterSchema.convert_to_schema(request.get_json())
    #return ApiResponse('OK', True, data).return_response(), 201
    try:
        data = RegisterSchema(**request.get_json())
    except ValidationError as err:
        return ApiResponse(str(err), False, None).return_response(),400
    #sprawdzamy czy hasła są do siebie podobne
    if data.password != data.repeat_password:
        return ApiResponse("PASSWROD_DO_NOT_MATCH", False, None).return_response(), 400
    session = SessionLocal()
    try:
        existing_user = session.query(User).filter_by(email=data.email).first()
        if existing_user:
            return ApiResponse("EMAIL_ALREADY_REAGISTERED", False, None).return_response(), 400

        new_user = User(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            password=data.password
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        user_data = {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email,
        }
        return ApiResponse("User registered", True, user_data).return_response(), 201
    except ValidationError as e:
        return ApiResponse(str(e), False, None).return_response(), 400
    finally:
        session.close()

@user_bp.route('/login', methods=['POST'])
def login():
    # data = LoginSchema.convert_to_schema(request.get_json())
    data = {'id': 1, "first_name": "Anna", "last_name": "Kowalska", "email": "anna.kowalska@email.pl"}
    # TEMP DATA
    return ApiResponse('OK', True, data).return_response(), 201
