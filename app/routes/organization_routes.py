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
        return ApiResponse('Name is already in use', False).return_response(), 400

    service = Service(OrganizationModel, OrganizationSchema, OrganisationRepository)
    response = service.create(data)
    return ApiResponse(response, True).return_response()



@organization_bp.route('/view/<int:organization_id>', methods=['GET'])
def get_organizations(organization_id):
    db = SessionLocal()
    org_rep = OrganisationRepository(db)

    org = org_rep.session.query(OrganizationModel).filter_by(id=organization_id).first()
    if org is None:
        return ApiResponse("ORGANIZATION_NOT_FOUND", False).return_response(), 404

    result = {
        "id": org.id,
        "name": org.name,
        "address": org.address,
    }

    return ApiResponse("OK", True, result).return_response(), 200


@organization_bp.route('/delete/<int:organization_id>', methods=['DELETE'])
def delete(organization_id):
    db = SessionLocal()
    repo = OrganisationRepository(db)

    org = repo.session.query(OrganizationModel).filter_by(id=organization_id).first()
    if not org:
        return ApiResponse("ORGANIZATION_NOT_FOUND", False).return_response(), 404
    db.delete(org)
    db.commit()
    return ApiResponse('OK', True, {}).return_response(), 201


@organization_bp.route('/edit/<int:organization_id>', methods=['PUT'])
def edit(organization_id):
    data = request.get_json()
    db = SessionLocal()
    org_rep = OrganisationRepository.instance(db)
    org = org_rep.get_by('id', organization_id)
    if not org:
        return ApiResponse("ORGANIZATION_NOT_FOUND", False).return_response(), 404

    if "name" in data:
        org.name = data["name"]
    if "address" in data:
        org.address = data["address"]
    db.commit()

    return ApiResponse("OK", True, org.to_dict()).return_response(), 200


@organization_bp.route('/list', methods=['GET'])
def organizations():
    s = request.args.get('s')
    db = SessionLocal()
    repo = OrganisationRepository(db)
    arr = repo.session.query(OrganizationModel).filter_by(is_deleted=0).all()

    result = []

    if s == '1':
        for item in arr:
            result.append({
                "value": item.id,
                "text": item.name
            })
    else:
        for org in arr:
            result.append({
                "id": org.id,
                "name": org.name,
                "address": org.address,
            })

    return ApiResponse("Success", True, result).return_response(), 200

