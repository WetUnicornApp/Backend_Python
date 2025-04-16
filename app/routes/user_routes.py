from flask import Blueprint

user_bp = Blueprint('user', __name__)

@user_bp.route('/', methods=['POST'])
def create_user():
    return "Użytkownik został stworzony!", 201

@user_bp.route('/', methods=['GET'])
def get_users():
    return "Lista użytkowników", 200
