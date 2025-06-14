
from flask import Blueprint, request

from app.models.animal_models.animal import Animal
from app.models.animal_models.gender import Gender
from app.models.animal_models.type import Type
from app.models.owner_models.owner import Owner
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


@pet_bp.route('/edit/<int:animal_id>', methods=['put'])
def edit(animal_id):
    data = request.get_json()
    db = SessionLocal()
    animal_repo = AnimalRepository(db)
    owner_repo = OwnerRepository(db)

    animal = animal_repo.get_by('id', animal_id)
    if not animal:
        return ApiResponse({"error": "Animal not found"}, success=False).return_response(), 404

    if "owner_id" in data:
        new_owner = owner_repo.get_by('id', data["owner_id"])
        if not new_owner:
            return ApiResponse({"error": "New owner not found"}, success=False).return_response(), 404
        animal.owner_id = data["owner_id"]

    for key, value in data.items():
        if key not in ['id', 'owner_id'] and hasattr(animal, key):
            setattr(animal, key, value)

    try:
        db.commit()
        db.refresh(animal)
        return ApiResponse(animal.to_dict(), success=True).return_response(), 200
    except Exception as e:
        db.rollback()
        return ApiResponse({"error": str(e)}, success=False).return_response(), 500


@pet_bp.route('/delete/<int:animal_id>', methods=['DELETE'])
def delete(animal_id):
    db = SessionLocal()
    repo = AnimalRepository(db)

    animal = repo.session.query(Animal).filter_by(id=animal_id).first()

    if not animal:
        return ApiResponse("Animal not found", False, {}).return_response(), 404

    response = repo.delete(animal)
    return response.return_response(), 200



@pet_bp.route('/gender-list', methods=['GET'])
def gender_list():
    return ApiResponse('OK', True, {}).return_response(), 201


@pet_bp.route('/type-list', methods=['GET'])
def type_list():
    return ApiResponse('OK', True, {}).return_response(), 201


@pet_bp.route('/list', methods=['GET'])
def list():
    db = SessionLocal()
    repo = AnimalRepository(db)
    animal = repo.session.query(Animal).all()

    result = []

    for an in animal:
        owner = db.query(Owner).filter_by(id=an.owner_id).first()
        result.append({
            "id": an.id,
            "name": an.name,
            "description": an.description,
            "date_of_birth":an.date_of_birth,
            "gender": an.gender,
            "type": an.type,
            "owner": owner.id,
        })
    return ApiResponse("Success", True, result).return_response(), 200

@pet_bp.route('/information/<int:animal_id>', methods=['GET'])
def get_animal(animal_id):
    db = SessionLocal()
    repo = AnimalRepository(db)

    animal = repo.session.query(Animal).filter_by(id=animal_id).first()

    if not animal:
        return ApiResponse("Animal not found", False, {}).return_response(), 404

    owner = db.query(Owner).filter_by(id=animal.owner_id).first()

    result = {
        "id": animal.id,
        "name": animal.name,
        "description": animal.description,
        "date_of_birth": animal.date_of_birth,
        "gender": animal.gender,
        "type": animal.type,
        "owner": owner.id

    }

    return ApiResponse("Success", True, result).return_response(), 200
