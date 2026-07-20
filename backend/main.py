from fastapi import FastAPI
from backend.database import engine, Base
from backend.routers import crowd

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Include router
app.include_router(crowd.router)

@app.get("/")
def home():
    return {"message": "CrowdSense AI Backend Running"}
