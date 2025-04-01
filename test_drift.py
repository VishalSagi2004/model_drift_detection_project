import requests
import time
import random

# URL for your /predict endpoint
url = "http://127.0.0.1:8000/predict"

# Number of requests to send
num_requests = 15

for i in range(num_requests):
    # Generate drifting values (randomized within a high range)
    payload = {
        "feature1": random.uniform(50, 100),  # Training mean ~5.8, so 50-100 simulates drift
        "feature2": random.uniform(40, 80),   # Training mean ~3.06
        "feature3": random.uniform(30, 70),   # Training mean ~3.73
        "feature4": random.uniform(20, 60)    # Training mean ~1.18
    }
    
    response = requests.post(url, json=payload)
    print(f"Response {i+1}: {response.json()} - Payload: {payload}")
    
    # Optional: wait a short time between requests
    time.sleep(0.5)