import requests
import time

# URL for your /predict endpoint
url = "http://127.0.0.1:8000/predict"

# Define the payload with extreme values (simulate drift)
payload = {
    "feature1": 999,
    "feature2": 888,
    "feature3": 777,
    "feature4": 666
}

# Number of requests to send
num_requests = 15

for i in range(num_requests):
    response = requests.post(url, json=payload)
    print(f"Response {i+1}: {response.json()}")
    # Optional: wait a short time between requests
    time.sleep(0.5)