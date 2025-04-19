from flask import Blueprint, request, jsonify

user_bp = Blueprint('user', __name__)


@user_bp.route('/register', methods=['POST'])
def create_user():
    data = request.get_json()
    return "Przekzane dane to: " + data.get('email'), 201


@user_bp.route('/', methods=['GET'])
def get_users():
    return "Lista użytkowników", 200
