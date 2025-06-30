import pytest
from unittest.mock import patch, MagicMock

from flask import Flask

from app.models.organization_models.employee import Employee
from app.models.user_models.user import User
from app.models.organization_models.organization_model import OrganizationModel
from app.routes.employee_routes import employee_bp
@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(employee_bp)
    app.config['TESTING'] = True
    return app.test_client()

@pytest.fixture
def employee_instance():
    return Employee(id=1, user_id=1, organization_id=10, is_deleted=0)



@pytest.fixture
def organization_instance():
    return OrganizationModel(id=10, name="SuperOrganizacja")

#TEST ID : TCEM1

@patch('app.routes.employee_routes.UserRepository')
@patch('app.routes.employee_routes.SessionLocal')
@patch('app.routes.employee_routes.EmployeeRepository')
@patch('app.routes.employee_routes.Service')
def test_create_success(mock_service_class, mock_employee_repo_class, mock_session_local, mock_user_repo_class, client):
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db

    mock_user_repo = MagicMock()
    mock_user_repo.get_by.return_value = None
    mock_user_repo_class.instance.return_value = mock_user_repo

    mock_service = MagicMock()
    mock_service.create.return_value.success = True
    mock_service.create.return_value.data = User(id=1)
    mock_service_class.return_value = mock_service

    mock_employee_repo = MagicMock()
    mock_employee_repo.create.return_value.success = True
    mock_employee_repo_class.return_value = mock_employee_repo

    response = client.post('/create', json={
        "email": "kOCHA@example.com",
        "first_name": "Marzena",
        "last_name": "KOCH",
        "password": "pass123",
        "organization_id": 10
    })

    assert response.status_code == 201
    assert response.get_json()['success'] is True

#TEST ID : TCEM2
@patch('app.routes.employee_routes.UserRepository')
@patch('app.routes.employee_routes.SessionLocal')
@patch('app.routes.employee_routes.EmployeeRepository')
@patch('app.routes.employee_routes.Service')
def test_create_missing_organization_id(mock_service_class, mock_employee_repo_class, mock_session_local, mock_user_repo_class, client):
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db

    mock_user_repo = MagicMock()
    mock_user_repo.get_by.return_value = None
    mock_user_repo_class.instance.return_value = mock_user_repo

    mock_service = MagicMock()
    mock_service.create.return_value.success = True
    mock_service.create.return_value.data = User(id=1)
    mock_service_class.return_value = mock_service

    mock_employee_repo = MagicMock()
    mock_employee_repo.create.return_value.success = True
    mock_employee_repo_class.return_value = mock_employee_repo
    response = client.post('/create', json={
        "email": "kOCHA@example.com",
        "first_name": "Marzena",
        "last_name": "KOCH",
        "password": "pass123",

    })
    assert response.status_code == 400
    assert response.get_json()['message'] == "ORGANIZATION_ID_REQUIRED"

#TEST ID : TCEM3
@patch('app.routes.employee_routes.UserRepository')
@patch('app.routes.employee_routes.SessionLocal')
def test_create_email_already_registered(mock_session_local, mock_user_repo_class, client):
    mock_user_repo = MagicMock()
    mock_user_repo.get_by.return_value = User(id=1)
    mock_user_repo_class.instance.return_value = mock_user_repo

    response = client.post('/create', json={"email": "kOCHA@example.com", "organization_id": 1})

    assert response.status_code == 400
    assert response.get_json()['message'] == "EMAIL_ALREADY_REGISTERED"

