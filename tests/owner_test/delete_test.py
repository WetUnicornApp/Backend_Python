import pytest
import pytest
from unittest.mock import patch, MagicMock
from app.models.owner_models.owner import Owner
from app.models.user_models.user import User
from app.routes.owner_routes import owner_bp
from flask import Flask

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(owner_bp)
    app.config['TESTING'] = True
    return app.test_client()
#TEST ID: TOD1
@patch('app.routes.owner_routes.OwnerRepository')
@patch('app.routes.owner_routes.UserRepository')
@patch('app.routes.owner_routes.SessionLocal')
def test_delete_owner_success(mock_session_local, mock_user_repo_class, mock_owner_repo_class, client):
    mock_owner_repo = MagicMock()
    mock_owner_repo.session.query().filter_by().first.return_value = Owner(id=1, user_id=1)
    mock_owner_repo_class.return_value = mock_owner_repo

    mock_user_repo = MagicMock()
    mock_user_repo.session.query().filter_by().first.return_value = User(id=1, email="Bożenka@wp.pl")
    mock_user_repo_class.return_value = mock_user_repo

    response = client.delete('/delete/1')

    assert response.status_code == 201
    assert response.get_json()['success'] is True

#TEST ID:TOD2
@patch('app.routes.owner_routes.OwnerRepository')
@patch('app.routes.owner_routes.SessionLocal')
def test_delete_owner_not_found(mock_session_local, mock_owner_repo_class, client):
    mock_owner_repo = MagicMock()
    mock_owner_repo.session.query().filter_by().first.return_value = None
    mock_owner_repo_class.return_value = mock_owner_repo

    response = client.delete('/delete/999')

    assert response.status_code == 404
    assert response.get_json()['message'] == 'OWNER_NOT_FOUND'