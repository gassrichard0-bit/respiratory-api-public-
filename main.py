from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel
from typing import Optional
import uuid

app = FastAPI()

# Your API key (generate a secure one)
VALID_API_KEY = "hermes-api-key-12345"  # Change this to your secure key

# Data model for respiratory data
class RespiratoryData(BaseModel):
    respiratory_rate: int  # breaths per minute
    oxygen_saturation: Optional[float] = None  # SpO2 percentage
    temperature: Optional[float] = None
    user_id: str

# Store data in memory (use a database for production)
respiratory_records = []

# API Key verification
async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != VALID_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return x_api_key

# Add respiratory data
@app.post("/respiratory")
async def add_respiratory(data: RespiratoryData, api_key: str = Depends(verify_api_key)):
    record = {
        "id": str(uuid.uuid4()),
        "respiratory_rate": data.respiratory_rate,
        "oxygen_saturation": data.oxygen_saturation,
        "temperature": data.temperature,
        "user_id": data.user_id
    }
    respiratory_records.append(record)
    return {"status": "success", "record": record}

# Get all respiratory data
@app.get("/respiratory")
async def get_respiratory(api_key: str = Depends(verify_api_key)):
    return {"data": respiratory_records}

# Get respiratory data by user
@app.get("/respiratory/{user_id}")
async def get_user_respiratory(user_id: str, api_key: str = Depends(verify_api_key)):
    user_data = [r for r in respiratory_records if r["user_id"] == user_id]
    return {"user_id": user_id, "data": user_data}

@app.get("/")
async def root():
    return {"message": "Hermes Respiratory API"}