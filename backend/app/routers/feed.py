"""
CampusNexus - Project Feed Router
Endpoints for student project/gig opportunities
"""
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

router = APIRouter()


# In-memory store (replace with database in production)
projects_db: list[dict] = []


class ProjectCreate(BaseModel):
    """Request model for creating a project."""
    title: str
    description: str
    skills_required: list[str]
    budget_algo: float
    deadline: str
    milestones: list[str]
    creator_address: str


class ProjectResponse(BaseModel):
    """Response model for a project."""
    id: int
    title: str
    description: str
    skills_required: list[str]
    budget_algo: float
    deadline: str
    milestones: list[str]
    creator_address: str
    status: str
    created_at: str
    applications_count: int


@router.get("/", response_model=list[ProjectResponse])
async def list_projects(
    skill: Optional[str] = Query(None, description="Filter by skill"),
    min_budget: Optional[float] = Query(None, description="Minimum budget in ALGO"),
    status: Optional[str] = Query("open", description="Project status")
):
    """
    List all available projects/gigs.
    Supports filtering by skill, budget, and status.
    """
    filtered = projects_db
    
    if skill:
        filtered = [p for p in filtered if skill.lower() in [s.lower() for s in p["skills_required"]]]
    
    if min_budget:
        filtered = [p for p in filtered if p["budget_algo"] >= min_budget]
    
    if status:
        filtered = [p for p in filtered if p["status"] == status]
    
    return filtered


@router.post("/", response_model=ProjectResponse)
async def create_project(project: ProjectCreate):
    """
    Create a new project/gig opportunity.
    """
    new_project = {
        "id": len(projects_db) + 1,
        **project.model_dump(),
        "status": "open",
        "created_at": datetime.utcnow().isoformat(),
        "applications_count": 0,
    }
    
    projects_db.append(new_project)
    
    return new_project


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int):
    """Get a specific project by ID."""
    for project in projects_db:
        if project["id"] == project_id:
            return project
    
    raise HTTPException(status_code=404, detail="Project not found")


@router.post("/{project_id}/apply")
async def apply_to_project(project_id: int, applicant_address: str):
    """Apply to a project as a freelancer."""
    for project in projects_db:
        if project["id"] == project_id:
            project["applications_count"] += 1
            return {"message": "Application submitted", "project_id": project_id}
    
    raise HTTPException(status_code=404, detail="Project not found")
