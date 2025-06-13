
from datetime import datetime

from flask import Blueprint, request, jsonify
from sqlalchemy import DateTime

from app.models.organization_models.employee import Employee
from app.models.user_models import user
from app.models.user_models.user import User
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.user_repositories.user_repository import UserRepository
from app.schemas.user_schemas.register_schema import RegisterSchema
from app.services.service import Service
from app.utils.api_response import ApiResponse
from config.database import SessionLocal

# from Backend_Python.app.utils.api_response import ApiResponse

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


@employee_bp.route('/edit', methods=['POST'])
def edit():
    """
    Expect form content
    Return 200 or 400
    """
    return ApiResponse('OK', True, {}).return_response(), 200


@employee_bp.route('/delete', methods=['DELETE'])
def delete():
    """
    Expect employee identifier
    Return 200 or 400
    """
    return ApiResponse('OK', True, {}).return_response(), 201


@employee_bp.route('/list', methods=['GET'])
def list():
    """
        Expect nothing
        Return 200 or 400
    """
    return ApiResponse('OK', True, [
        {'employee': 'Anna Kowalska', 'owner': "Jan Nowak", 'pet': "Fafik", 'name': 'name name', 'description': 'lorem',
         'date': datetime.now().strftime('%d.%m.%Y'),
         'time': datetime.now().strftime('%H:%M')}]).return_response(), 200