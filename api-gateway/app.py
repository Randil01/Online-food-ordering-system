
from flask import Flask, jsonify, request
from flask_restx import Api
import requests

app = Flask(__name__)
api = Api(
    app,
    title="Online Food Ordering System API Gateway",
    version="1.0",
    description="""
    API Gateway for Online Food Ordering System

    Available Services:

    - Restaurant → /api/restaurant/restaurants
    - Order → /api/order/orders
    - Payment → /api/payment/payments
    - Feedback → /api/feedback/feedbacks
    - Delivery → /api/delivery/delivery

    All requests will go through this gateway
    """,
    doc="/docs"
)

# The SERVICES dictionary maps a service name to its base URL.
SERVICES = {
    "restaurant": "http://localhost:5001",
    "order": "http://localhost:5002",
    "payment": "http://localhost:5004",
    "feedback": "http://localhost:5005",
    "delivery": "http://localhost:5006"
}

@app.route('/api/<service_name>/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def gateway(service_name, path):
    """
    This function is the gateway that forwards requests to the appropriate microservice.
    It takes the service_name and path from the URL and forwards the request to the
    corresponding microservice.
    """
    if service_name not in SERVICES:
        return jsonify({"error": "Service not found"}), 404
        
    url = f"{SERVICES[service_name]}/{path}"
    
    try:
        resp = requests.request(
            method=request.method,
            url=url,
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            json=request.get_json() if request.is_json else None,
            params=request.args
        )
        
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items()
                   if name.lower() not in excluded_headers]
                   
        return (resp.content, resp.status_code, headers)
    except requests.exceptions.ConnectionError:
        return jsonify({"error": f"{service_name} service is down"}), 503

@app.route('/')
def home():
    return jsonify({"message": "API Gateway Running"})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
