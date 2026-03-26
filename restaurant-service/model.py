from bson import ObjectId

def restaurant_schema(restaurant):
    return {
        "id": str(restaurant["_id"]),
        "name": restaurant["name"],
        "location": restaurant["location"],
        "cuisine": restaurant["cuisine"],
        "rating": restaurant.get("rating", 0)
    }