import pytest
from unittest.mock import patch, MagicMock
from app.routes.owner_routes import owner_bp
from flask import Flask

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(owner_bp)
    app.config['TESTING'] = True
    return app.test_client()

#TEST ID: TOC1
@patch('app.routes.owner_routes.OwnerRepository')
@patch('app.routes.owner_routes.UserRepository')
@patch('app.routes.owner_routes.SessionLocal')
def test_create_owner_success(mock_session_local, mock_user_repo_class, mock_owner_repo_class, client):

    mock_user_repo = MagicMock()
    mock_owner_repo = MagicMock()

    mock_user_repo.get_by.return_value = None
    mock_user_repo_class.instance.return_value = mock_user_repo

    mock_owner_repo.create.return_value.success = True
    mock_owner_repo_class.return_value = mock_owner_repo

    response = client.post('/create', json={
        "email": "Bożena@wp.pl",
        "first_name": "Bożena",
        "last_name": "koch",
        "password": "koch123"
    })

    assert response.status_code == 201
    assert response.get_json()["success"] is True

#TEST ID: TOC2
@patch('app.routes.owner_routes.UserRepository')
@patch('app.routes.owner_routes.SessionLocal')
def test_create_owner_email_exists(mock_session_local, mock_user_repo_class, client):

    mock_user_repo = MagicMock()
    mock_user_repo.get_by.return_value = MagicMock()
    mock_user_repo_class.instance.return_value = mock_user_repo

    response = client.post('/create', json={
        "email": "Bożena@wp.pl",
        "first_name": "Bożena",
        "last_name": "koch",
        "password": "koch123"
    })

    assert response.status_code == 400
    assert response.get_json()["message"] == "Email already registered"
