from flask import Blueprint, request, jsonify

from Backend_Python.app.utils.api_response import ApiResponse

owner_bp = Blueprint('owner', __name__)


@owner_bp.route('/create', methods=['POST'])
def register():
    return ApiResponse('OK', True, {}).return_response(), 201


@owner_bp.route('/edit', methods=['POST'])
def register():
    return ApiResponse('OK', True, {}).return_response(), 201


@owner_bp.route('/delete', methods=['POST'])
def register():
    return ApiResponse('OK', True, {}).return_response(), 201


@owner_bp.route('/list', methods=['POST'])
def register():
    return ApiResponse('OK', True, {}).return_response(), 201
