from flask import Blueprint, request, jsonify

from Backend_Python.app.utils.api_response import ApiResponse

pet_bp = Blueprint('pet', __name__)


@pet_bp.route('/create', methods=['POST'])
def register():
    return ApiResponse('OK', True, {}).return_response(), 201


@pet_bp.route('/edit', methods=['POST'])
def register():
    return ApiResponse('OK', True, {}).return_response(), 201


@pet_bp.route('/delete', methods=['POST'])
def register():
    return ApiResponse('OK', True, {}).return_response(), 201


@pet_bp.route('/list', methods=['POST'])
def register():
    return ApiResponse('OK', True, {}).return_response(), 201
