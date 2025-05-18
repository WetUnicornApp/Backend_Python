from datetime import datetime

from flask import Blueprint, request, jsonify
from sqlalchemy import DateTime

from Backend_Python.app.utils.api_response import ApiResponse

visit_bp = Blueprint('visit', __name__)


@visit_bp.route('/create', methods=['POST'])
def create():
    return ApiResponse('OK', True, {}).return_response(), 201


@visit_bp.route('/edit', methods=['POST'])
def edit():
    return ApiResponse('OK', True, {}).return_response(), 201


@visit_bp.route('/delete', methods=['POST'])
def delete():
    return ApiResponse('OK', True, {}).return_response(), 201


@visit_bp.route('/list', methods=['GET'])
def list():
    return ApiResponse('OK', True, [
        {'employee': 'Anna Kowalska', 'owner': "Jan Nowak", 'pet': "Fafik", 'name': 'name name', 'description': 'lorem',
         'date': datetime.now().strftime('%d.%m.%Y'),
         'time': datetime.now().strftime('%H:%M')}]).return_response(), 200
