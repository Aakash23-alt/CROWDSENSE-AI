from sqlalchemy import Column, Integer, String
from app.database import Base

class CrowdData(Base):
    __tablename__ = "crowd_data"

    id = Column(Integer, primary_key=True, index=True)
    camera_id = Column(String)
    people_count = Column(Integer)
    density = Column(String)
    risk = Column(String)