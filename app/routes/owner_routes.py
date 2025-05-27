from flask import Blueprint, request, jsonify

from app.utils.api_response import ApiResponse

# from Backend_Python.app.utils.api_response import ApiResponse

owner_bp = Blueprint('owner', __name__)


@owner_bp.route('/create', methods=['POST'])
def create():
    """
    Expect form content
    Return 201 or 400
    """

    return ApiResponse('Create new owner', True, {}).return_response(), 201


@owner_bp.route('/edit', methods=['POST'])
def edit():
    """
    Expect form content
    Return 200 or 400
    """
    return ApiResponse('OK', True, {}).return_response(), 201


@owner_bp.route('/delete', methods=['DELETE'])
def delete():
    """
    Expect owner identifier
    Return 200 or error
    """
    return ApiResponse('OK', True, {}).return_response(), 201


@owner_bp.route('/list', methods=['GET'])
def list():
    """
    Expect nothing
    Return 201 or 400
    """
    return ApiResponse('OK', True, {}).return_response(), 201
