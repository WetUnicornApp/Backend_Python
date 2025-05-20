from flask import Flask
from flasgger import Swagger


def create_app():
    app = Flask(__name__)
    Swagger(app)

    # Rejestrujemy blueprinty (czyli nasze endpointy)
    from app.routes.user_routes import user_bp

    app.register_blueprint(user_bp, url_prefix="/users")

    return app
