from pydantic import BaseModel

class CrowdDataCreate(BaseModel):
    camera_id: str
    people_count: int
    density: str

class PredictionRequest(BaseModel):
    people_count: int  
