"""
CampusNexus - Escrow Router
Milestone-based escrow for freelancing
"""
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# In-memory store (replace with smart contract in production)
escrows_db: list[dict] = []


class MilestoneCreate(BaseModel):
    """Milestone definition."""
    title: str
    description: str
    amount_algo: float


class EscrowCreate(BaseModel):
    """Request model for creating an escrow."""
    project_id: int
    client_address: str
    freelancer_address: str
    total_amount_algo: float
    milestones: list[MilestoneCreate]


class EscrowResponse(BaseModel):
    """Response model for an escrow."""
    id: int
    project_id: int
    client_address: str
    freelancer_address: str
    total_amount_algo: float
    milestones: list[dict]
    status: str
    created_at: str


@router.post("/", response_model=EscrowResponse)
async def create_escrow(escrow: EscrowCreate):
    """
    Create a milestone-based escrow contract.
    In production, this will deploy an Algorand smart contract.
    """
    milestones_with_status = [
        {
            **m.model_dump(),
            "status": "pending",
            "completed_at": None,
            "approved_at": None,
        }
        for m in escrow.milestones
    ]
    
    new_escrow = {
        "id": len(escrows_db) + 1,
        "project_id": escrow.project_id,
        "client_address": escrow.client_address,
        "freelancer_address": escrow.freelancer_address,
        "total_amount_algo": escrow.total_amount_algo,
        "milestones": milestones_with_status,
        "status": "active",
        "created_at": datetime.utcnow().isoformat(),
    }
    
    escrows_db.append(new_escrow)
    return new_escrow


@router.get("/{escrow_id}", response_model=EscrowResponse)
async def get_escrow(escrow_id: int):
    """Get escrow details by ID."""
    for escrow in escrows_db:
        if escrow["id"] == escrow_id:
            return escrow
    raise HTTPException(status_code=404, detail="Escrow not found")


@router.post("/{escrow_id}/milestone/{milestone_index}/complete")
async def complete_milestone(escrow_id: int, milestone_index: int, freelancer_address: str):
    """Mark a milestone as complete (by freelancer)."""
    for escrow in escrows_db:
        if escrow["id"] == escrow_id:
            if escrow["freelancer_address"] != freelancer_address:
                raise HTTPException(status_code=403, detail="Only freelancer can complete milestones")
            
            if milestone_index >= len(escrow["milestones"]):
                raise HTTPException(status_code=400, detail="Invalid milestone index")
            
            escrow["milestones"][milestone_index]["status"] = "completed"
            escrow["milestones"][milestone_index]["completed_at"] = datetime.utcnow().isoformat()
            
            return {"message": "Milestone marked as complete", "milestone": escrow["milestones"][milestone_index]}
    
    raise HTTPException(status_code=404, detail="Escrow not found")


@router.post("/{escrow_id}/milestone/{milestone_index}/approve")
async def approve_milestone(escrow_id: int, milestone_index: int, client_address: str):
    """Approve a milestone and release funds (by client)."""
    for escrow in escrows_db:
        if escrow["id"] == escrow_id:
            if escrow["client_address"] != client_address:
                raise HTTPException(status_code=403, detail="Only client can approve milestones")
            
            milestone = escrow["milestones"][milestone_index]
            if milestone["status"] != "completed":
                raise HTTPException(status_code=400, detail="Milestone not marked as complete")
            
            milestone["status"] = "approved"
            milestone["approved_at"] = datetime.utcnow().isoformat()
            
            # Check if all milestones are approved
            all_approved = all(m["status"] == "approved" for m in escrow["milestones"])
            if all_approved:
                escrow["status"] = "completed"
            
            return {
                "message": f"Milestone approved. {milestone['amount_algo']} ALGO released.",
                "milestone": milestone
            }
    
    raise HTTPException(status_code=404, detail="Escrow not found")
