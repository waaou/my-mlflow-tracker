import mlflow
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score
import os

# Load Iris dataset
iris = load_iris()

# Split dataset into X features and Target variable
X = pd.DataFrame(data = iris["data"], columns= iris["feature_names"])
y = pd.Series(data = iris["target"], name="target")


# Set tracking URI to your Hugging Face application
mlflow.set_tracking_uri(os.environ["APP_URI"])

model = mlflow.sklearn.load_model("models:/m-032f55432d0642c9ae9359c5d441916e")

y_pred=model.predict(X)
print(y_pred)

accuracy = accuracy_score(y, y_pred)
print(accuracy)