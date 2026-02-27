from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services import hustle_score

router = APIRouter(prefix="/api/hustle", tags=["hustle"])

class ScoreResponse(BaseModel):

    wallet_address: str
    score: int
    initialized: bool

@router.get("/score/{wallet_address}", response_model=ScoreResponse)
async def get_student_score(wallet_address: str):

    try:
        score = await hustle_score.get_student_score(wallet_address)
        return ScoreResponse(
            wallet_address=wallet_address,
            score=score,
            initialized=score > 0
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching score: {str(e)}")

@router.post("/initialize/{wallet_address}")
async def initialize_student(wallet_address: str):

    try:
        already_initialized = await hustle_score.ensure_student_initialized(wallet_address)
        
        if already_initialized:
            return {"message": "Student already initialized", "wallet_address": wallet_address}
        else:
            return {"message": "Student initialized successfully", "wallet_address": wallet_address}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error initializing student: {str(e)}")

@router.post("/add-points/{wallet_address}")
async def add_reputation(wallet_address: str, points: int = 10):

    try:
        tx_id = await hustle_score.add_reputation_points(wallet_address, points)
        new_score = await hustle_score.get_student_score(wallet_address)
        
        return {
            "message": f"Added {points} points successfully",
            "wallet_address": wallet_address,
            "new_score": new_score,
            "transaction_id": tx_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding reputation: {str(e)}")
