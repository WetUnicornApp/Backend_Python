from datetime import datetime

from flask import Blueprint, request, jsonify
from sqlalchemy import DateTime

from app.utils.api_response import ApiResponse

# from Backend_Python.app.utils.api_response import ApiResponse

employee_bp = Blueprint('employee', __name__)


@employee_bp.route('/create', methods=['POST'])
def create():
    """
    Expect form content
    Return 201 or 400
    """
    return ApiResponse('OK', True, {}).return_response(), 201


@employee_bp.route('/edit', methods=['POST'])
def edit():
    """
    Expect form content
    Return 200 or 400
    """
    return ApiResponse('OK', True, {}).return_response(), 200


@employee_bp.route('/delete', methods=['DELETE'])
def delete():
    """
    Expect employee identifier
    Return 200 or 400
    """
    return ApiResponse('OK', True, {}).return_response(), 201


@employee_bp.route('/list', methods=['GET'])
def list():
    """
        Expect nothing
        Return 200 or 400
    """
    return ApiResponse('OK', True, [
        {'employee': 'Anna Kowalska', 'owner': "Jan Nowak", 'pet': "Fafik", 'name': 'name name', 'description': 'lorem',
         'date': datetime.now().strftime('%d.%m.%Y'),
         'time': datetime.now().strftime('%H:%M')}]).return_response(), 200
