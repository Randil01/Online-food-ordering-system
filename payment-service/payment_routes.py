from flask import request
from flask_restx import Namespace, Resource, fields
from db import payments_collection, restaurants_collection, orders_collection
from model import payment_schema
from bson import ObjectId
from datetime import datetime

payment_ns = Namespace('payments', description="Payment operations")

payment_model = payment_ns.model('Payment', {
    'order_id': fields.String(required=True),
    'restaurant_id': fields.String(required=True),
    'amount': fields.Float(required=True),
    'method': fields.String(required=True),
    'status': fields.String(default="Pending")
})

# validation functions

import requests

    
def restaurant_exists(restaurant_id):
    try:
        return restaurants_collection.find_one({"_id": ObjectId(restaurant_id)}) is not None
    except:
        return False


def order_exists(order_id):
    try:
        return orders_collection.find_one({"_id": ObjectId(order_id)}) is not None
    except:
        return False


# create / get all payments
@payment_ns.route('/')
class PaymentList(Resource):

    @payment_ns.expect(payment_model)
    def post(self):
        data = request.json

        # VALIDATION
        if not restaurant_exists(data["restaurant_id"]):
            return {"error": "Restaurant not found"}, 404

        if not order_exists(data["order_id"]):
            return {"error": "Order not found"}, 404

        if data["amount"] <= 0:
            return {"error": "Amount must be greater than 0"}, 400

        payment = {
            "order_id": data["order_id"],
            "restaurant_id": data["restaurant_id"],
            "amount": data["amount"],
            "method": data["method"],
            "status": data.get("status", "Pending"),
            "created_at": datetime.utcnow()
        }

        result = payments_collection.insert_one(payment)

        return {
            "message": "Payment created",
            "id": str(result.inserted_id)
        }


    def get(self):
        payments = payments_collection.find()
        return [payment_schema(p) for p in payments]


# get/update/delete payment by id
@payment_ns.route('/<id>')
class Payment(Resource):

    def get(self, id):
        payment = payments_collection.find_one({"_id": ObjectId(id)})
        if not payment:
            return {"error": "Payment not found"}, 404
        return payment_schema(payment)

    def put(self, id):
        data = request.json

        # Optional validation if updating foreign keys
        if "restaurant_id" in data and not restaurant_exists(data["restaurant_id"]):
            return {"error": "Invalid restaurant_id"}, 404

        if "order_id" in data and not order_exists(data["order_id"]):
            return {"error": "Invalid order_id"}, 404

        payments_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": data}
        )

        return {"message": "Payment updated"}

    def delete(self, id):
        payments_collection.delete_one({"_id": ObjectId(id)})
        return {"message": "Payment deleted"}


#update payment status
@payment_ns.route('/<id>/status')
class PaymentStatus(Resource):
    def put(self, id):
        data = request.json

        payments_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"status": data["status"]}}
        )

        return {"message": "Status updated"}



# get payment by resturant
@payment_ns.route('/restaurant/<restaurant_id>')
class PaymentsByRestaurant(Resource):
    def get(self, restaurant_id):

        if not restaurant_exists(restaurant_id):
            return {"error": "Restaurant not found"}, 404

        payments = payments_collection.find({"restaurant_id": restaurant_id})
        return [payment_schema(p) for p in payments]