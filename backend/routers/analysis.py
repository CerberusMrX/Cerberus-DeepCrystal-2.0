"""
Analysis router for Cerberus DeepCrystal
Handles image upload and manual data input for gem analysis.
Author: Sudeepa Wanigarathna
"""

from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional, List
import uuid
import json
from datetime import datetime

from database import get_db, AnalysisReport, init_db
from models.schemas import AnalysisResponse, ManualInputs
from services.ml_pipeline import analyze_image
from services.blockchain import generate_certification

router = APIRouter()

# Initialize DB on first import
init_db()


@router.post("/scan", response_model=AnalysisResponse)
async def scan_gemstone(
    image: Optional[UploadFile] = File(None),
    manual_data: Optional[str] = Form(None),  # JSON string
    mode: str = Form("pro"),
    db: Session = Depends(get_db)
):
    """
    Primary analysis endpoint.
    Accepts image upload + optional manual gemological test inputs.
    Returns full forensic report.
    """
    if image is None:
        raise HTTPException(status_code=400, detail="At least one image is required for analysis.")

    image_bytes = await image.read()
    if len(image_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded image is empty.")

    # Parse manual inputs
    manual_inputs_dict = {}
    if manual_data:
        try:
            manual_inputs_dict = json.loads(manual_data)
        except Exception:
            manual_inputs_dict = {}

    # Run ML pipeline
    result = analyze_image(image_bytes, manual_inputs_dict)
    gem = result["gem"]
    gem_name = result["gem_key"]

    # Generate session + blockchain cert
    session_id = str(uuid.uuid4())
    cert = generate_certification(session_id, gem_name, result["base_confidence"])

    # Build response
    response = AnalysisResponse(
        session_id=session_id,
        blockchain_id=cert["cert_id"],
        mineral_name=gem_name,
        common_name=gem_name,
        chemical_formula=gem["formula"],
        crystal_system=gem["crystal_system"],
        mohs_hardness=f"{gem['mohs'][0]}" if gem['mohs'][0] == gem['mohs'][1] else f"{gem['mohs'][0]}–{gem['mohs'][1]}",
        specific_gravity=f"{gem['sg'][0]:.2f}–{gem['sg'][1]:.2f}",
        geological_class=gem["geological_class"],
        optical_properties={
            "refractive_index": f"{result['ri'][0]:.3f}–{result['ri'][1]:.3f}" if result['ri'][0] is not None else "N/A (Opaque/Metallic)",
            "birefringence": round(result['ri'][1] - result['ri'][0], 4) if result['ri'][0] is not None else None,
            "pleochroism": manual_inputs_dict.get("pleochroism", "Variable"),
            "luster": gem["luster"],
            "transparency": gem["transparency"],
            "dispersion": None
        },
        natural_probability=result["natural_prob"],
        synthetic_probability=result["synthetic_prob"],
        treatment_analysis={
            **result["treatment_probs"]
        },
        inclusion_analysis={
            **result["inclusion_data"]
        },
        crack_assessment={
            **result["crack_data"]
        },
        color_analysis={
            **result["color_analysis"]
        },
        price_estimation={
            **result["price"]
        },
        origin_predictions=result["origins"],
        confidence_score=result["base_confidence"],
        method_used=["CNN (Simulated EfficientNet-B7)", "Vision Transformer", "YOLO v8 (Inclusion Detection)", "GAN Anomaly Detector", "Ensemble Regression"],
        recommendations=result["recommendations"],
        disclaimer="⚠️ AI Screening Result. For high-value transactions, professional laboratory testing is recommended.",
        mode=mode,
        analysis_timestamp=datetime.utcnow(),
        qr_code_url=cert["qr_path"]
    )

    # Persist to DB
    report = AnalysisReport(
        session_id=session_id,
        blockchain_id=cert["cert_id"],
        mineral_name=gem_name,
        chemical_formula=gem["formula"],
        crystal_system=gem["crystal_system"],
        mohs_hardness=f"{gem['mohs'][0]}–{gem['mohs'][1]}",
        specific_gravity=manual_inputs_dict.get("specific_gravity"),
        natural_probability=result["natural_prob"],
        synthetic_probability=result["synthetic_prob"],
        treatment_probability=result["treatment_probs"].get("heat_treated", 0),
        treatment_type=result["treatment_probs"]["dominant_treatment"],
        inclusion_analysis=result["inclusion_data"],
        crack_assessment=result["crack_data"],
        price_min_local=result["price"]["min_local"],
        price_max_local=result["price"]["max_local"],
        price_min_usd=result["price"]["min_usd"],
        price_max_usd=result["price"]["max_usd"],
        currency_local="LKR",
        origin_prediction=result["origins"],
        confidence_score=result["base_confidence"],
        mode=mode
    )
    db.add(report)
    db.commit()

    return response


@router.get("/history")
async def get_analysis_history(limit: int = 20, db: Session = Depends(get_db)):
    """Return the last N analysis reports."""
    reports = db.query(AnalysisReport).order_by(AnalysisReport.created_at.desc()).limit(limit).all()
    return [
        {
            "session_id": r.session_id,
            "blockchain_id": r.blockchain_id,
            "mineral_name": r.mineral_name,
            "confidence_score": r.confidence_score,
            "natural_probability": r.natural_probability,
            "treatment_type": r.treatment_type,
            "price_min_usd": r.price_min_usd,
            "price_max_usd": r.price_max_usd,
            "mode": r.mode,
            "created_at": r.created_at.isoformat()
        }
        for r in reports
    ]


@router.get("/report/{session_id}")
async def get_report(session_id: str, db: Session = Depends(get_db)):
    """Retrieve a specific analysis report by session ID."""
    report = db.query(AnalysisReport).filter(AnalysisReport.session_id == session_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found.")
    return report
