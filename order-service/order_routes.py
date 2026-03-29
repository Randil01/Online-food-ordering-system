from flask import request
from flask_restx import Namespace, Resource, fields
from db import orders_collection
from model import order_schema
from bson import ObjectId

order_ns = Namespace('orders', description="Order operations")

order_item_model = order_ns.model('OrderItem', {
    'name': fields.String(required=True),
    'quantity': fields.Integer(required=True),
    'price': fields.Float(required=True)
})

order_model = order_ns.model('Order', {
    'customer_name': fields.String(required=True),
    'restaurant_id': fields.String(required=True, description='Restaurant ID associated with the order'),
    'payment_id': fields.String(required=False, description='Payment ID for the transaction'),
    'feedback_id': fields.String(required=False, description='Feedback ID left for this order'),
    'delivery_note': fields.String(required=False, description='Special instructions for delivery'),
    'items': fields.List(fields.Nested(order_item_model), required=True),
    'total_amount': fields.Float(required=True),
    'status': fields.String(default="Pending")
})

@order_ns.route('/')
class OrderList(Resource):
    
    @order_ns.expect(order_model)
    def post(self):
        data = request.json
        
        new_order = {
            "customer_name": data["customer_name"],
            "restaurant_id": data["restaurant_id"],
            "payment_id": data.get("payment_id"),
            "feedback_id": data.get("feedback_id"),
            "delivery_note": data.get("delivery_note"),
            "items": data["items"],
            "total_amount": data["total_amount"],
            "status": data.get("status", "Pending")
        }
        
        result = orders_collection.insert_one(new_order)
        
        return {
            "message": "Order created successfully",
            "id": str(result.inserted_id)
        }, 201

    def get(self):
        orders = orders_collection.find()
        return [order_schema(order) for order in orders]


@order_ns.route('/<id>')
class Order(Resource):
    
    def get(self, id):
        order = orders_collection.find_one({"_id": ObjectId(id)})
        if not order:
            return {"error": "Order not found"}, 404
        return order_schema(order)

    @order_ns.expect(order_model)
    def put(self, id):
        data = request.json
        
        update_data = {
            "customer_name": data["customer_name"],
            "restaurant_id": data["restaurant_id"],
            "payment_id": data.get("payment_id"),
            "feedback_id": data.get("feedback_id"),
            "delivery_note": data.get("delivery_note"),
            "items": data["items"],
            "total_amount": data["total_amount"],
            "status": data.get("status", "Pending")
        }
        
        result = orders_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            return {"error": "Order not found"}, 404
            
        return {"message": "Order updated successfully"}

    def delete(self, id):
        result = orders_collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            return {"error": "Order not found"}, 404
        return {"message": "Order deleted successfully"}
