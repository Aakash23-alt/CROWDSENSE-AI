from fastapi import FastAPI
from app.database import engine, Base
from app.routers import crowd

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Include router
app.include_router(crowd.router)

@app.get("/")
def home():
    return {"message": "CrowdSense AI Backend Running"}