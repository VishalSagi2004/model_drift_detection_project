from fastapi import FastAPI
import pickle
import numpy as np
from pydantic import BaseModel
from prometheus_client import Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

# Load the model
with open("model/model_v1.pkl", "rb") as f:
    model = pickle.load(f)

# Define input schema
class InputData(BaseModel):
    feature1: float
    feature2: float
    feature3: float
    feature4: float

# Create the FastAPI app
app = FastAPI()

# Define Prometheus histograms for each feature
feature1_hist = Histogram("feature1_distribution", "Distribution of feature1")
feature2_hist = Histogram("feature2_distribution", "Distribution of feature2")
feature3_hist = Histogram("feature3_distribution", "Distribution of feature3")
feature4_hist = Histogram("feature4_distribution", "Distribution of feature4")

@app.get("/")
def read_root():
    return {"message": "Model is up and running!"}

@app.post("/predict")
def predict(data: InputData):
    # Log real user input to Prometheus
    feature1_hist.observe(data.feature1)
    feature2_hist.observe(data.feature2)
    feature3_hist.observe(data.feature3)
    feature4_hist.observe(data.feature4)

    # Make prediction
    features = np.array([[data.feature1, data.feature2, data.feature3, data.feature4]])
    prediction = model.predict(features)
    return {"prediction": int(prediction[0])}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
