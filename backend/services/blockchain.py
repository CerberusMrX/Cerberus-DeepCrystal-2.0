"""
Blockchain Certification Service for Cerberus DeepCrystal
Generates tamper-proof certification IDs, hashes, and QR codes.
Author: Sudeepa Wanigarathna
"""

import hashlib
import uuid
import qrcode
import json
import os
from datetime import datetime
from pathlib import Path


def generate_cert_id() -> str:
    return f"CDC-{uuid.uuid4().hex[:8].upper()}-{uuid.uuid4().hex[:4].upper()}"


def generate_blockchain_hash(cert_id: str, mineral_name: str, confidence: float, timestamp: str) -> str:
    """
    Creates a SHA-256 fingerprint of the certificate data.
    In production this would be anchored to a real blockchain (e.g., Ethereum/Polygon).
    """
    payload = json.dumps({
        "cert_id": cert_id,
        "mineral_name": mineral_name,
        "confidence": confidence,
        "issued_at": timestamp,
        "issuer": "Cerberus DeepCrystal v1.0",
        "author": "Sudeepa Wanigarathna"
    }, sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()


def generate_qr_code(cert_id: str, mineral_name: str, hash_val: str) -> str:
    """
    Generates a QR code image containing the verification URL.
    Returns the relative path to the saved QR image.
    """
    Path("static/qrcodes").mkdir(parents=True, exist_ok=True)
    verification_url = f"https://deepcrystal.cerberus.ai/verify/{cert_id}"
    qr_data = json.dumps({
        "cert_id": cert_id,
        "mineral": mineral_name,
        "hash": hash_val,
        "verify": verification_url
    })

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#0a0a0a", back_color="#f0f4ff")

    filename = f"{cert_id}.png"
    filepath = f"static/qrcodes/{filename}"
    img.save(filepath)

    return f"/static/qrcodes/{filename}"


def generate_certification(
    session_id: str,
    mineral_name: str,
    confidence_score: float
) -> dict:
    """
    Full certification cycle: ID → Hash → QR → Result dict
    """
    cert_id = generate_cert_id()
    now = datetime.utcnow().isoformat() + "Z"
    hash_val = generate_blockchain_hash(cert_id, mineral_name, confidence_score, now)
    qr_path = generate_qr_code(cert_id, mineral_name, hash_val)
    verification_url = f"https://deepcrystal.cerberus.ai/verify/{cert_id}"

    return {
        "cert_id": cert_id,
        "session_id": session_id,
        "mineral_name": mineral_name,
        "confidence_score": confidence_score,
        "hash_value": hash_val,
        "qr_path": qr_path,
        "verification_url": verification_url,
        "issued_at": now,
        "is_valid": True
    }
