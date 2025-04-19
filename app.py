from flask_cors import CORS
from flasgger import Swagger
from flask import Flask
from config.database import engine, get_db
# from sqlalchemy.ext.asyncio import AsyncSession
# import asyncio
from app.routes.user_routes import user_bp

app = Flask(__name__)
swagger = Swagger(app)
app.register_blueprint(user_bp, url_prefix='/user')

CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/')
async def index():
    async for db in get_db():
        return "Połączenie z bazą danych działa!", 200


if __name__ == "__main__":
    app.run(debug=True)
