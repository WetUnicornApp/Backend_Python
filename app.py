from flasgger import Swagger
from flask import Flask
from config.database import engine, get_db
# from sqlalchemy.ext.asyncio import AsyncSession
# import asyncio
app = Flask(__name__)
swagger = Swagger(app)

@app.route('/')
async def index():
    async for db in get_db():
        return "Połączenie z bazą danych działa!", 200

if __name__ == "__main__":
    app.run(debug=True)
