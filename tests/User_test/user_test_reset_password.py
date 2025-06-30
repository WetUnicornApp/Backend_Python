import pytest
from unittest.mock import patch, MagicMock
from flask import Flask

from app.routes.user_routes import user_bp

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(user_bp)
    app.config['TESTING'] = True
    return app.test_client()

#TEST ID: TUC1
def test_reset_password_missing_data(client):
    response = client.post('/reset-password', json={})
    assert response.status_code == 400
    assert response.json['message'] == "Missing data"
    assert response.json['success'] is False

#TEST ID : TUC2
@patch('app.routes.user_routes.UserRepository')
@patch('app.routes.user_routes.SessionLocal')
def test_reset_password_user_not_found(mock_session, mock_repo_class, client):
    mock_repo = MagicMock()
    mock_repo.get_by.return_value = None
    mock_repo_class.instance.return_value = mock_repo
    response = client.post('/reset-password', json={"email": "missing@example.com", "new_password": "123"})
    assert response.status_code == 400
    assert response.json['message'] == "User not found"
    assert response.json['success'] is False

#TEST ID: TUC3
@patch('app.routes.user_routes.UserService')
@patch('app.routes.user_routes.UserRepository')
@patch('app.routes.user_routes.SessionLocal')
def test_reset_password_success(mock_session, mock_repo_class, mock_user_service, client):
    mock_user = MagicMock()
    mock_repo = MagicMock()
    mock_repo.get_by.return_value = mock_user
    mock_repo_class.instance.return_value = mock_repo

    mock_user_service.hash_password.return_value = "hashedpassword"

    mock_db = MagicMock()
    mock_session.return_value = mock_db

    response = client.post('/reset-password', json={"email": "user@example.com", "new_password": "newpass"})

    assert response.status_code == 200
    assert response.json['message'] == "OK"
    assert response.json['success'] is True

    assert mock_user.password == "hashedpassword"
    mock_db.commit.assert_called_once()
