"""
Pydantic schemas for Cerberus DeepCrystal API
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ManualInputs(BaseModel):
    refractive_index: Optional[float] = None
    specific_gravity: Optional[float] = None
    pleochroism: Optional[str] = None
    magnetism: Optional[str] = None
    streak: Optional[str] = None
    hardness_result: Optional[float] = None
    carat_weight: Optional[float] = None
    uv_fluorescence: Optional[str] = None


class InclusionAnalysis(BaseModel):
    curved_growth_lines: float = 0.0
    gas_bubbles: float = 0.0
    rutile_silk: float = 0.0
    fracture_filling: float = 0.0
    flame_fusion_indicators: float = 0.0
    heat_treatment_markers: float = 0.0
    fingerprint_inclusions: float = 0.0
    needles: float = 0.0
    crystals: float = 0.0
    feathers: float = 0.0
    summary: str = ""


class CrackAssessment(BaseModel):
    surface_cracks: float = 0.0
    internal_fractures: float = 0.0
    chips: float = 0.0
    abrasions: float = 0.0
    overall_clarity_grade: str = ""
    damage_description: str = ""


class OriginPrediction(BaseModel):
    country: str
    probability: float


class TreatmentAnalysis(BaseModel):
    natural: float
    heat_treated: float
    diffusion_treated: float
    glass_filled: float
    resin_filled: float
    laser_drilled: float
    coated: float
    synthetic: float
    dominant_treatment: str


class ColorAnalysis(BaseModel):
    dominant_hex: str
    palette_hex: List[str]
    hue: float
    saturation: float
    lightness: float
    color_quality_score: float
    description: str


class PriceEstimation(BaseModel):
    min_usd: float
    max_usd: float
    min_local: float
    max_local: float
    currency_local: str = "LKR"
    per_carat: bool = True
    factors: List[str] = []


class OpticalProperties(BaseModel):
    refractive_index: str = ""
    birefringence: Optional[float] = None
    pleochroism: Optional[str] = None
    luster: str = ""
    transparency: str = ""
    dispersion: Optional[float] = None


class AnalysisRequest(BaseModel):
    manual_inputs: Optional[ManualInputs] = None
    mode: str = "pro"  # free, pro, lab


class AnalysisResponse(BaseModel):
    session_id: str
    blockchain_id: str
    mineral_name: str
    common_name: Optional[str] = None
    chemical_formula: str
    crystal_system: str
    mohs_hardness: str
    specific_gravity: str
    geological_class: str
    optical_properties: OpticalProperties
    natural_probability: float
    synthetic_probability: float
    treatment_analysis: TreatmentAnalysis
    inclusion_analysis: InclusionAnalysis
    crack_assessment: CrackAssessment
    color_analysis: ColorAnalysis
    price_estimation: PriceEstimation
    origin_predictions: List[OriginPrediction]
    confidence_score: float
    method_used: List[str]
    recommendations: List[str]
    disclaimer: str
    mode: str
    analysis_timestamp: datetime
    qr_code_url: Optional[str] = None


class MineralDB(BaseModel):
    name: str
    chemical_formula: str
    crystal_system: str
    mohs_hardness_min: float
    mohs_hardness_max: float
    specific_gravity_min: float
    specific_gravity_max: float
    luster: str
    cleavage: str
    fracture: str
    streak: str
    color: str
    refractive_index_min: Optional[float] = None
    refractive_index_max: Optional[float] = None
    common_treatments: Optional[str] = None
    synthetic_methods: Optional[str] = None
    known_origins: Optional[str] = None
    price_min_usd: Optional[float] = None
    price_max_usd: Optional[float] = None
    geological_class: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    uv_fluorescence: Optional[str] = None
    inclusion_patterns: Optional[str] = None

    class Config:
        from_attributes = True


class BlockchainCertResponse(BaseModel):
    cert_id: str
    mineral_name: str
    confidence_score: float
    hash_value: str
    issued_at: datetime
    qr_code_url: str
    verification_url: str
    is_valid: bool
