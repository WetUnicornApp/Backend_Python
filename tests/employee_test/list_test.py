from types import SimpleNamespace

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from app.routes.employee_routes import employee_bp
from app.models.organization_models.employee import Employee
from app.models.user_models.user import User
from app.models.organization_models.organization_model import OrganizationModel


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(employee_bp)
    app.config['TESTING'] = True
    return app.test_client()


#TEST ID : TEL1
@patch('app.routes.employee_routes.SessionLocal')
def test_view_employee_success(mock_session_local, client):
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db

    emp = MagicMock(spec=Employee)
    emp.id = 1
    emp.user_id = 10
    emp.organization_id = 100

    user = MagicMock(spec=User)
    user.email = "user@example.com"
    user.first_name = "John"
    user.last_name = "Doe"

    org = MagicMock(spec=OrganizationModel)
    org.name = "TestOrg"
    org.id = 100

    mock_db.query.return_value.filter_by.return_value.first.side_effect = lambda: emp

    def query_side_effect(model):
        q = MagicMock()
        if model == Employee:
            q.filter_by.return_value.first.return_value = emp
        elif model == User:
            q.filter_by.return_value.first.return_value = user
        elif model == OrganizationModel:
            q.filter_by.return_value.first.return_value = org
        else:
            q.filter_by.return_value.first.return_value = None
        return q
    mock_db.query.side_effect = query_side_effect

    response = client.get('/view/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['email'] == "user@example.com"
    assert data['data']['organization'] == "TestOrg"


#TEST ID : TEL2
@patch('app.routes.employee_routes.SessionLocal')
def test_view_employee_not_found(mock_session_local, client):
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db

    mock_db.query.return_value.filter_by.return_value.first.return_value = None

    response = client.get('/view/999')
    assert response.status_code == 404
    data = response.get_json()
    assert data['success'] is False
    assert data['message'] == "EMPLOYEE_NOT_FOUND"
