
from flask import Flask, jsonify, request, make_response
from flask_restx import Api, Resource, Namespace
import requests

app = Flask(__name__)
api = Api(
    app,
    title="Online Food Ordering System API Gateway",
    version="1.0",
    description="API Gateway for Online Food Ordering System",
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

def forward_request(service_name, path):
    """
    Forwards requests to the appropriate microservice.
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
                   
        flask_resp = make_response(resp.content, resp.status_code)
        for name, value in headers:
            flask_resp.headers[name] = value
        return flask_resp
    except requests.exceptions.ConnectionError:
        return jsonify({"error": f"{service_name} service is down"}), 503

# --- RESTAURANT SERVICE ---
restaurant_ns = api.namespace('Restaurant', description='Restaurant service operations', path='/api/restaurant')

@restaurant_ns.route('/restaurants')
class RestaurantListProxy(Resource):
    @api.doc('list_restaurants')
    def get(self):
        """Get all restaurants"""
        return forward_request('restaurant', 'restaurants')
    
    @api.doc('create_restaurant')
    def post(self):
        """Create a new restaurant"""
        return forward_request('restaurant', 'restaurants')

@restaurant_ns.route('/restaurants/<id>')
class RestaurantProxy(Resource):
    @api.doc('get_restaurant')
    def get(self, id):
        """Get a specific restaurant"""
        return forward_request('restaurant', f'restaurants/{id}')
    
    @api.doc('update_restaurant')
    def put(self, id):
        """Update a restaurant"""
        return forward_request('restaurant', f'restaurants/{id}')
    
    @api.doc('delete_restaurant')
    def delete(self, id):
        """Delete a restaurant"""
        return forward_request('restaurant', f'restaurants/{id}')

# --- ORDER SERVICE ---
order_ns = api.namespace('Order', description='Order service operations', path='/api/order')

@order_ns.route('/orders')
class OrderListProxy(Resource):
    @api.doc('list_orders')
    def get(self):
        """Get all orders"""
        return forward_request('order', 'orders')
    
    @api.doc('create_order')
    def post(self):
        """Create a new order"""
        return forward_request('order', 'orders')

@order_ns.route('/orders/<id>')
class OrderProxy(Resource):
    @api.doc('get_order')
    def get(self, id):
        """Get a specific order"""
        return forward_request('order', f'orders/{id}')
    
    @api.doc('update_order')
    def put(self, id):
        """Update an order"""
        return forward_request('order', f'orders/{id}')
    
    @api.doc('delete_order')
    def delete(self, id):
        """Delete an order"""
        return forward_request('order', f'orders/{id}')

# --- PAYMENT SERVICE ---
payment_ns = api.namespace('Payment', description='Payment service operations', path='/api/payment')

@payment_ns.route('/payments')
class PaymentListProxy(Resource):
    @api.doc('list_payments')
    def get(self):
        """Get all payments"""
        return forward_request('payment', 'payments')
    
    @api.doc('create_payment')
    def post(self):
        """Create a new payment"""
        return forward_request('payment', 'payments')

@payment_ns.route('/payments/<id>')
class PaymentProxy(Resource):
    @api.doc('get_payment')
    def get(self, id):
        """Get a specific payment"""
        return forward_request('payment', f'payments/{id}')
    
    @api.doc('update_payment')
    def put(self, id):
        """Update a payment"""
        return forward_request('payment', f'payments/{id}')
    
    @api.doc('delete_payment')
    def delete(self, id):
        """Delete a payment"""
        return forward_request('payment', f'payments/{id}')

@payment_ns.route('/payments/<id>/status')
class PaymentStatusProxy(Resource):
    @api.doc('update_payment_status')
    def put(self, id):
        """Update payment status"""
        return forward_request('payment', f'payments/{id}/status')

@payment_ns.route('/payments/restaurant/<restaurant_id>')
class PaymentRestaurantProxy(Resource):
    @api.doc('get_payments_by_restaurant')
    def get(self, restaurant_id):
        """Get payments for a specific restaurant"""
        return forward_request('payment', f'payments/restaurant/{restaurant_id}')

# --- FEEDBACK SERVICE ---
feedback_ns = api.namespace('Feedback', description='Feedback service operations', path='/api/feedback')

@feedback_ns.route('/feedbacks')
class FeedbackListProxy(Resource):
    @api.doc('list_feedbacks')
    def get(self):
        """Get all feedbacks"""
        return forward_request('feedback', 'feedbacks')
    
    @api.doc('create_feedback')
    def post(self):
        """Submit new feedback"""
        return forward_request('feedback', 'feedbacks')

@feedback_ns.route('/feedbacks/<id>')
class FeedbackProxy(Resource):
    @api.doc('get_feedback')
    def get(self, id):
        """Get specific feedback"""
        return forward_request('feedback', f'feedbacks/{id}')
    
    @api.doc('delete_feedback')
    def delete(self, id):
        """Delete feedback"""
        return forward_request('feedback', f'feedbacks/{id}')

@feedback_ns.route('/feedbacks/restaurant/<restaurant_id>')
class FeedbackRestaurantProxy(Resource):
    @api.doc('get_feedbacks_by_restaurant')
    def get(self, restaurant_id):
        """Get feedbacks for a specific restaurant"""
        return forward_request('feedback', f'feedbacks/restaurant/{restaurant_id}')

# --- DELIVERY SERVICE ---
delivery_ns = api.namespace('Delivery', description='Delivery service operations', path='/api/delivery')

@delivery_ns.route('/delivery')
class DeliveryListProxy(Resource):
    @api.doc('list_deliveries')
    def get(self):
        """Get all deliveries"""
        return forward_request('delivery', 'delivery')
    
    @api.doc('create_delivery')
    def post(self):
        """Create a new delivery"""
        return forward_request('delivery', 'delivery')

@delivery_ns.route('/delivery/<id>')
class DeliveryProxy(Resource):
    @api.doc('get_delivery')
    def get(self, id):
        """Get a specific delivery"""
        return forward_request('delivery', f'delivery/{id}')
    
    @api.doc('update_delivery')
    def put(self, id):
        """Update a delivery"""
        return forward_request('delivery', f'delivery/{id}')
    
    @api.doc('delete_delivery')
    def delete(self, id):
        """Delete a delivery"""
        return forward_request('delivery', f'delivery/{id}')

# KEEP the generic catch-all gateway route as a fallback, but mark it hidden in swagger
@api.route('/api/<string:service_name>/<path:path>', doc=False)
class CatchAllGateway(Resource):
    def get(self, service_name, path):
        return forward_request(service_name, path)
    def post(self, service_name, path):
        return forward_request(service_name, path)
    def put(self, service_name, path):
        return forward_request(service_name, path)
    def delete(self, service_name, path):
        return forward_request(service_name, path)

@app.route('/')
def home():
    return jsonify({"message": "API Gateway Running. Visit /docs for Swagger UI"})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
