
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
#TEST ID: TORD1
@patch('app.routes.organization_routes.OrganisationRepository')
@patch('app.routes.organization_routes.SessionLocal')
def test_delete_organization_success(mock_session_local, mock_repo_class, client):
    mock_repo = MagicMock()
    mock_repo.session.query().filter_by().first.return_value = MagicMock()
    mock_repo.session.delete.return_value = None
    mock_repo.session.commit.return_value = None
    mock_repo_class.return_value = mock_repo

    response = client.delete('/delete/1')
    assert response.status_code == 201
    assert response.get_json()['message'] == 'OK'
#TEST ID: TORD2
@patch('app.routes.organization_routes.OrganisationRepository')
@patch('app.routes.organization_routes.SessionLocal')
def test_delete_organization_not_found(mock_session_local, mock_repo_class, client):
    mock_repo = MagicMock()
    mock_repo.session.query().filter_by().first.return_value = None
    mock_repo_class.return_value = mock_repo

    response = client.delete('/delete/999')
    assert response.status_code == 404
    assert response.get_json()['message'] == 'ORGANIZATION_NOT_FOUND'
