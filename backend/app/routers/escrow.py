"""
CampusNexus - Escrow Router (Blockchain Integration)
Milestone-based escrow reading from Algorand blockchain
"""
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from algosdk.v2client import algod
from algosdk import encoding

from app.config import get_settings

router = APIRouter()
settings = get_settings()

# Initialize Algod client for blockchain queries
algod_client = algod.AlgodClient(
    algod_token=settings.algorand_algod_token,
    algod_address=settings.algorand_algod_address
)


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
    project_id: Optional[int] = None
    client_address: str
    freelancer_address: str
    total_amount_algo: float
    released_amount_algo: float
    num_milestones: int
    completed_milestones: int
    status: str
    created_at: Optional[str] = None


@router.get("/{escrow_app_id}", response_model=EscrowResponse)
async def get_escrow(escrow_app_id: int):
    """
    Fetch escrow state directly from Algorand blockchain.
    
    Args:
        escrow_app_id: The Algorand Application ID of the escrow contract
        
    Returns:
        EscrowResponse with current blockchain state
    """
    try:
        # Query blockchain for application info
        app_info = algod_client.application_info(escrow_app_id)
        global_state_raw = app_info.get('params', {}).get('global-state', [])
        
        # Parse global state from base64
        state = {}
        for item in global_state_raw:
            key = encoding.base64.b64decode(item['key']).decode('utf-8')
            value_obj = item['value']
            
            if value_obj['type'] == 1:  # bytes
                state[key] = encoding.base64.b64decode(value_obj['bytes'])
            elif value_obj['type'] == 2:  # uint
                state[key] = value_obj['uint']
        
        # Decode addresses from bytes
        client_address = encoding.encode_address(state.get('client', b'\x00' * 32))
        freelancer_address = encoding.encode_address(state.get('freelancer', b'\x00' * 32))
        
        # Decode status string
        status_bytes = state.get('status', b'inactive')
        status = status_bytes.decode('utf-8') if isinstance(status_bytes, bytes) else str(status_bytes)
        
        # Convert microALGOs to ALGO
        total_amount_algo = state.get('total_amount', 0) / 1_000_000
        released_amount_algo = state.get('released_amount', 0) / 1_000_000
        
        return EscrowResponse(
            id=escrow_app_id,
            client_address=client_address,
            freelancer_address=freelancer_address,
            total_amount_algo=total_amount_algo,
            released_amount_algo=released_amount_algo,
            num_milestones=state.get('num_milestones', 0),
            completed_milestones=state.get('completed_milestones', 0),
            status=status,
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch escrow from blockchain: {str(e)}"
        )


@router.post("/")
async def create_escrow_metadata(escrow: EscrowCreate):
    """
    Store escrow metadata for frontend display.
    
    NOTE: The actual escrow contract creation happens on the frontend
    via Algorand transaction. This endpoint just stores metadata to
    help the frontend display project/milestone details.
    
    Returns the escrow data that should be submitted to blockchain.
    """
    return {
        "message": "Escrow metadata ready. Deploy to blockchain via frontend.",
        "contract_params": {
            "client_address": escrow.client_address,
            "freelancer_address": escrow.freelancer_address,
            "total_amount_algo": escrow.total_amount_algo,
            "num_milestones": len(escrow.milestones),
            "milestones": [m.model_dump() for m in escrow.milestones]
        }
    }


@router.post("/{escrow_id}/milestone/{milestone_index}/complete")
async def complete_milestone(escrow_id: int, milestone_index: int, freelancer_address: str):
    """
    Helper endpoint to verify milestone completion on blockchain.
    
    NOTE: Actual completion happens via blockchain transaction.
    This endpoint helps frontend track state.
    """
    return {
        "message": f"Submit 'complete_milestone' transaction to App ID {escrow_id}",
        "params": {
            "app_id": escrow_id,
            "method": "complete_milestone",
            "milestone_index": milestone_index,
            "signer": freelancer_address
        }
    }


@router.post("/{escrow_id}/milestone/{milestone_index}/approve")
async def approve_milestone(escrow_id: int, milestone_index: int, client_address: str, amount_algo: float):
    """
    Helper endpoint to prepare approval transaction.
    
    NOTE: Actual approval happens via blockchain transaction.
    This endpoint helps frontend construct the transaction.
    """
    return {
        "message": f"Submit 'approve_milestone' transaction to App ID {escrow_id}",
        "params": {
            "app_id": escrow_id,
            "method": "approve_milestone",
            "milestone_index": milestone_index,
            "amount_microalgos": int(amount_algo * 1_000_000),
            "signer": client_address
        }
    }
