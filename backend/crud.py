from sqlalchemy.orm import Session
from app.models import CrowdData
from app.schemas import CrowdDataCreate


def create_crowd_data(db: Session, crowd: CrowdDataCreate):
    db_data = CrowdData(
        camera_id=crowd.camera_id,
        people_count=crowd.people_count,
        density=crowd.density,
        risk=crowd.risk
    )

    db.add(db_data)
    db.commit()
    db.refresh(db_data)

    return db_data