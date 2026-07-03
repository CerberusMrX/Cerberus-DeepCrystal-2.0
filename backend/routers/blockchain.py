"""
Blockchain verification router for Cerberus DeepCrystal
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, BlockchainCert

router = APIRouter()


@router.get("/verify/{cert_id}")
async def verify_certificate(cert_id: str, db: Session = Depends(get_db)):
    cert = db.query(BlockchainCert).filter(BlockchainCert.cert_id == cert_id).first()
    if not cert:
        raise HTTPException(status_code=404, detail=f"Certificate {cert_id} not found in the Cerberus DeepCrystal ledger.")
    return {
        "cert_id": cert.cert_id,
        "mineral_name": cert.mineral_name,
        "confidence_score": cert.confidence_score,
        "hash_value": cert.hash_value,
        "issued_at": cert.issued_at.isoformat(),
        "is_valid": cert.is_valid,
        "qr_code_url": cert.qr_path
    }


@router.get("/all")
async def list_certificates(limit: int = 50, db: Session = Depends(get_db)):
    certs = db.query(BlockchainCert).order_by(BlockchainCert.issued_at.desc()).limit(limit).all()
    return [
        {
            "cert_id": c.cert_id,
            "mineral_name": c.mineral_name,
            "confidence_score": c.confidence_score,
            "issued_at": c.issued_at.isoformat(),
            "is_valid": c.is_valid
        }
        for c in certs
    ]
