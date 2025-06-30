
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from app.routes.organization_routes import organization_bp

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(organization_bp)
    app.config['TESTING'] = True
    return app.test_client()
#TEST ID:TOV1
@patch('app.routes.organization_routes.OrganisationRepository')
@patch('app.routes.organization_routes.SessionLocal')
def test_view_organization_success(mock_session_local, mock_repo_class, client):
    mock_org = MagicMock()
    mock_org.id = 1
    mock_org.name = "ORGANIZACJA NR 15"
    mock_org.address = "kONWALIOWA 15"

    mock_repo = MagicMock()
    mock_repo.session.query().filter_by().first.return_value = mock_org
    mock_repo_class.return_value = mock_repo

    response = client.get('/view/1')
    data = response.get_json()
    assert response.status_code == 200
    assert data['data']['id'] == 1
    assert data['data']['name'] == "ORGANIZACJA NR 15"
# TEST ID: TOV2
@patch('app.routes.organization_routes.OrganisationRepository')
@patch('app.routes.organization_routes.SessionLocal')
def test_view_organization_not_found(mock_session_local, mock_repo_class, client):
    mock_repo = MagicMock()
    mock_repo.session.query().filter_by().first.return_value = None
    mock_repo_class.return_value = mock_repo

    response = client.get('/view/999')

    assert response.status_code == 404
    assert response.get_json()["message"] == "ORGANIZATION_NOT_FOUND"
