import requests
import time
import random

# URL for your /predict endpoint
url = "http://127.0.0.1:8000/predict"

# Number of requests to send
num_requests = 15

for i in range(num_requests):
    # Generate more extreme drifting values
    payload = {
        "feature1": random.uniform(500, 1000),  # Much higher than training mean (~5.8)
        "feature2": random.uniform(400, 800),    # Much higher than training mean (~3.06)
        "feature3": random.uniform(300, 700),    # Much higher than training mean (~3.73)
        "feature4": random.uniform(200, 600)     # Much higher than training mean (~1.18)
    }
    
    response = requests.post(url, json=payload)
    print(f"Response {i+1}: {response.json()} - Payload: {payload}")
    
    # Wait a short time between requests
    time.sleep(0.5)