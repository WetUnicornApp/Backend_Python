from flask import Blueprint, request, jsonify

from app.schemas.user_schemas.register_schema import RegisterSchema
from app.utils.api_response import ApiResponse

#from Backend_Python.app.schemas.user_schemas.login_schema import LoginSchema
#from Backend_Python.app.schemas.user_schemas.register_schema import RegisterSchema
#from Backend_Python.app.utils.api_response import ApiResponse

user_bp = Blueprint('user', __name__)


@user_bp.route('/register', methods=['POST'])
def register():
    data = RegisterSchema.convert_to_schema(request.get_json())
    return ApiResponse('OK', True, data).return_response(), 201


@user_bp.route('/login', methods=['POST'])
def login():
    # data = LoginSchema.convert_to_schema(request.get_json())
    data = {'id': 1, "first_name": "Anna", "last_name": "Kowalska", "email": "anna.kowalska@email.pl"}
    # TEMP DATA
    return ApiResponse('OK', True, data).return_response(), 201
