import requests
import json

# Load training stats
with open("monitoring/training_stats.json", "r") as f:
    stats = json.load(f)

trained_means = stats["means"]
trained_stds = stats["stds"]

# Prometheus endpoint
PROMETHEUS_URL = "http://localhost:9090/api/v1/query"

# Feature names used in Prometheus metrics
features = [
    "feature1_distribution",
    "feature2_distribution",
    "feature3_distribution",
    "feature4_distribution"
]

print("Fetching live stats from Prometheus...")

drift_detected = False

for i, feature in enumerate(features):
    # Correct: Use _sum and _count directly
    sum_query = f"{feature}_sum"
    count_query = f"{feature}_count"

    sum_resp = requests.get(PROMETHEUS_URL, params={"query": sum_query})
    count_resp = requests.get(PROMETHEUS_URL, params={"query": count_query})

    sum_val = float(sum_resp.json()["data"]["result"][0]["value"][1]) if sum_resp.json()["data"]["result"] else 0.0
    count_val = float(count_resp.json()["data"]["result"][0]["value"][1]) if count_resp.json()["data"]["result"] else 0.0

    # Avoid division by zero
    if count_val == 0:
        print(f"[WARNING] No data found yet for {feature}. Skipping.")
        continue

    live_mean = sum_val / count_val
    trained_mean = trained_means[i]

    # Compare means
    drift_threshold = 0.3 * trained_stds[i]  # 30% of std deviation
    if abs(live_mean - trained_mean) > drift_threshold:
        print(f"[ALERT] Drift detected in {feature}!")
        print(f"  Trained mean: {trained_mean:.4f}, Live mean: {live_mean:.4f}")
        drift_detected = True
    else:
        print(f"{feature}: ✅ No drift (Live: {live_mean:.4f}, Trained: {trained_mean:.4f})")

if not drift_detected:
    print("\n✅ No significant drift detected across all features.")