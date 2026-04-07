# Online Food Ordering System – Microservices Architecture

## Overview
This project implements an **Online Food Ordering System** using a **microservices architecture** as part of the IT4020 assignment.

The system is divided into multiple independent services, where each service handles a specific business functionality. All services are accessed through a centralized API Gateway.

---

## Microservices

### 1. Restaurant Service
- Manages restaurant details such as name, location, cuisine, and ratings  
- Provides CRUD operations for restaurants  

### 2. Order Service
- Handles customer order creation and management  
- Tracks order status  

### 3. Payment Service
- Processes customer payments  
- Manages transaction records  

### 4. Feedback Service
- Handles customer reviews and ratings  
- Stores feedback for restaurants  

### 5. Delivery Service
- Manages delivery assignments  
- Tracks delivery status  

---

## API Gateway
- Acts as a **single entry point** for all client requests  
- Routes requests to appropriate microservices  
- Eliminates the need for exposing multiple service ports  
- Simplifies communication between client and backend  

---

## Project Structure
food-ordering-system/
│
├── api-gateway/
├── restaurant-service/
├── order-service/
├── payment-service/
├── feedback-service/
├── delivery-service/
├── .env
└── README.md

## How to Run the Project

### 1. Clone the repository
git clone <your-repo-link>
cd food-ordering-system


### 2. Run each microservice
Navigate into each service folder and run:
flask run --port

Example ports:
- API Gateway → 5000
- Restaurant Service → 5001  
- Order Service → 5002  
- Payment Service → 5003  
- Feedback Service → 5004  
- Delivery Service → 5005  

### 3. Run API Gateway
cd api-gateway
flask run --port 

## API Access

### Direct Access (Example)
http://localhost:5000/api/restaurants


### Via API Gateway (Example)
http://localhost:5001/restaurants
---

## Key Features
- Microservices-based architecture  
- Independent service deployment  
- RESTful APIs  
- Centralized API Gateway routing  

---

## Contribution

| Member | Contribution |
|--------|-------------|
| Duvini27 | Restaurant Service |
| Vnuja | Order Service |
| Randil01 | Payment Service |
| venujageenodh 4 | Feedback Service |
| Dinal Chnadeepa | Delivery Service |

---

## Notes
- Each microservice runs independently  
- MongoDB is used as the database  
- API Gateway is used to unify access to services  

---

## Conclusion
This project demonstrates how microservices architecture can be used to build a scalable and modular online food ordering system with independent services and centralized access through an API Gateway.
