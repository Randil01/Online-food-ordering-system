from flask import request
from flask_restx import Namespace, Resource, fields
from db import deliveries_collection
from models.delivery import delivery_schema
from bson import ObjectId
from datetime import datetime

delivery_ns = Namespace('delivery', description="Delivery operations")

delivery_model = delivery_ns.model('Delivery', {
    'order_id': fields.String(required=True, description='The associated order ID'),
    'driver_name': fields.String(required=True, description='The name of the driver assigned'),
    'status': fields.String(description='The status of the delivery (e.g., Pending, Assigned, Out for Delivery, Delivered)', default="Pending")
})

delivery_update_model = delivery_ns.model('DeliveryUpdate', {
    'driver_name': fields.String(description='The name of the driver assigned'),
    'status': fields.String(description='The status of the delivery')
})

valid_statuses = ["Pending", "Assigned", "Out for Delivery", "Delivered"]

@delivery_ns.route('/')
class DeliveryList(Resource):
    
    @delivery_ns.doc('list_deliveries')
    def get(self):
        """Retrieve all delivery records"""
        deliveries = deliveries_collection.find()
        return [delivery_schema(d) for d in deliveries], 200

    @delivery_ns.expect(delivery_model, validate=True)
    @delivery_ns.doc('create_delivery')
    def post(self):
        """Create a new delivery record"""
        data = request.json
        
        status = data.get("status", "Pending")
        if status not in valid_statuses:
            return {"error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"}, 400

        delivery_doc = {
            "order_id": data["order_id"],
            "driver_name": data["driver_name"],
            "status": status,
            "created_at": datetime.utcnow()
        }
        
        result = deliveries_collection.insert_one(delivery_doc)
        
        return {
            "message": "Delivery created successfully",
            "id": str(result.inserted_id)
        }, 201

@delivery_ns.route('/<id>')
@delivery_ns.param('id', 'The delivery identifier')
@delivery_ns.response(404, 'Delivery not found')
class Delivery(Resource):
    
    @delivery_ns.doc('get_delivery')
    def get(self, id):
        """Retrieve a single delivery by its id"""
        if not ObjectId.is_valid(id):
            return {"error": "Invalid ID format"}, 400
            
        delivery = deliveries_collection.find_one({"_id": ObjectId(id)})
        if not delivery:
            return {"error": "Delivery not found"}, 404
            
        return delivery_schema(delivery), 200

    @delivery_ns.expect(delivery_update_model)
    @delivery_ns.doc('update_delivery')
    def put(self, id):
        """Update delivery status or driver_name"""
        if not ObjectId.is_valid(id):
            return {"error": "Invalid ID format"}, 400

        data = request.json
        if not data:
            return {"error": "No data provided to update"}, 400

        update_fields = {}
        if "driver_name" in data:
            update_fields["driver_name"] = data["driver_name"]
            
        if "status" in data:
            if data["status"] not in valid_statuses:
                return {"error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"}, 400
            update_fields["status"] = data["status"]
            
        if not update_fields:
            return {"error": "Must provide 'driver_name' or 'status' to update"}, 400

        result = deliveries_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": update_fields}
        )
        
        if result.matched_count == 0:
            return {"error": "Delivery not found"}, 404
            
        return {"message": "Delivery updated successfully"}, 200

    @delivery_ns.doc('delete_delivery')
    def delete(self, id):
        """Delete a delivery record"""
        if not ObjectId.is_valid(id):
            return {"error": "Invalid ID format"}, 400

        result = deliveries_collection.delete_one({"_id": ObjectId(id)})
        
        if result.deleted_count == 0:
            return {"error": "Delivery not found"}, 404
            
        return {"message": "Delivery deleted successfully"}, 200
