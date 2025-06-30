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
#TEST ID: TOL1
@patch('app.routes.owner_routes.OwnerRepository')
@patch('app.routes.owner_routes.SessionLocal')
def test_list_owner_default(mock_session_local, mock_owner_repo_class, client):
    owners = [Owner(id=1, user_id=1), Owner(id=2, user_id=2)]
    mock_owner_repo = MagicMock()
    mock_owner_repo.session.query().all.return_value = owners
    mock_owner_repo_class.return_value = mock_owner_repo

    with patch('app.routes.owner_routes.SessionLocal') as mock_db:
        mock_db.return_value.query().filter_by().first.side_effect = lambda id=None: User(id=id, email=f"user{id}@wp.pl", first_name=f"First{id}", last_name=f"Last{id}")

        response = client.get('/list')

    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert isinstance(data['data'], list)

#TEST ID: TOL2
@patch('app.routes.owner_routes.OwnerRepository')
@patch('app.routes.owner_routes.SessionLocal')
def test_list_owner_with_s1(mock_session_local, mock_owner_repo_class, client):
    owners = [Owner(id=1, user_id=1)]
    mock_owner_repo = MagicMock()
    mock_owner_repo.session.query().all.return_value = owners
    mock_owner_repo_class.return_value = mock_owner_repo

    with patch('app.routes.owner_routes.SessionLocal') as mock_db:
        mock_db.return_value.query().filter_by().first.return_value = User(id=1, email="klosz@2t.com", first_name="Łucja", last_name="Klosz")

        response = client.get('/list?s=1')

    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert all('value' in item and 'text' in item for item in data['data'])
