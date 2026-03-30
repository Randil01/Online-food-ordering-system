from bson import ObjectId
from datetime import datetime

def feedback_schema(feedback):
    return {
        "id": str(feedback["_id"]),
        "customer_name": feedback.get("customer_name"),
        "restaurant_id": feedback.get("restaurant_id"),
        "order_id": feedback.get("order_id"),
        "rating": feedback.get("rating", 0),
        "comment": feedback.get("comment", ""),
        "timestamp": feedback.get("timestamp", datetime.utcnow().isoformat())
    }
