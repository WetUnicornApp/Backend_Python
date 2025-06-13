
from datetime import datetime

from flask import Blueprint, request, jsonify
from sqlalchemy import DateTime

from app.models.organization_models.employee import Employee
from app.models.organization_models.organization_model import OrganizationModel
from app.models.user_models import user
from app.models.user_models.user import User
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.user_repositories.user_repository import UserRepository
from app.repositories.organization_repository import OrganisationRepository
from app.schemas.user_schemas.register_schema import RegisterSchema
from app.services.service import Service
from app.utils.api_response import ApiResponse
from config.database import SessionLocal

employee_bp = Blueprint('employee', __name__)


@employee_bp.route('/create', methods=['POST'])
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

    organization_id = data.get('organization_id')
    if not organization_id:
        return ApiResponse("Organization ID is required", False).return_response(), 400

    repo_employee = EmployeeRepository(db)
    employee = Employee(user_id=user.id,organization_id=organization_id)
    response = repo_employee.create(employee)
    if not response.success:
        return ApiResponse(response.message, False).return_response(), 400

    return ApiResponse('OK', True, {}).return_response(), 201


@employee_bp.route('/edit/<int:user_id>', methods=['PUT'])
def edit(user_id):
    data = request.get_json()
    db = SessionLocal()
    user_repo = UserRepository.instance(db)
    employee_repo = EmployeeRepository(db)
    org_repo = OrganisationRepository(db)

    user = user_repo.get_by("id", user_id)
    if not user:
        return ApiResponse("User not found", False).return_response(), 404

    new_email = data.get("email")
    if new_email and new_email != user.email:
        if user_repo.get_by("email", new_email):
            return ApiResponse("Email already in use", False).return_response(), 400
        user.email = new_email
    if "first_name" in data:
        user.first_name = data["first_name"]
    if "last_name" in data:
        user.last_name = data["last_name"]
    if "organization_id" in data:
        org = org_repo.get_by("id", data["organization_id"])
        if not org:
            return ApiResponse("Organization not found", False).return_response(), 404

        employee = employee_repo.get_by("user_id", user.id)
        if not employee:
            return ApiResponse("Employee not found", False).return_response(), 404

        employee.organization_id = data["organization_id"]

    db.commit()

    return ApiResponse("User updated successfully", True, user.to_dict()).return_response(), 200


@employee_bp.route('/delete/<int:user_id>', methods=['DELETE'])
def delete(user_id):
    db = SessionLocal()
    repo = EmployeeRepository(db)
    user_repo = UserRepository(db)

    employee = repo.session.query(Employee).filter_by(user_id=user_id).first()
    if not employee:
        return ApiResponse("Employee not found", False).return_response(), 404

    user = user_repo.session.query(User).filter_by(id=user_id).first()
    if user:
        db.delete(user)

    db.delete(employee)

    db.commit()
    return ApiResponse('OK', True, {}).return_response(), 201


@employee_bp.route('/list', methods=['GET'])
def list():
    db = SessionLocal()
    repo = EmployeeRepository(db)
    employees = repo.session.query(Employee).all()

    result = []
    for emp in employees:
        user = db.query(User).filter_by(id=emp.user_id).first()
        org = db.query(OrganizationModel).filter_by(id=emp.organization_id).first() if emp.organization_id else None

        result.append({
            "id": emp.id,
            "user_id": emp.user_id,
            "email": user.email if user else None,
            "first_name": user.first_name if user else None,
            "last_name": user.last_name if user else None,
            "organization": org.name if org else None,
        })

    return ApiResponse("Success", True, result).return_response(), 200


@employee_bp.route('/information/<int:user_id>', methods=['GET'])
def get_employee(user_id):
    db = SessionLocal()
    emp_repo = EmployeeRepository(db)
    user_repo = UserRepository(db)
    org_repo = OrganisationRepository(db)

    employee = emp_repo.session.query(Employee).filter_by(user_id=user_id).first()
    if not employee:
        return ApiResponse("Employee not found", False).return_response(), 404

    user = user_repo.session.query(User).filter_by(id=user_id).first()
    organization = None
    if employee.organization_id:
        organization = org_repo.session.query(OrganizationModel).filter_by(id=employee.organization_id).first()

    result = {
        "id": employee.id,
        "user_id": employee.user_id,
        "email": user.email if user else None,
        "first_name": user.first_name if user else None,
        "last_name": user.last_name if user else None,
        "organization": organization.name if organization else None,
    }

    return ApiResponse("OK", True, result).return_response(), 200