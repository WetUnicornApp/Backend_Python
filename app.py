from flask_cors import CORS
from flasgger import Swagger
from flask import Flask
from sqlalchemy import text, Result

from app.models.model import Model
from app.routes.employee_routes import employee_bp
from app.routes.owner_routes import owner_bp
from app.routes.pet_routes import pet_bp
from app.routes.visit_routes import visit_bp
from config.database import engine, get_db
# from sqlalchemy.ext.asyncio import AsyncSession
# import asyncio
from app.routes.user_routes import user_bp
from app.models.user_models import user
app = Flask(__name__)
swagger = Swagger(app)
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(visit_bp, url_prefix='/visit')
app.register_blueprint(pet_bp, url_prefix='/pet')
app.register_blueprint(owner_bp, url_prefix='/owner')
app.register_blueprint(employee_bp, url_prefix='/employee')

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

if __name__ == "__main__":
    print('Tabele')
    print(Model.metadata.tables.keys())
    #tworzenie tabel
    Model.metadata.create_all(engine)
    app.run(debug=True)
