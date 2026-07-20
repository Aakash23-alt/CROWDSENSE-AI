import joblib

model = joblib.load("app/ai/crowd_model.pkl")

def predict_people(current_people):
    prediction = model.predict([[current_people]])
    return int(prediction[0])