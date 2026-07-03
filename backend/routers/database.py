"""
Mineral database router for Cerberus DeepCrystal
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db, Mineral, init_db
from typing import Optional

router = APIRouter()

init_db()


@router.get("/search")
async def search_minerals(
    q: Optional[str] = Query(None, description="Search by name or formula"),
    category: Optional[str] = Query(None),
    crystal_system: Optional[str] = Query(None),
    mohs_min: Optional[float] = Query(None),
    mohs_max: Optional[float] = Query(None),
    limit: int = 50,
    db: Session = Depends(get_db)
):
    query = db.query(Mineral)
    if q:
        query = query.filter(
            Mineral.name.ilike(f"%{q}%") |
            Mineral.chemical_formula.ilike(f"%{q}%")
        )
    if category:
        query = query.filter(Mineral.category.ilike(f"%{category}%"))
    if crystal_system:
        query = query.filter(Mineral.crystal_system.ilike(f"%{crystal_system}%"))
    if mohs_min is not None:
        query = query.filter(Mineral.mohs_hardness_min >= mohs_min)
    if mohs_max is not None:
        query = query.filter(Mineral.mohs_hardness_max <= mohs_max)

    minerals = query.limit(limit).all()
    return [
        {
            "id": m.id,
            "name": m.name,
            "chemical_formula": m.chemical_formula,
            "crystal_system": m.crystal_system,
            "mohs_hardness": f"{m.mohs_hardness_min}–{m.mohs_hardness_max}",
            "specific_gravity": f"{m.specific_gravity_min}–{m.specific_gravity_max}",
            "luster": m.luster,
            "color": m.color,
            "streak": m.streak,
            "transparency": m.transparency,
            "refractive_index": f"{m.refractive_index_min}–{m.refractive_index_max}" if m.refractive_index_min else "N/A",
            "geological_class": m.geological_class,
            "category": m.category,
            "known_origins": m.known_origins,
            "common_treatments": m.common_treatments,
            "price_range": f"${m.price_min_usd}–${m.price_max_usd} {m.price_unit}" if m.price_min_usd else "N/A",
            "uv_fluorescence": m.uv_fluorescence,
            "description": m.description,
        }
        for m in minerals
    ]


@router.get("/{mineral_name}")
async def get_mineral(mineral_name: str, db: Session = Depends(get_db)):
    m = db.query(Mineral).filter(Mineral.name.ilike(mineral_name)).first()
    if not m:
        raise HTTPException(status_code=404, detail=f"Mineral '{mineral_name}' not found in the Cerberus DeepCrystal database.")
    return {
        "name": m.name,
        "chemical_formula": m.chemical_formula,
        "crystal_system": m.crystal_system,
        "mohs_hardness": f"{m.mohs_hardness_min}–{m.mohs_hardness_max}",
        "specific_gravity": f"{m.specific_gravity_min}–{m.specific_gravity_max}",
        "luster": m.luster,
        "cleavage": m.cleavage,
        "fracture": m.fracture,
        "streak": m.streak,
        "transparency": m.transparency,
        "optical_properties": m.optical_properties,
        "refractive_index": f"{m.refractive_index_min}–{m.refractive_index_max}" if m.refractive_index_min else "N/A",
        "birefringence": m.birefringence,
        "pleochroism": m.pleochroism,
        "color": m.color,
        "geological_class": m.geological_class,
        "category": m.category,
        "known_origins": m.known_origins,
        "common_treatments": m.common_treatments,
        "synthetic_methods": m.synthetic_methods,
        "price_range": f"${m.price_min_usd}–${m.price_max_usd} {m.price_unit}" if m.price_min_usd else "N/A",
        "uv_fluorescence": m.uv_fluorescence,
        "inclusion_patterns": m.inclusion_patterns,
        "description": m.description,
    }


@router.get("/")
async def list_minerals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    minerals = db.query(Mineral).offset(skip).limit(limit).all()
    return [{"id": m.id, "name": m.name, "chemical_formula": m.chemical_formula, "category": m.category} for m in minerals]
