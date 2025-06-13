from flask_cors import CORS
from flasgger import Swagger
from flask import Flask, Blueprint
from sqlalchemy import text, Result
from app.routes.employee_routes import employee_bp
from app.models.model import Model
from app.routes.owner_routes import owner_bp
from app.routes.pet_routes import pet_bp
from app.routes.visit_routes import visit_bp
from app.routes.organization_routes import organization_bp
from config.database import engine, get_db
# from sqlalchemy.ext.asyncio import AsyncSession
# import asyncio
from app.routes.user_routes import user_bp
#To musim być dzięki temu tworzone są tabela w bazie danych na podstawie modeli
from app.models.user_models import user
from app.models.organization_models.organization_model import OrganizationModel
from app.models.organization_models.employee import Employee
from app.models.owner_models.owner import Owner
from app.models.animal_models.animal import Animal
from app.models.animal_models.type import Type

app = Flask(__name__)
swagger = Swagger(app)
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(visit_bp, url_prefix='/visit')
app.register_blueprint(pet_bp, url_prefix='/pet')
app.register_blueprint(owner_bp, url_prefix='/owner')
app.register_blueprint(employee_bp, url_prefix='/employee')
app.register_blueprint(organization_bp, url_prefix='/organization')


CORS(app, resources={r"/*": {"origins": "*"}})



@app.route('/')
def index():
    db = next(get_db())
    query = text("SELECT @@SERVERNAME AS server_name, DB_NAME() AS database_name")
    result: Result = db.execute(query)
    row = result.mappings().fetchone()
    server_name = row['server_name']
    database_name = row['database_name']
    return f"Server: {server_name}, Database: {database_name}"

user_bp = Blueprint('user', __name__)
organization_bp = Blueprint('organization', __name__)
employee_bp = Blueprint('employee', __name__)
owner_bp = Blueprint('owner', __name__)
if __name__ == "__main__":
    print('Tabele')
    print(Model.metadata.tables.keys())
    Model.metadata.create_all(engine)
    app.run(debug=True)
