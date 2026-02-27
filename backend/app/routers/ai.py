from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from typing import List

from app.services.ai_matching import rank_projects
from app.utils.database import get_all_projects

router = APIRouter(
    tags=["ai"],
)

class MatchRequest(BaseModel):
    skills: List[str]

class MatchResponse(BaseModel):
    project_id: int
    title: str
    match_score: float
    skills_required: List[str]

@router.post("/match", response_model=List[MatchResponse])
async def match_projects(request: MatchRequest):

    if not request.skills:
        raise HTTPException(status_code=400, detail="Skills list cannot be empty")
    
    projects = get_all_projects()
    ranked_projects = rank_projects(request.skills, projects)
    
    results = [
        MatchResponse(
            project_id=p["id"],
            title=p["title"],
            match_score=p["match_score"],
            skills_required=p["skills_required"]
        )
        for p in ranked_projects
    ]
    
    return results
