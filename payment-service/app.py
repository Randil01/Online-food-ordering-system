from flask import Flask
from flask_restx import Api
from payment_routes import payment_ns
from config import Config

app = Flask(__name__)

api = Api(
    app,
    title="Payment Service API",
    version="1.0",
    description="Handles payment processing on restaurants and order details",
    doc="/docs"
)

api.add_namespace(payment_ns, path="/payments")

if __name__ == "__main__":
    app.run(port=Config.PORT, debug=True)