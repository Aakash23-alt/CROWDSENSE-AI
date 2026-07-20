from sqlalchemy.orm import Session
from backend.models import CrowdData
from backend.schemas import CrowdDataCreate


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
