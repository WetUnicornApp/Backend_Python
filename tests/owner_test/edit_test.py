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
@pytest.fixture
def owner_instance():
    return Owner(id=1, user_id=1)

@pytest.fixture
def user_instance():
    user = User(id=1, email="old@WP.com", first_name="Waleria", last_name="Nowak")
    user.to_dict = lambda: {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name
    }
    return user
#TEST ID:TOE1
@patch('app.routes.owner_routes.UserRepository')
@patch('app.routes.owner_routes.OwnerRepository')
@patch('app.routes.owner_routes.SessionLocal')
def test_edit_owner_success(mock_session_local, mock_owner_repo_class, mock_user_repo_class, client, owner_instance, user_instance):
    mock_owner_repo = MagicMock()
    mock_owner_repo.get_by.return_value = owner_instance
    mock_owner_repo_class.instance.return_value = mock_owner_repo

    mock_user_repo = MagicMock()
    mock_user_repo.get_by.side_effect = lambda key, val=None: user_instance if key == 'id' else None
    mock_user_repo_class.instance.return_value = mock_user_repo

    response = client.put('/edit/1', json={"email": "NOWY@example.com", "first_name": "Elżbieta"})

    assert response.status_code == 200
    assert response.get_json()['data']['email'] == 'NOWY@example.com'

#TEST ID:TOE2
@patch('app.routes.owner_routes.OwnerRepository')
@patch('app.routes.owner_routes.SessionLocal')
def test_edit_owner_not_found(mock_session_local, mock_owner_repo_class, client):
    mock_owner_repo = MagicMock()
    mock_owner_repo.get_by.return_value = None
    mock_owner_repo_class.instance.return_value = mock_owner_repo

    response = client.put('/edit/999', json={"first_name": "Zenek"})
    assert response.status_code == 404
    assert response.get_json()['message'] == 'OWNER_NOT_FOUND'

#TEST ID: TOE3
@patch('app.routes.owner_routes.UserRepository')
@patch('app.routes.owner_routes.OwnerRepository')
@patch('app.routes.owner_routes.SessionLocal')
def test_edit_owner_email_already_used(mock_session_local, mock_owner_repo_class, mock_user_repo_class, client, owner_instance, user_instance):
    mock_owner_repo = MagicMock()
    mock_owner_repo.get_by.return_value = owner_instance
    mock_owner_repo_class.instance.return_value = mock_owner_repo

    mock_user_repo = MagicMock()
    def get_by(key, val=None):
        if key == 'id':
            return user_instance
        if key == 'email':
            return MagicMock()
        return None

    mock_user_repo.get_by.side_effect = get_by
    mock_user_repo_class.instance.return_value = mock_user_repo

    response = client.put('/edit/1', json={"email": "old@WP.com"})
    assert response.status_code == 400
    assert response.get_json()['message'] == 'EMAIL_ALREADY_IN_USER'
