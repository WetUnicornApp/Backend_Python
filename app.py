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
from app.models.calendar_models.calendar import Calendar
from app.models.visit_models.visit import Visit
from app.models.visit_models.visit_animal import VisitAnimal
from app.models.visit_models.visit_employee import VisitEmployee


app = Flask(__name__)


app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(visit_bp, url_prefix='/visit')
app.register_blueprint(pet_bp, url_prefix='/pet')
app.register_blueprint(owner_bp, url_prefix='/owner')
app.register_blueprint(employee_bp, url_prefix='/employee')
app.register_blueprint(organization_bp, url_prefix='/organization')


CORS(app, resources={r"/*": {"origins": "*"}})



@app.route("/")
def index():
    return "Welcome to the Unicorn API!"

#user_bp = Blueprint('user', __name__)
#organization_bp = Blueprint('organization', __name__)
#employee_bp = Blueprint('employee', __name__)
#owner_bp = Blueprint('owner', __name__)
#pet_bp = Blueprint('pet', __name__)
if __name__ == "__main__":
    #print('Tabele')
    #print(Model.metadata.tables.keys())
    #Model.metadata.create_all(engine)
    #app.run(debug=True)
    Model.metadata.create_all(engine)
    app.run(host='0.0.0.0', port=5000)
