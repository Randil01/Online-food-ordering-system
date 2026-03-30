from flask import Flask
from flask_restx import Api
from feedback_routes import feedback_ns
from config import Config
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

api = Api(
    app,
    title="Feedback Service API",
    version="1.0",
    description="Handles customer feedback and restaurant reviews",
    doc="/docs"
)

api.add_namespace(feedback_ns, path="/feedbacks")

if __name__ == "__main__":
    app.run(port=Config.PORT, debug=True)
