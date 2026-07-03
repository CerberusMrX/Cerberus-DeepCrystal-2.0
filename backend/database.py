"""
Database setup for Cerberus DeepCrystal
PostgreSQL + SQLAlchemy connection
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./deepcrystal.db")

# Use SQLite as fallback for local dev (no Postgres required)
if DATABASE_URL.startswith("postgresql"):
    try:
        engine = create_engine(DATABASE_URL)
        engine.connect()
    except Exception:
        DATABASE_URL = "sqlite:///./deepcrystal.db"
        engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Mineral(Base):
    __tablename__ = "minerals"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    chemical_formula = Column(String)
    crystal_system = Column(String)
    mohs_hardness_min = Column(Float)
    mohs_hardness_max = Column(Float)
    specific_gravity_min = Column(Float)
    specific_gravity_max = Column(Float)
    luster = Column(String)
    cleavage = Column(String)
    fracture = Column(String)
    streak = Column(String)
    transparency = Column(String)
    optical_properties = Column(Text)
    refractive_index_min = Column(Float)
    refractive_index_max = Column(Float)
    birefringence = Column(Float, nullable=True)
    pleochroism = Column(String, nullable=True)
    color = Column(String)
    common_treatments = Column(Text)
    synthetic_methods = Column(Text)
    known_origins = Column(Text)
    price_min_usd = Column(Float)
    price_max_usd = Column(Float)
    price_unit = Column(String, default="per carat")
    geological_class = Column(String)
    uv_fluorescence = Column(String)
    inclusion_patterns = Column(Text)
    category = Column(String)  # Gem, Rock-forming, Ore, etc.
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class AnalysisReport(Base):
    __tablename__ = "analysis_reports"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True)
    blockchain_id = Column(String, unique=True)
    mineral_name = Column(String)
    chemical_formula = Column(String)
    crystal_system = Column(String)
    mohs_hardness = Column(String)
    specific_gravity = Column(Float, nullable=True)
    natural_probability = Column(Float)
    synthetic_probability = Column(Float)
    treatment_probability = Column(Float)
    treatment_type = Column(String)
    inclusion_analysis = Column(JSON)
    crack_assessment = Column(JSON)
    price_min_local = Column(Float)
    price_max_local = Column(Float)
    price_min_usd = Column(Float)
    price_max_usd = Column(Float)
    currency_local = Column(String, default="LKR")
    origin_prediction = Column(JSON)
    confidence_score = Column(Float)
    mode = Column(String, default="pro")  # free, pro, lab
    created_at = Column(DateTime, default=datetime.utcnow)


class BlockchainCert(Base):
    __tablename__ = "blockchain_certs"
    id = Column(Integer, primary_key=True, index=True)
    cert_id = Column(String, unique=True, index=True)
    session_id = Column(String)
    mineral_name = Column(String)
    confidence_score = Column(Float)
    hash_value = Column(String)
    qr_path = Column(String)
    issued_at = Column(DateTime, default=datetime.utcnow)
    is_valid = Column(Boolean, default=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)
