import requests
import json

BASE_URL = "http://127.0.0.1:5002/orders"

def test_order_service():
    print("Testing Order API Microservice...\n")
    
    # 1. Create a new order
    print("1. Creating a new order...")
    new_order = {
        "customer_name": "John Doe Test",
        "restaurant_id": "rest_12345",
        "payment_id": "pay_98765",
        "delivery_note": "Leave at the front door",
        "items": [
            {"name": "Margherita Pizza", "quantity": 1, "price": 12.99},
            {"name": "Garlic Bread", "quantity": 1, "price": 4.99}
        ],
        "total_amount": 17.98,
        "status": "Pending"
    }
    
    response = requests.post(f"{BASE_URL}/", json=new_order)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}\n")
    
    if response.status_code != 201:
        print("Failed to create order.")
        return
        
    order_id = response.json().get("id")
    
    # 2. Get all orders
    print("2. Fetching all orders...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Found {len(response.json())} orders. Top order: {response.json()[0]['customer_name']}\n")
    
    # 3. Get the specific order
    print(f"3. Fetching order by ID ({order_id})...")
    response = requests.get(f"{BASE_URL}/{order_id}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    
    # 4. Update the order
    print("4. Updating the order status to 'Delivered'...")
    update_data = response.json()
    update_data["status"] = "Delivered"
    # Note: the update must match all fields expected by the PUT route
    response = requests.put(f"{BASE_URL}/{order_id}", json=update_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}\n")
    
    # 5. Delete the order
    print("5. Cleaning up (Deleting the order)...")
    response = requests.delete(f"{BASE_URL}/{order_id}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}\n")
    
    print("Test Completed Successfully!")

if __name__ == "__main__":
    test_order_service()
