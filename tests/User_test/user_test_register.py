import pytest
from unittest.mock import MagicMock, patch
from flask import Flask, json

from app.routes.user_routes import user_bp

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(user_bp)
    app.config['TESTING'] = True
    return app.test_client()

#TEST ID : TUR1
@patch('app.routes.user_routes.SessionLocal')
@patch('app.routes.user_routes.UserRepository')
def test_register_email_exists(mock_repo_class, mock_session, client):
    mock_repo = MagicMock()
    mock_repo.get_by.return_value = True
    mock_repo_class.instance.return_value = mock_repo

    payload = {"email": "iza@wp.pl"}
    response = client.post('/register', json=payload)

    assert response.status_code == 400
    assert response.json['message'] == 'EMAIL_ALREADY_REGISTER'

#TEST ID : TUR2
@patch('app.routes.user_routes.Service')
@patch('app.routes.user_routes.UserRepository')
@patch('app.routes.user_routes.SessionLocal')
def test_register_success(mock_session, mock_repo_class, mock_service_class, client):
    mock_repo = MagicMock()
    mock_repo.get_by.return_value = None
    mock_repo_class.instance.return_value = mock_repo

    mock_response = MagicMock()
    mock_response.success = True
    mock_response.return_response.return_value = {"message": "OK", "success": True}

    mock_service = MagicMock()
    mock_service.create.return_value = mock_response
    mock_service_class.return_value = mock_service

    payload = {"email": "test@example.com"}
    response = client.post('/register', json=payload)

    assert response.status_code == 201
    assert response.json['success'] is True

# TEST ID : TUR3
@patch('app.routes.user_routes.Service')
@patch('app.routes.user_routes.UserRepository')
@patch('app.routes.user_routes.SessionLocal')
def test_register_fail(mock_session, mock_repo_class, mock_service_class, client):
    mock_repo = MagicMock()
    mock_repo.get_by.return_value = None
    mock_repo_class.instance.return_value = mock_repo

    mock_response = MagicMock()
    mock_response.success = False
    mock_response.return_response.return_value = {"message": "ERROR", "success": False}

    mock_service = MagicMock()
    mock_service.create.return_value = mock_response
    mock_service_class.return_value = mock_service

    payload = {"email": "invalid"}
    response = client.post('/register', json=payload)

    assert response.status_code == 400
    assert response.json['success'] is False


