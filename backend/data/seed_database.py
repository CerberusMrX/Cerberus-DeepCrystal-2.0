"""
Mineral database seed script for Cerberus DeepCrystal
Populates the database with gem/mineral data.
Author: Sudeepa Wanigarathna
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import engine, Base, Mineral, SessionLocal, init_db
from services.ml_pipeline import GEM_DATA

EXTENDED_MINERALS = []


def seed_database():
    init_db()
    db = SessionLocal()

    print("Seeding mineral database...")

    # Seed from ML pipeline GEM_DATA
    for name, data in GEM_DATA.items():
        existing = db.query(Mineral).filter(Mineral.name == name).first()
        if not existing:
            m = Mineral(
                name=name,
                chemical_formula=data["formula"],
                crystal_system=data["crystal_system"],
                mohs_hardness_min=data["mohs"][0],
                mohs_hardness_max=data["mohs"][1],
                specific_gravity_min=data["sg"][0],
                specific_gravity_max=data["sg"][1],
                refractive_index_min=data["ri"][0],
                refractive_index_max=data["ri"][1],
                luster=data["luster"],
                transparency=data["transparency"],
                streak=data["streak"],
                geological_class=data["geological_class"],
                category=data["category"],
                color=data.get("color", "Variable"),
                known_origins=", ".join([f"{c} ({p:.0%})" for c, p in data["origins"]]),
                common_treatments=", ".join(data["treatments"]),
                price_min_usd=data["price_min"],
                price_max_usd=data["price_max"],
                price_unit="per carat",
                uv_fluorescence=data.get("uv", ""),
                cleavage="See technical references",
                fracture="Conchoidal",
                description=f"{name} gemstone data from Cerberus DeepCrystal knowledge base.",
            )
            db.add(m)

    # Seed extended minerals
    for mineral_data in EXTENDED_MINERALS:
        existing = db.query(Mineral).filter(Mineral.name == mineral_data["name"]).first()
        if not existing:
            m = Mineral(**{k: v for k, v in mineral_data.items()})
            db.add(m)

    db.commit()
    print(f"Database seeded. Total minerals: {db.query(Mineral).count()}")
    db.close()


if __name__ == "__main__":
    seed_database()
