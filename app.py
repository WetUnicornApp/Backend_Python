from app import create_app
from app.models.model import Model
from config.database import engine

app = create_app()

if __name__ == "__main__":
    Model.metadata.create_all(engine)
    app.run(host="0.0.0.0", port=5000, debug=True)
