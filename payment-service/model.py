
def payment_schema(payment):
    return {
        "id": str(payment["_id"]),
        "order_id": payment["order_id"], # FOREIGN KEY
        "restaurant_id": payment["restaurant_id"],  # FOREIGN KEY
        "amount": payment["amount"],
        "status": payment["status"],
        "method": payment["method"],
        "created_at": payment["created_at"].isoformat() 
    }