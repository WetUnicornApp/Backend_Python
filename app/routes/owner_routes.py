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


@owner_bp.route('/edit/<int:owner_id>', methods=['PUT'])
def edit(owner_id):
    data = request.get_json()
    db = SessionLocal()
    user_repo = UserRepository.instance(db)
    owner_repo = OwnerRepository.instance(db)
    owner = owner_repo.get_by('id', owner_id)
    if not owner:
        return ApiResponse("OWNER_NOT_FOUND", False).return_response(), 404

    user = user_repo.get_by('id', owner.user_id)
    if user is None:
        return ApiResponse("USER_NOT_FOUND", False).return_response(), 404
    new_email = data.get("email")
    if new_email and new_email != user.email:
        if user_repo.get_by("email", new_email):
            return ApiResponse("EMAIL_ALREADY_IN_USER", False).return_response(), 400
        user.email = new_email
    if "first_name" in data:
        user.first_name = data["first_name"]
    if "last_name" in data:
        user.last_name = data["last_name"]
    db.commit()

    return ApiResponse("OK", True, user.to_dict()).return_response(), 200


@owner_bp.route('/delete/<int:owner_id>', methods=['DELETE'])
def delete(owner_id):
    db = SessionLocal()
    repo = OwnerRepository(db)
    repo_user = UserRepository(db)

    owner = repo.session.query(Owner).filter_by(user_id=owner_id).first()
    if not owner:
        return ApiResponse("OWNER_NOT_FOUND", False).return_response(), 404
    user = repo_user.session.query(User).filter_by(id=owner_id).first()
    if user:
        db.delete(user)

    db.delete(owner)

    db.commit()
    return ApiResponse('OK', True, {}).return_response(), 201


@owner_bp.route('/list', methods=['GET'])
def list():
    db = SessionLocal()
    repo = OwnerRepository(db)
    owners = repo.session.query(Owner).all()
    result = []
    for owner in owners:
        user = db.query(User).filter_by(id=owner.user_id).first()
        result.append({
            'id': owner.id,
            'user_id': owner.user_id,
            "email": user.email if user else None,
            "first_name": user.first_name if user else None,
            "last_name": user.last_name if user else None
        })
    return ApiResponse("Success", True, result).return_response(), 200


@owner_bp.route('/view/<int:owner_id>', methods=['GET'])
def get_owner(owner_id):
    db = SessionLocal()
    owner_repo = OwnerRepository(db)
    user_repo = UserRepository(db)

    owner = owner_repo.session.query(Owner).filter_by(id=owner_id).first()
    if not owner:
        return ApiResponse("OWNER_NOT_FOUND", False).return_response(), 404

    user = user_repo.session.query(User).filter_by(id=owner.user_id).first()
    result = {
        "id": owner.id,
        "user_id": owner.user_id,
        "email": user.email if user else None,
        "first_name": user.first_name if user else None,
        "last_name": user.last_name if user else None
    }
    return ApiResponse("OK", True, result).return_response(), 200
