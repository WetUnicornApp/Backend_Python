import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, json
from app.routes.user_routes import user_bp

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(user_bp)
    app.config['TESTING'] = True
    return app.test_client()
#TEST ID:TUL1
def test_login_missing_data(client):
    response = client.post('/login', json={})
    assert response.status_code == 400
    assert response.json['message'] == "Missing data"
    assert response.json['success'] is False
#TEST ID:TUL2
@patch('app.routes.user_routes.UserService')
def test_login_success(mock_user_service, client):
    mock_response = MagicMock()
    mock_response.success = True
    mock_response.return_response.return_value = {"message": "Login successful", "success": True}
    mock_user_service.authenticate.return_value = mock_response

    payload = {"email": "user@example.com", "password": "correctpass"}
    response = client.post('/login', json=payload)

    assert response.status_code == 200
    assert response.json['success'] is True
#TEST ID:TUL3
@patch('app.routes.user_routes.UserService')
def test_login_fail(mock_user_service, client):
    mock_response = MagicMock()
    mock_response.success = False
    mock_response.return_response.return_value = {"message": "Invalid credentials", "success": False}
    mock_user_service.authenticate.return_value = mock_response

    payload = {"email": "user@example.com", "password": "wrongpass"}
    response = client.post('/login', json=payload)

    assert response.status_code == 400
    assert response.json['success'] is False
