from flask import Flask
from flask_restx import Api
from order_routes import order_ns
from config import Config
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

api = Api(
    app,
    title="Order Service API",
    version="1.0",
    description="Handles food orders, and tracking status",
    doc="/docs"
)

api.add_namespace(order_ns, path="/orders")

if __name__ == "__main__":
    app.run(port=Config.PORT, debug=True)
