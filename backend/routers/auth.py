"""
Auth router for Cerberus DeepCrystal (subscription tiers)
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

TIERS = {
    "free": {"name": "Free Basic Scan", "scans_per_day": 3, "features": ["Basic ID", "Confidence Score"]},
    "pro": {"name": "Pro Trader Mode", "scans_per_day": 50, "features": ["Full Treatment Analysis", "Price Estimation", "Origin Prediction", "QR Certificate", "History"]},
    "lab": {"name": "Laboratory License", "scans_per_day": -1, "features": ["All Pro Features", "Spectral Data Input", "Research Mode", "Priority Support", "API Access", "Export Reports"]},
    "api": {"name": "API Integration for Jewelers", "scans_per_day": -1, "features": ["REST API Access", "Batch Processing", "Webhook Notifications"]},
    "gov": {"name": "Government Regulatory Module", "scans_per_day": -1, "features": ["Audit Logs", "Regulatory Compliance Reports", "Multi-user Management", "Blockchain Registry Access"]},
}


class RegisterRequest(BaseModel):
    username: str
    email: str
    tier: str = "free"


@router.get("/tiers")
def get_tiers():
    return TIERS


@router.post("/register")
def register(req: RegisterRequest):
    if req.tier not in TIERS:
        raise HTTPException(status_code=400, detail=f"Invalid tier. Choose from: {list(TIERS.keys())}")
    return {
        "message": f"Welcome to Cerberus DeepCrystal, {req.username}!",
        "tier": TIERS[req.tier]["name"],
        "features": TIERS[req.tier]["features"],
        "author": "Sudeepa Wanigarathna",
        "note": "Demo mode: no authentication required. Production requires JWT integration."
    }
