from flask import Blueprint, request, jsonify

from app.models.owner_models.owner import Owner
from app.models.user_models.user import User
from app.repositories.owner_repository import OwnerRepository
from app.repositories.user_repositories.user_repository import UserRepository
from app.schemas.user_schemas.register_schema import RegisterSchema
from app.services.service import Service
from app.utils.api_response import ApiResponse
from config.database import SessionLocal

# from Backend_Python.app.utils.api_response import ApiResponse

owner_bp = Blueprint('owner', __name__)


@owner_bp.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    db = SessionLocal()

    repo_user = UserRepository.instance(db)
    if repo_user.get_by('email', data.get('email')):
        return ApiResponse("Email already registered", False).return_response(), 400

    service = Service(User, RegisterSchema, UserRepository)
    response = service.create(data)
    if not response.success:
        return ApiResponse(response.message, False).return_response(), 400

    user = response.data

    repo_owner = OwnerRepository(db)
    owner = Owner(user_id=user.id)
    response = repo_owner.create(owner)
    if not response.success:
        return ApiResponse(response.message, False).return_response(), 400

    return ApiResponse('OK', True, {}).return_response(), 201


@owner_bp.route('/edit', methods=['POST'])
def edit():
    """
    Expect form content
    Return 200 or 400
    """
    return ApiResponse('OK', True, {}).return_response(), 201


@owner_bp.route('/delete', methods=['DELETE'])
def delete():
    """
    Expect owner identifier
    Return 200 or error
    """
    return ApiResponse('OK', True, {}).return_response(), 201


@owner_bp.route('/list', methods=['GET'])
def list():
    """
    Expect nothing
    Return 201 or 400
    """
    return ApiResponse('OK', True, {}).return_response(), 201
