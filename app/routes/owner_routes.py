from flask import Blueprint, request, jsonify

from app.utils.api_response import ApiResponse

#from Backend_Python.app.utils.api_response import ApiResponse

owner_bp = Blueprint('owner', __name__)


@owner_bp.route('/create', methods=['POST'])
def create():
    return ApiResponse('Create new owner', True, {}).return_response(), 201


@owner_bp.route('/edit', methods=['POST'])
def edit():
    return ApiResponse('OK', True, {}).return_response(), 201


@owner_bp.route('/delete', methods=['POST'])
def delete():
    return ApiResponse('OK', True, {}).return_response(), 201


@owner_bp.route('/list', methods=['POST'])
def list():
    return ApiResponse('OK', True, {}).return_response(), 201
