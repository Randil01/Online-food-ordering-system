from flask import Flask
from flask_restx import Api
from routes.delivery_routes import delivery_ns
from config import Config

app = Flask(__name__)

api = Api(
    app,
    title="Delivery Service API",
    version="1.0",
    description="Handles delivery operations",
    doc="/docs"
)

api.add_namespace(delivery_ns, path="/delivery")

if __name__ == "__main__":
    app.run(port=Config.PORT, debug=True)
