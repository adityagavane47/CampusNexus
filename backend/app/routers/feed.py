from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.utils.database import (
    create_project,
    get_all_projects,
    get_project_by_id,
    apply_to_project,
    hire_freelancer
)

router = APIRouter()

class ProjectCreate(BaseModel):

    title: str
    description: str
    skills_required: List[str]
    budget_algo: float
    deadline: str
    milestones: List[str]
    creator_id: str
    escrow_app_id: Optional[int] = None
    escrow_enabled: Optional[bool] = False
    client_wallet: Optional[str] = None
    num_milestones: Optional[int] = None
    enableEscrow: Optional[bool] = None

class ProjectResponse(BaseModel):

    id: int
    title: str
    description: str
    skills_required: List[str]
    budget_algo: float
    deadline: str
    milestones: List[str]
    creator_id: str
    creator_name: str
    creator_avatar: Optional[str]
    status: str
    created_at: str
    applications: List[dict]

class ApplicationRequest(BaseModel):

    applicant_id: str

@router.get("/", response_model=List[ProjectResponse])
async def list_projects(
    skill: Optional[str] = Query(None, description="Filter by skill"),
    min_budget: Optional[float] = Query(None, description="Minimum budget in ALGO"),
    status: Optional[str] = Query("open", description="Project status"),
    creator_id: Optional[str] = Query(None, description="Filter by creator ID")
):

    projects = get_all_projects()
    filtered = projects
    
    if skill:
        filtered = [p for p in filtered if skill.lower() in [s.lower() for s in p.get("skills_required", [])]]
    
    if min_budget:
        filtered = [p for p in filtered if p.get("budget_algo", 0) >= min_budget]
    
    if status:
        filtered = [p for p in filtered if p.get("status") == status]
    
    if creator_id:
        filtered = [p for p in filtered if p.get("creator_id") == creator_id]
    
    return filtered

@router.post("/", response_model=ProjectResponse)
async def create_new_project(project: ProjectCreate):

    new_project = create_project(project.model_dump())
    return new_project

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int):

    project = get_project_by_id(project_id)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return project

@router.post("/{project_id}/apply")
async def apply_to_project_endpoint(project_id: int, request: ApplicationRequest):

    project = apply_to_project(project_id, request.applicant_id)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or user not found")
    
    return {
        "message": "Application submitted successfully",
        "project_id": project_id,
        "applications_count": len(project.get("applications", []))
    }

class HireRequest(BaseModel):

    freelancer_id: str
    freelancer_wallet: str
    escrow_app_id: int

@router.post("/{project_id}/hire")
async def hire_applicant(project_id: int, request: HireRequest):

    project = hire_freelancer(
        project_id,
        request.freelancer_id,
        request.escrow_app_id,
        request.freelancer_wallet
    )
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {
        "message": "Freelancer hired successfully",
        "project_id": project_id,
        "status": project.get("status"),
        "escrow_app_id": project.get("escrow_app_id")
    }
