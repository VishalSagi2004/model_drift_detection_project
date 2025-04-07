import requests
import time
import random

# URL for your /predict endpoint
url = "http://127.0.0.1:8000/predict"

# Number of requests to send
num_requests = 15

for i in range(num_requests):
    # Generate normal values near original Iris training means
    payload = {
        "feature1": random.uniform(4.5, 7.5),   # Petal length
        "feature2": random.uniform(2.0, 4.5),   # Sepal width
        "feature3": random.uniform(1.0, 6.0),   # Petal width
        "feature4": random.uniform(0.0, 2.5)    # Sepal length
    }
    
    response = requests.post(url, json=payload)
    print(f"Response {i+1}: {response.json()} - Payload: {payload}")
    
    time.sleep(0.5)