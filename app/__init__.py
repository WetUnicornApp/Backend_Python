from flask import Flask
from flask_cors import CORS
from flasgger import Swagger

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Import and register blueprints
    from app.routes.user_routes import user_bp
    from app.routes.visit_routes import visit_bp
    from app.routes.pet_routes import pet_bp
    from app.routes.owner_routes import owner_bp
    from app.routes.employee_routes import employee_bp
    from app.routes.organization_routes import organization_bp

    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(visit_bp, url_prefix='/visit')
    app.register_blueprint(pet_bp, url_prefix='/pet')
    app.register_blueprint(owner_bp, url_prefix='/owner')
    app.register_blueprint(employee_bp, url_prefix='/employee')
    app.register_blueprint(organization_bp, url_prefix='/organization')

    @app.route('/')
    def index():
        return 'Welcome to the Unicorn API!'

    return app
