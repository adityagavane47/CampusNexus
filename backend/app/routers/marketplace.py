from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, Query, File, UploadFile
from pydantic import BaseModel

from app.utils.ipfs import upload_to_ipfs, get_ipfs_url
from app.utils.database import (
    get_all_listings, 
    create_listing as create_db_listing,
    update_listing_status
)

router = APIRouter()

class ListingCreate(BaseModel):

    title: str
    description: str
    category: str
    price_algo: float
    condition: str
    ipfs_cid: str = ""
    seller_address: str

class ListingResponse(BaseModel):

    id: int
    title: str
    description: str
    category: str
    price_algo: float
    condition: str
    ipfs_cid: str
    seller_address: str
    status: str
    created_at: str

class PurchaseRequest(BaseModel):

    buyer_address: str

@router.post("/upload-image")
async def upload_listing_image(file: UploadFile = File(...)):

    result = await upload_to_ipfs(file)
    
    return {
        "cid": result["cid"],
        "gateway_url": result["gateway_url"],
        "size_bytes": result["size"]
    }

@router.get("/", response_model=list[ListingResponse])
async def list_items(
    category: Optional[str] = Query(None, description="Filter by category"),
    max_price: Optional[float] = Query(None, description="Maximum price in ALGO"),
    condition: Optional[str] = Query(None, description="Item condition")
):

    listings = get_all_listings()
    filtered = [l for l in listings if l["status"] == "available"]
    
    if category and category != "all":
        filtered = [l for l in filtered if l["category"].lower() == category.lower()]
    
    if max_price:
        filtered = [l for l in filtered if l["price_algo"] <= max_price]
    
    if condition:
        filtered = [l for l in filtered if l["condition"] == condition]
    
    return filtered

@router.post("/", response_model=ListingResponse)
async def create_listing(listing: ListingCreate):

    new_listing = create_db_listing(listing.model_dump())
    return new_listing

@router.get("/{listing_id}", response_model=ListingResponse)
async def get_listing(listing_id: int):

    listings = get_all_listings()
    for listing in listings:
        if listing["id"] == listing_id:
            return listing
    raise HTTPException(status_code=404, detail="Listing not found")

@router.post("/{listing_id}/purchase")
async def purchase_item(listing_id: int, request: PurchaseRequest):

    listings = get_all_listings()
    for listing in listings:
        if listing["id"] == listing_id:
            if listing["status"] != "available":
                raise HTTPException(status_code=400, detail="Item not available")
            
            if listing["seller_address"] == request.buyer_address:
                raise HTTPException(status_code=400, detail="Cannot buy your own item")
            
            update_listing_status(listing_id, "pending")
            
            listing["status"] = "pending"
            
            return {
                "success": True,
                "message": "Purchase initiated",
                "listing": listing,
                "escrow_required": listing["price_algo"],
                "seller_address": listing["seller_address"],
            }
    
    raise HTTPException(status_code=404, detail="Listing not found")

@router.get("/categories/list")
async def list_categories():

    return {
        "categories": [
            {"id": "arduino", "name": "Arduino & Electronics", "icon": "🔌"},
            {"id": "books", "name": "Books & Notes", "icon": "📚"},
            {"id": "laptops", "name": "Laptops & Computers", "icon": "💻"},
            {"id": "components", "name": "Electronic Components", "icon": "🔧"},
            {"id": "lab_equipment", "name": "Lab Equipment", "icon": "🔬"},
            {"id": "other", "name": "Other", "icon": "📦"},
        ]
    }

class ListingCreate(BaseModel):

    title: str
    description: str
    category: str
    price_algo: float
    condition: str
    ipfs_cid: str = ""
    seller_address: str

class ListingResponse(BaseModel):

    id: int
    title: str
    description: str
    category: str
    price_algo: float
    condition: str
    ipfs_cid: str
    seller_address: str
    status: str
    created_at: str

@router.post("/upload-image")
async def upload_listing_image(file: UploadFile = File(...)):

    result = await upload_to_ipfs(file)
    
    return {
        "cid": result["cid"],
        "gateway_url": result["gateway_url"],
        "size_bytes": result["size"]
    }

@router.get("/", response_model=list[ListingResponse])
async def list_items(
    category: Optional[str] = Query(None, description="Filter by category"),
    max_price: Optional[float] = Query(None, description="Maximum price in ALGO"),
    condition: Optional[str] = Query(None, description="Item condition")
):

    filtered = [l for l in listings_db if l["status"] == "available"]
    
    if category:
        filtered = [l for l in filtered if l["category"].lower() == category.lower()]
    
    if max_price:
        filtered = [l for l in filtered if l["price_algo"] <= max_price]
    
    if condition:
        filtered = [l for l in filtered if l["condition"] == condition]
    
    return filtered

@router.post("/", response_model=ListingResponse)
async def create_listing(listing: ListingCreate):

    new_listing = {
        "id": len(listings_db) + 1,
        **listing.model_dump(),
        "status": "available",
        "created_at": datetime.utcnow().isoformat(),
    }
    
    listings_db.append(new_listing)
    return new_listing

@router.get("/{listing_id}", response_model=ListingResponse)
async def get_listing(listing_id: int):

    for listing in listings_db:
        if listing["id"] == listing_id:
            return listing
    raise HTTPException(status_code=404, detail="Listing not found")

class PurchaseRequest(BaseModel):

    buyer_address: str

@router.post("/{listing_id}/purchase")
async def purchase_item(listing_id: int, request: PurchaseRequest):

    for listing in listings_db:
        if listing["id"] == listing_id:
            if listing["status"] != "available":
                raise HTTPException(status_code=400, detail="Item not available")
            
            if listing["seller_address"] == request.buyer_address:
                raise HTTPException(status_code=400, detail="Cannot buy your own item")
            
            listing["status"] = "pending"
            
            return {
                "success": True,
                "message": "Purchase initiated",
                "listing": listing,
                "escrow_required": listing["price_algo"],
                "seller_address": listing["seller_address"],
            }
    
    raise HTTPException(status_code=404, detail="Listing not found")

@router.get("/categories/list")
async def list_categories():

    return {
        "categories": [
            {"id": "arduino", "name": "Arduino & Electronics", "icon": "🔌"},
            {"id": "books", "name": "Books & Notes", "icon": "📚"},
            {"id": "laptops", "name": "Laptops & Computers", "icon": "💻"},
            {"id": "components", "name": "Electronic Components", "icon": "🔧"},
            {"id": "lab_equipment", "name": "Lab Equipment", "icon": "🔬"},
            {"id": "other", "name": "Other", "icon": "📦"},
        ]
    }
