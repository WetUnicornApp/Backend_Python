from flask import Blueprint, request, jsonify

from Backend_Python.app.utils.api_response import ApiResponse

pet_bp = Blueprint('pet', __name__)


@pet_bp.route('/create', methods=['POST'])
def create():
    return ApiResponse('OK', True, {}).return_response(), 201


@pet_bp.route('/edit', methods=['POST'])
def edit():
    return ApiResponse('OK', True, {}).return_response(), 201


@pet_bp.route('/delete', methods=['POST'])
def delete():
    return ApiResponse('OK', True, {}).return_response(), 201


@pet_bp.route('/list', methods=['GET'])
def list():
    if request.args.get('simple'):
        return ApiResponse('OK', True, [{1: 'Fafik'}, {2: 'Petunia'}]).return_response(), 200
    else:
        return ApiResponse('OK', True, {}).return_response(), 200
