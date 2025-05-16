from flask import Blueprint, request, jsonify

from Backend_Python.app.utils.api_response import ApiResponse

visit_bp = Blueprint('visit', __name__)


@visit_bp.route('/create', methods=['POST'])
def register():
    return ApiResponse('OK', True, {}).return_response(), 201


@visit_bp.route('/edit', methods=['POST'])
def register():
    return ApiResponse('OK', True, {}).return_response(), 201


@visit_bp.route('/delete', methods=['POST'])
def register():
    return ApiResponse('OK', True, {}).return_response(), 201


@visit_bp.route('/list', methods=['POST'])
def register():
    return ApiResponse('OK', True, {}).return_response(), 201
