from fastapi import APIRouter
from backend.database import SessionLocal
from backend.models import CrowdData
from backend.schemas import CrowdDataCreate
from backend.ai.predictor import predict_people
from backend.schemas import PredictionRequest
from backend.ai.predictor import predict_people

router = APIRouter()

# ✅ CREATE + SMART LOGIC
@router.post("/crowd-data")
def add_crowd_data(data: CrowdDataCreate):
    db = SessionLocal()

    data = data.dict()
    # 🔥 Risk Logic
    if data["people_count"] > 50:
        data["risk"] = "high"
    elif data["people_count"] > 20:
        data["risk"] = "medium"
    else:
        data["risk"] = "low"

    new_data = CrowdData(**data)

    db.add(new_data)
    db.commit()
    db.refresh(new_data)

    return new_data


# ✅ GET ALL
@router.get("/crowd-data")
def get_all_data():
    db = SessionLocal()
    return db.query(CrowdData).all()


# ✅ FILTER BY CAMERA
@router.get("/crowd-data/{camera_id}")
def get_by_camera(camera_id: str):
    db = SessionLocal()
    return db.query(CrowdData).filter(CrowdData.camera_id == camera_id).all()


# ✅ ALERTS (HIGH RISK)
@router.get("/alerts")
def get_alerts():
    db = SessionLocal()
    return db.query(CrowdData).filter(CrowdData.risk == "high").all()


# ✅ DELETE
@router.delete("/crowd-data/{id}")
def delete_data(id: int):
    db = SessionLocal()
    data = db.query(CrowdData).filter(CrowdData.id == id).first()

    if data:
        db.delete(data)
        db.commit()
        return {"message": "Deleted successfully"}
    return {"message": "Data not found"}

# 🤖 AI Prediction
@router.post("/predict")
def predict(data: PredictionRequest):

    future_people = predict_people(data.people_count)

    # Future risk prediction
    if future_people > 50:
        future_risk = "High"
        recommendation = "Open Gate 2 and Deploy Security"

    elif future_people > 20:
        future_risk = "Medium"
        recommendation = "Monitor Crowd"

    else:
        future_risk = "Low"
        recommendation = "No Action Needed"

    return {
        "current_people": data.people_count,
        "predicted_people": future_people,
        "future_risk": future_risk,
        "recommendation": recommendation
    }

@router.get("/dashboard")
def dashboard():
    db = SessionLocal()

    total = db.query(CrowdData).count()

    high = db.query(CrowdData).filter(
        CrowdData.risk=="high"
    ).count()

    medium = db.query(CrowdData).filter(
        CrowdData.risk=="medium"
    ).count()

    low = db.query(CrowdData).filter(
        CrowdData.risk=="low"
    ).count()

    latest = db.query(CrowdData).order_by(
        CrowdData.id.desc()
    ).first()

    return {
        "total_records": total,
        "high_risk": high,
        "medium_risk": medium,
        "low_risk": low,
        "latest_people_count": latest.people_count if latest else 0,
        "latest_camera": latest.camera_id if latest else None
    }
@router.get("/predict/latest")
def predict_latest():
    db = SessionLocal()

    latest = db.query(CrowdData).order_by(CrowdData.id.desc()).first()

    if not latest:
        return {"message": "No crowd data available"}

    predicted_people = predict_people(latest.people_count)

    if predicted_people > 50:
        future_risk = "High"
        recommendation = "Open Gate 2 and Deploy Security"
    elif predicted_people > 20:
        future_risk = "Medium"
        recommendation = "Monitor Crowd"
    else:
        future_risk = "Low"
        recommendation = "Crowd is Safe"

    return {
        "camera_id": latest.camera_id,
        "current_people": latest.people_count,
        "predicted_people": predicted_people,
        "future_risk": future_risk,
        "recommendation": recommendation
    }
