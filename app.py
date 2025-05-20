from flask_cors import CORS
from flasgger import Swagger
from flask import Flask

from app.routes.owner_routes import owner_bp
from app.routes.pet_routes import pet_bp
from app.routes.visit_routes import visit_bp
#from Backend_Python.app.routes.owner_routes import owner_bp
#from Backend_Python.app.routes.pet_routes import pet_bp
#from Backend_Python.app.routes.visit_routes import visit_bp
from config.database import engine, get_db
# from sqlalchemy.ext.asyncio import AsyncSession
# import asyncio
from app.routes.user_routes import user_bp

app = Flask(__name__)
swagger = Swagger(app)
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(visit_bp, url_prefix='/visit')
app.register_blueprint(pet_bp, url_prefix='/pet')
app.register_blueprint(owner_bp, url_prefix='/owner')

CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/')
async def index():
    async for db in get_db():
        return "Połączenie z bazą danych działa!", 200


if __name__ == "__main__":
    app.run(debug=True)
