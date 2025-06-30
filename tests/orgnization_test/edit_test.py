import pytest
from unittest.mock import patch, MagicMock

from flask import Flask

from app.models.organization_models.organization_model import OrganizationModel
from app.utils.api_response import ApiResponse
from app.routes.organization_routes import organization_bp
@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(organization_bp)
    app.config['TESTING'] = True
    return app.test_client()

@pytest.fixture
def organization_instance():
    org = OrganizationModel(id=1, name="Old Org", address="Old Address")
    org.to_dict = lambda: {"id": org.id, "name": org.name, "address": org.address}
    return org

#TEST ID:TORE1
@patch('app.routes.organization_routes.OrganisationRepository')
@patch('app.routes.organization_routes.SessionLocal')
def test_edit_organization_success(mock_session_local, mock_repo_class, client, organization_instance):
    mock_repo = MagicMock()
    mock_repo.get_by.return_value = organization_instance
    mock_repo_class.instance.return_value = mock_repo

    response = client.put(
        '/edit/1',
        json={"name": "sUPER NOWA ORGANIZACJA", "address": "POLNA15"}
    )

    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["success"] is True
    assert json_data["data"]["name"] == "sUPER NOWA ORGANIZACJA"
    assert json_data["data"]["address"] == "POLNA15"

#TEST ID:TORE2
@patch('app.routes.organization_routes.OrganisationRepository')
@patch('app.routes.organization_routes.SessionLocal')
def test_edit_organization_not_found(mock_session_local, mock_repo_class, client):
    mock_repo = MagicMock()
    mock_repo.get_by.return_value = None
    mock_repo_class.instance.return_value = mock_repo

    response = client.put(
        '/edit/999',
        json={"name": "Psy i koty"}
    )

    assert response.status_code == 404
    assert response.get_json()["message"] == "ORGANIZATION_NOT_FOUND"
