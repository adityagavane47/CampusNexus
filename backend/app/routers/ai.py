"""
CampusNexus - AI Router
Endpoints for AI features (Skill Matcher, Hustle Score verification)
"""
from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from typing import List

from app.services.ai_matching import rank_projects
# Import database function instead of in-memory variable
from app.utils.database import get_all_projects

router = APIRouter(
    prefix="/ai",
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
    """
    AI Skill-Matcher: Match user skills with available projects.
    Returns a list of projects ranked by relevance score.
    """
    if not request.skills:
        raise HTTPException(status_code=400, detail="Skills list cannot be empty")
    
    # Fetch projects from database
    projects = get_all_projects()
    ranked_projects = rank_projects(request.skills, projects)
    
    # Format response
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
