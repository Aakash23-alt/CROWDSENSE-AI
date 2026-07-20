import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

# Sample training data
data = {
    "current_people": [5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
    "future_people":  [8, 15, 28, 42, 55, 68, 80, 95,110,125,140]
}

df = pd.DataFrame(data)

X = df[["current_people"]]
y = df["future_people"]

model = LinearRegression()
model.fit(X, y)

joblib.dump(model, "app/ai/crowd_model.pkl")

print("✅ AI Model Trained Successfully!")
