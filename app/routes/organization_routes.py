
from flask import Blueprint, request
from app.models.organization_models.organization_model import OrganizationModel
from app.repositories.organization_repository import OrganisationRepository
from app.schemas.organisation_schemas.organization_schema import OrganizationSchema
from app.services.service import Service
from app.utils.api_response import ApiResponse
from config.database import SessionLocal

organization_bp = Blueprint('organization', __name__)

@organization_bp.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    db = SessionLocal()
    repo = OrganisationRepository.instance(db)

    if repo.get_by('name', data['name']):
        return ApiResponse('Name is already in use',False).return_response(), 400

    service = Service(OrganizationModel,OrganizationSchema, OrganisationRepository)
    response = service.create(data)
    return ApiResponse(response,True).return_response()

@organization_bp.route('/show', methods=['GET'])
def show():
    name = request.args.get('name')
    if not name:
        return ApiResponse('Name is required',False).return_response(),400
    db = SessionLocal()
    repo = OrganisationRepository.instance(db)
    organization = repo.get_by('name', name)
    if not organization:
        return ApiResponse('Organization not found', False).return_response(), 404

    organization_data={
        'name': organization.name,
        'address': organization.address,
    }
    return ApiResponse(organization_data,True).return_response(),200


@organization_bp.route('/delete', methods=['DELETE'])
def delete():
    data = request.get_json()
    if not data or not data.get('name'):
        return ApiResponse('No name provided', False).return_response(), 400

    db = SessionLocal()
    repo = OrganisationRepository.instance(db)
    organization = repo.get_by('name', data['name'])
    if not organization:
        return ApiResponse('Organization not found', False).return_response(), 404

    repo.delete(organization)
    db.commit()

    return ApiResponse(f'Organization "{data["name"]}" deleted successfully', True).return_response(), 200

@organization_bp.route('/update', methods=['PUT'])
def update():
    data = request.get_json()
    if not data or 'name' not in data:
        return ApiResponse('No organization name provided', False).return_response(), 400

    db = SessionLocal()
    repo = OrganisationRepository.instance(db)
    organization = repo.get_by('name', data['name'])

    if not organization:
        return ApiResponse('Organization not found', False).return_response(), 404

    if 'address' in data:
        organization.address = data['address']

    if 'new_name' in data:
        organization.name = data['new_name']

    db.commit()
    return ApiResponse('Organization updated successfully', True).return_response(), 200



