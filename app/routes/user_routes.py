from flask import Blueprint, request, jsonify

from Backend_Python.app.schemas.user_schemas.register_schema import RegisterSchema
from Backend_Python.app.utils.api_response import ApiResponse

user_bp = Blueprint('user', __name__)


@user_bp.route('/register', methods=['POST'])
def register():
    data = RegisterSchema.convert_to_schema(request.get_json())
    return ApiResponse('OK', True, data).return_response(), 201


@user_bp.route('/login', methods=['POST'])
def login():
    return "Lista użytkowników", 200
