from flask import Blueprint, jsonify, request

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/', methods=['GET'])
def get_users():
    return jsonify({"users": ["Alice", "Bob", "Charlie"]})

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return jsonify({"user_id": user_id})

@user_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get("name")
    return jsonify({"message": f"User {name} created"}), 201
