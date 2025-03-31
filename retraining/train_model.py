# 1. Import libraries
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
import os
import json
import numpy as np

# 2. Load the dataset
iris = load_iris()
X = iris.data        # Features: petal length, sepal width, etc.
y = iris.target      # Labels: 0 = Setosa, 1 = Versicolor, 2 = Virginica

# 3. Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4. Train the model
clf = RandomForestClassifier()
clf.fit(X_train, y_train)

# 5. Make predictions and evaluate
preds = clf.predict(X_test)
acc = accuracy_score(y_test, preds)
print(f"Model Accuracy: {acc:.2f}")

# 6. Save the trained model
os.makedirs("model", exist_ok=True)  # creates folder if it doesn't exist
with open("model/model_v1.pkl", "wb") as f:
    pickle.dump(clf, f)

# Save training stats
feature_means = np.mean(X_train, axis=0).tolist()
feature_stds = np.std(X_train, axis=0).tolist()

with open("monitoring/training_stats.json", "w") as f:
    json.dump({"means": feature_means, "stds": feature_stds}, f)