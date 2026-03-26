import importlib

def delivery_schema(delivery):
    return {
        "id": str(delivery["_id"]),
        "order_id": delivery.get("order_id"),
        "driver_name": delivery.get("driver_name"),
        "status": delivery.get("status"),
        "created_at": delivery.get("created_at")
    }
