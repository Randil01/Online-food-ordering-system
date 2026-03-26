from flask import request
from flask_restx import Namespace, Resource, fields
from db import restaurants_collection
from model import restaurant_schema
from bson import ObjectId

restaurant_ns = Namespace('restaurants', description="Restaurant operations")

restaurant_model = restaurant_ns.model('Restaurant', {
    'name': fields.String(required=True),
    'location': fields.String(required=True),
    'cuisine': fields.String(required=True),
    'rating': fields.Float(default=0)
})


# Create / Read all restaurants
@restaurant_ns.route('/')
class RestaurantList(Resource):

    @restaurant_ns.expect(restaurant_model)
    def post(self):
        data = request.json

        restaurant = {
            "name": data["name"],
            "location": data["location"],
            "cuisine": data["cuisine"],
            "rating": data.get("rating", 0)
        }

        result = restaurants_collection.insert_one(restaurant)

        return {
            "message": "Restaurant created",
            "id": str(result.inserted_id)
        }, 201


    def get(self):
        restaurants = restaurants_collection.find()
        return [restaurant_schema(r) for r in restaurants]


# Read/Update/Delete single restaurant
@restaurant_ns.route('/<id>')
class Restaurant(Resource):

    def get(self, id):
        restaurant = restaurants_collection.find_one({"_id": ObjectId(id)})
        if not restaurant:
            return {"error": "Restaurant not found"}, 404
        return restaurant_schema(restaurant)

    def put(self, id):
        data = request.json

        restaurants_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": data}
        )

        return {"message": "Restaurant updated"}

    def delete(self, id):
        restaurants_collection.delete_one({"_id": ObjectId(id)})
        return {"message": "Restaurant deleted"}