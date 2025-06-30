import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from app.routes.organization_routes import organization_bp
from app.utils.api_response import ApiResponse

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(organization_bp)
    app.config['TESTING'] = True
    return app.test_client()
#TEST ID: TCO1
@patch('app.routes.organization_routes.OrganisationRepository')
@patch('app.routes.organization_routes.Service')
def test_create_organization_success(mock_service_class, mock_repo_class, client):
    mock_repo = MagicMock()
    mock_repo.get_by.return_value = None
    mock_repo_class.instance.return_value = mock_repo

    mock_service = MagicMock()
    mock_service.create.return_value = {"id": 1, "name": "uper organizacja"}
    mock_service_class.return_value = mock_service

    response = client.post('/create', json={"name": "uper organizacja"})
    assert response.status_code == 200
    assert response.get_json()['success'] is True
#TEST ID: TCO2
@patch('app.routes.organization_routes.OrganisationRepository')
def test_create_organization_name_conflict(mock_repo_class, client):
    mock_repo = MagicMock()
    mock_repo.get_by.return_value = True
    mock_repo_class.instance.return_value = mock_repo

    response = client.post('/create', json={"name": "uper organizacja"})
    assert response.status_code == 400
    assert response.get_json()['message'] == 'Name is already in use'
