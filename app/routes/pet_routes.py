
from flask import Blueprint, request

from app.models.animal_models.animal import Animal
from app.models.animal_models.gender import Gender
from app.models.animal_models.type import Type
from app.repositories.animal_repository import AnimalRepository
from app.repositories.owner_repository import OwnerRepository
from app.schemas.animal_schemas import AnimalSchema
from app.services.service import Service
from app.utils.api_response import ApiResponse
from config.database import SessionLocal


pet_bp = Blueprint('pet', __name__)


from flask import request, jsonify
from datetime import datetime

from flask import Blueprint, request, jsonify
from datetime import datetime

from app.models.animal_models.animal import Animal
from app.models.animal_models.gender import Gender
from app.models.animal_models.type import Type
from config.database import SessionLocal

pet_bp = Blueprint('pet', __name__)


@pet_bp.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    db = SessionLocal()
    repo = OwnerRepository(db)
    owner = repo.get_by('id', data.get('owner_id'))
    if not owner:
        return ApiResponse({"error": "Owner not found"}, success=False).return_response(), 404

    service = Service(Animal, AnimalSchema, AnimalRepository)

    response = service.create(data)
    status_code = 201 if response.success else 400
    return response.return_response(), status_code


@pet_bp.route('/edit', methods=['POST'])
def edit():
    return ApiResponse('OK', True, {}).return_response(), 201


@pet_bp.route('/delete', methods=['GET'])
def delete():
    return ApiResponse('OK', True, {}).return_response(), 201


@pet_bp.route('/gender-list', methods=['GET'])
def gender_list():
    return ApiResponse('OK', True, {}).return_response(), 201


@pet_bp.route('/type-list', methods=['GET'])
def type_list():
    return ApiResponse('OK', True, {}).return_response(), 201


@pet_bp.route('/list', methods=['GET'])
def list():
    if request.args.get('simple'):
        return ApiResponse('OK', True, [{1: 'Fafik'}, {2: 'Petunia'}]).return_response(), 200
    else:
        return ApiResponse('OK', True, {}).return_response(), 200
