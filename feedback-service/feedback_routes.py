from flask import request
from flask_restx import Namespace, Resource, fields
from db import feedbacks_collection
from model import feedback_schema
from bson import ObjectId
from datetime import datetime

feedback_ns = Namespace('feedbacks', description="Feedback and Review operations")

feedback_model = feedback_ns.model('Feedback', {
    'customer_name': fields.String(required=True, description='Name of the customer'),
    'restaurant_id': fields.String(required=True, description='ID of the restaurant being reviewed'),
    'order_id': fields.String(required=False, description='ID of the associated order'),
    'rating': fields.Integer(required=True, description='Rating from 1 to 5', min=1, max=5),
    'comment': fields.String(required=True, description='Feedback text'),
})

@feedback_ns.route('/')
class FeedbackList(Resource):
    
    @feedback_ns.expect(feedback_model)
    def post(self):
        data = request.json
        
        # Basic validation for rating
        rating = data.get("rating", 0)
        if not (1 <= rating <= 5):
            return {"error": "Rating must be between 1 and 5"}, 400

        new_feedback = {
            "customer_name": data["customer_name"],
            "restaurant_id": data["restaurant_id"],
            "order_id": data.get("order_id"),
            "rating": rating,
            "comment": data["comment"],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        result = feedbacks_collection.insert_one(new_feedback)
        
        return {
            "message": "Feedback submitted successfully",
            "id": str(result.inserted_id)
        }, 201

    def get(self):
        feedbacks = feedbacks_collection.find()
        return [feedback_schema(fb) for fb in feedbacks]


@feedback_ns.route('/<id>')
class Feedback(Resource):
    
    def get(self, id):
        feedback = feedbacks_collection.find_one({"_id": ObjectId(id)})
        if not feedback:
            return {"error": "Feedback not found"}, 404
        return feedback_schema(feedback)

    def delete(self, id):
        result = feedbacks_collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            return {"error": "Feedback not found"}, 404
        return {"message": "Feedback deleted successfully"}


@feedback_ns.route('/restaurant/<restaurant_id>')
class RestaurantFeedback(Resource):
    
    def get(self, restaurant_id):
        feedbacks = feedbacks_collection.find({"restaurant_id": restaurant_id})
        return [feedback_schema(fb) for fb in feedbacks]
