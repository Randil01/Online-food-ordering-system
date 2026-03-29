from bson import ObjectId

def order_schema(order):
    return {
        "id": str(order["_id"]),
        "customer_name": order.get("customer_name"),
        "restaurant_id": order.get("restaurant_id"),
        "payment_id": order.get("payment_id"),
        "feedback_id": order.get("feedback_id"),
        "delivery_note": order.get("delivery_note"),
        "items": order.get("items", []),
        "total_amount": order.get("total_amount", 0.0),
        "status": order.get("status", "Pending")
    }
