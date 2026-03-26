from flask import Flask
from flask_restx import Api
from restaurant_routes import restaurant_ns
from config import Config

app = Flask(__name__)

api = Api(
    app,
    title="Restaurant Service API",
    version="1.0",
    description="Handles restaurant details and management",
    doc="/docs"
)

api.add_namespace(restaurant_ns, path="/restaurants")

if __name__ == "__main__":
    app.run(port=Config.PORT, debug=True)