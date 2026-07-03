"""
AI/ML Pipeline for Cerberus DeepCrystal
Simulates CNN (ResNet/EfficientNet), Vision Transformer, YOLO, GAN, and ensemble model
Author: Sudeepa Wanigarathna
"""

import random
import hashlib
import uuid
from PIL import Image
import numpy as np
import io
from typing import Optional, Dict, Any, List


# ─────────────── Gem Knowledge Base ───────────────
GEM_DATA = {
    "Blue Sapphire": {
        "formula": "Al₂O₃ (Corundum with Fe,Ti)",
        "crystal_system": "Trigonal",
        "mohs": (9.0, 9.0),
        "sg": (3.98, 4.02),
        "ri": (1.762, 1.778),
        "luster": "Vitreous to Adamantine",
        "transparency": "Transparent to Opaque",
        "streak": "White",
        "geological_class": "Oxide",
        "category": "Gemstone",
        "origins": [("Sri Lanka", 0.40), ("Myanmar", 0.20), ("Kashmir", 0.15), ("Madagascar", 0.15), ("Thailand", 0.10)],
        "treatments": ["Heat Treatment", "Beryllium Diffusion"],
        "price_min": 200, "price_max": 50000,
        "uv": "Inert to weak orange-red"
    },
    "Yellow Sapphire": {
        "formula": "Al₂O₃ (Corundum with Fe)",
        "crystal_system": "Trigonal",
        "mohs": (9.0, 9.0),
        "sg": (3.98, 4.02),
        "ri": (1.762, 1.770),
        "luster": "Vitreous",
        "transparency": "Transparent",
        "streak": "White",
        "geological_class": "Oxide",
        "category": "Gemstone",
        "origins": [("Sri Lanka", 0.50), ("Thailand", 0.20), ("Madagascar", 0.15), ("Australia", 0.15)],
        "treatments": ["Heat Treatment", "Irradiation"],
        "price_min": 100, "price_max": 5000,
        "uv": "Weak orange to yellow"
    },
    "Pink Sapphire": {
        "formula": "Al₂O₃ (Corundum with Cr)",
        "crystal_system": "Trigonal",
        "mohs": (9.0, 9.0),
        "sg": (3.98, 4.02),
        "ri": (1.762, 1.770),
        "luster": "Vitreous",
        "transparency": "Transparent",
        "streak": "White",
        "geological_class": "Oxide",
        "category": "Gemstone",
        "origins": [("Sri Lanka", 0.40), ("Madagascar", 0.35), ("Myanmar", 0.25)],
        "treatments": ["Heat Treatment"],
        "price_min": 150, "price_max": 10000,
        "uv": "Strong orange-red"
    },
    "Padparadscha Sapphire": {
        "formula": "Al₂O₃ (Corundum with Fe,Cr)",
        "crystal_system": "Trigonal",
        "mohs": (9.0, 9.0),
        "sg": (3.98, 4.02),
        "ri": (1.762, 1.770),
        "luster": "Vitreous",
        "transparency": "Transparent",
        "streak": "White",
        "geological_class": "Oxide",
        "category": "Gemstone",
        "origins": [("Sri Lanka", 0.80), ("Madagascar", 0.15), ("Tanzania", 0.05)],
        "treatments": ["Heat Treatment (Caution: Beryllium Diffusion)"],
        "price_min": 500, "price_max": 30000,
        "uv": "Strong orange-red"
    },
    "Ruby": {
        "formula": "Al₂O₃ (Chromium-bearing Corundum)",
        "crystal_system": "Trigonal",
        "mohs": (9.0, 9.0),
        "sg": (3.99, 4.01),
        "ri": (1.762, 1.770),
        "luster": "Adamantine to Vitreous",
        "transparency": "Transparent to Opaque",
        "streak": "White",
        "geological_class": "Oxide",
        "category": "Gemstone",
        "origins": [("Myanmar", 0.35), ("Sri Lanka", 0.25), ("Mozambique", 0.20), ("Thailand", 0.12), ("Madagascar", 0.08)],
        "treatments": ["Heat Treatment", "Glass Filling", "Fracture Filling"],
        "price_min": 300, "price_max": 100000,
        "uv": "Strong red fluorescence"
    },
    "White Diamond": {
        "formula": "C", "crystal_system": "Cubic", "mohs": (10.0, 10.0), "sg": (3.51, 3.53), "ri": (2.417, 2.417),
        "luster": "Adamantine", "transparency": "Transparent", "streak": "White",
        "geological_class": "Native Element", "category": "Gemstone",
        "origins": [("Botswana", 0.30), ("Russia", 0.25), ("Canada", 0.20), ("South Africa", 0.15), ("Australia", 0.10)],
        "treatments": ["Laser Drilling", "Fracture Filling"],
        "price_min": 1000, "price_max": 1000000, "uv": "Strong blue to inert"
    },
    "Yellow Diamond": {
        "formula": "C (with Nitrogen)", "crystal_system": "Cubic", "mohs": (10.0, 10.0), "sg": (3.51, 3.53), "ri": (2.417, 2.417),
        "luster": "Adamantine", "transparency": "Transparent", "streak": "White",
        "geological_class": "Native Element", "category": "Gemstone",
        "origins": [("South Africa", 0.40), ("Australia", 0.30), ("Russia", 0.20), ("Canada", 0.10)],
        "treatments": ["HPHT Treatment", "Irradiation"],
        "price_min": 2000, "price_max": 100000, "uv": "Variable"
    },
    "Blue Diamond": {
        "formula": "C (with Boron)", "crystal_system": "Cubic", "mohs": (10.0, 10.0), "sg": (3.51, 3.53), "ri": (2.417, 2.417),
        "luster": "Adamantine", "transparency": "Transparent", "streak": "White",
        "geological_class": "Native Element", "category": "Gemstone",
        "origins": [("South Africa", 0.60), ("India", 0.20), ("Russia", 0.20)],
        "treatments": ["Irradiation", "HPHT"],
        "price_min": 10000, "price_max": 5000000, "uv": "Inert (often phosphoresces red)"
    },
    "Pink Diamond": {
        "formula": "C", "crystal_system": "Cubic", "mohs": (10.0, 10.0), "sg": (3.51, 3.53), "ri": (2.417, 2.417),
        "luster": "Adamantine", "transparency": "Transparent", "streak": "White",
        "geological_class": "Native Element", "category": "Gemstone",
        "origins": [("Australia (Argyle)", 0.90), ("South Africa", 0.05), ("Russia", 0.05)],
        "treatments": ["Irradiation", "HPHT"],
        "price_min": 50000, "price_max": 2000000, "uv": "Variable"
    },
    "Alexandrite": {
        "formula": "BeAl₂O₄ (Chrysoberyl)",
        "crystal_system": "Orthorhombic",
        "mohs": (8.5, 8.5),
        "sg": (3.70, 3.78),
        "ri": (1.746, 1.755),
        "luster": "Vitreous",
        "transparency": "Transparent",
        "streak": "White",
        "geological_class": "Oxide",
        "category": "Gemstone",
        "origins": [("Sri Lanka", 0.30), ("Russia (Ural)", 0.30), ("Brazil", 0.20), ("Zimbabwe", 0.20)],
        "treatments": ["Rarely treated"],
        "price_min": 5000, "price_max": 150000,
        "uv": "Strong red fluorescence"
    },
    "Rubellite Tourmaline": {
        "formula": "Complex Borosilicate (Pink/Red)", "crystal_system": "Trigonal", "mohs": (7.0, 7.5), "sg": (3.01, 3.06), "ri": (1.624, 1.644),
        "luster": "Vitreous", "transparency": "Transparent", "streak": "White",
        "geological_class": "Silicate", "category": "Gemstone",
        "origins": [("Brazil", 0.40), ("Madagascar", 0.30), ("Nigeria", 0.30)],
        "treatments": ["Irradiation", "Heat Treatment"],
        "price_min": 50, "price_max": 2000, "uv": "Inert to weak red"
    },
    "Indicolite Tourmaline": {
        "formula": "Complex Borosilicate (Blue)", "crystal_system": "Trigonal", "mohs": (7.0, 7.5), "sg": (3.01, 3.06), "ri": (1.624, 1.644),
        "luster": "Vitreous", "transparency": "Transparent", "streak": "White",
        "geological_class": "Silicate", "category": "Gemstone",
        "origins": [("Brazil", 0.50), ("Afghanistan", 0.30), ("Namibia", 0.20)],
        "treatments": ["Heat Treatment"],
        "price_min": 100, "price_max": 5000, "uv": "Inert"
    },
    "Verdelite Tourmaline": {
        "formula": "Complex Borosilicate (Green)", "crystal_system": "Trigonal", "mohs": (7.0, 7.5), "sg": (3.01, 3.06), "ri": (1.624, 1.644),
        "luster": "Vitreous", "transparency": "Transparent", "streak": "White",
        "geological_class": "Silicate", "category": "Gemstone",
        "origins": [("Brazil", 0.40), ("Namibia", 0.30), ("Madagascar", 0.30)],
        "treatments": ["Heat Treatment"],
        "price_min": 30, "price_max": 1000, "uv": "Inert"
    },
    "Red Spinel": {
        "formula": "MgAl₂O₄ (with Cr)", "crystal_system": "Cubic", "mohs": (8.0, 8.0), "sg": (3.58, 3.61), "ri": (1.712, 1.762),
        "luster": "Vitreous", "transparency": "Transparent", "streak": "White",
        "geological_class": "Oxide", "category": "Gemstone",
        "origins": [("Myanmar", 0.60), ("Vietnam", 0.20), ("Tanzania", 0.20)],
        "treatments": ["Rarely treated"],
        "price_min": 300, "price_max": 20000, "uv": "Strong red"
    },
    "Blue Spinel": {
        "formula": "MgAl₂O₄ (with Co/Fe)", "crystal_system": "Cubic", "mohs": (8.0, 8.0), "sg": (3.58, 3.61), "ri": (1.712, 1.762),
        "luster": "Vitreous", "transparency": "Transparent", "streak": "White",
        "geological_class": "Oxide", "category": "Gemstone",
        "origins": [("Sri Lanka", 0.50), ("Vietnam", 0.30), ("Myanmar", 0.20)],
        "treatments": ["Rarely treated"],
        "price_min": 100, "price_max": 5000, "uv": "Inert"
    },
    "Rhodolite Garnet": {
        "formula": "(Mg,Fe)₃Al₂(SiO₄)₃", "crystal_system": "Cubic", "mohs": (7.0, 7.5), "sg": (3.78, 3.85), "ri": (1.750, 1.760),
        "luster": "Vitreous", "transparency": "Transparent", "streak": "White",
        "geological_class": "Silicate", "category": "Gemstone",
        "origins": [("Sri Lanka", 0.40), ("Tanzania", 0.30), ("Madagascar", 0.30)],
        "treatments": ["Not typically treated"],
        "price_min": 30, "price_max": 500, "uv": "Inert"
    },
    "Tsavorite Garnet": {
        "formula": "Ca₃Al₂(SiO₄)₃ (Green)", "crystal_system": "Cubic", "mohs": (7.0, 7.5), "sg": (3.57, 3.73), "ri": (1.734, 1.759),
        "luster": "Vitreous", "transparency": "Transparent", "streak": "White",
        "geological_class": "Silicate", "category": "Gemstone",
        "origins": [("Kenya", 0.60), ("Tanzania", 0.40)],
        "treatments": ["Not typically treated"],
        "price_min": 500, "price_max": 10000, "uv": "Inert"
    },
    "Demantoid Garnet": {
        "formula": "Ca₃Fe₂(SiO₄)₃ (Green)", "crystal_system": "Cubic", "mohs": (6.5, 7.0), "sg": (3.82, 3.88), "ri": (1.880, 1.889),
        "luster": "Adamantine", "transparency": "Transparent", "streak": "White",
        "geological_class": "Silicate", "category": "Gemstone",
        "origins": [("Russia", 0.70), ("Namibia", 0.20), ("Madagascar", 0.10)],
        "treatments": ["Heat Treatment"],
        "price_min": 500, "price_max": 20000, "uv": "Inert"
    },
    "Aquamarine": {
        "formula": "Be₃Al₂Si₆O₁₈ (Beryl)",
        "crystal_system": "Hexagonal",
        "mohs": (7.5, 8.0),
        "sg": (2.68, 2.74),
        "ri": (1.567, 1.590),
        "luster": "Vitreous",
        "transparency": "Transparent",
        "streak": "White",
        "geological_class": "Silicate - Cyclosilicate",
        "category": "Gemstone",
        "origins": [("Brazil", 0.50), ("Pakistan", 0.20), ("Nigeria", 0.15), ("Sri Lanka", 0.15)],
        "treatments": ["Heat Treatment"],
        "price_min": 50, "price_max": 5000,
        "uv": "Inert"
    },
    "Paraiba Tourmaline": {
        "formula": "Na(Li,Al)₉Al₆(BO₃)₃Si₆O₁₈(OH)₄ + Cu",
        "crystal_system": "Trigonal",
        "mohs": (7.0, 7.5),
        "sg": (3.00, 3.26),
        "ri": (1.620, 1.640),
        "luster": "Vitreous",
        "transparency": "Transparent",
        "streak": "White",
        "geological_class": "Silicate - Cyclosilicate",
        "category": "Gemstone",
        "origins": [("Brazil", 0.40), ("Mozambique", 0.35), ("Nigeria", 0.25)],
        "treatments": ["Heat Treatment"],
        "price_min": 5000, "price_max": 60000,
        "uv": "Inert"
    },
    "Tanzanite": {
        "formula": "Ca₂Al₃(SiO₄)(Si₂O₇)O(OH) (Zoisite)",
        "crystal_system": "Orthorhombic",
        "mohs": (6.0, 7.0),
        "sg": (3.35, 3.38),
        "ri": (1.691, 1.700),
        "luster": "Vitreous",
        "transparency": "Transparent",
        "streak": "White",
        "geological_class": "Silicate - Sorosilicate",
        "category": "Gemstone",
        "origins": [("Tanzania (Merelani)", 1.00)],
        "treatments": ["Heat Treatment"],
        "price_min": 200, "price_max": 12000,
        "uv": "Weak blue"
    },
    "Opal": {
        "formula": "SiO₂ · nH₂O",
        "crystal_system": "Amorphous",
        "mohs": (5.5, 6.5),
        "sg": (1.98, 2.25),
        "ri": (1.37, 1.47),
        "luster": "Resinous to Waxy",
        "transparency": "Transparent to Opaque",
        "streak": "White",
        "geological_class": "Mineraloid",
        "category": "Gemstone",
        "origins": [("Australia", 0.90), ("Ethiopia", 0.05), ("Mexico", 0.05)],
        "treatments": ["Impregnation", "Backing", "Doublet/Triplet"],
        "price_min": 50, "price_max": 30000,
        "uv": "Yellow-green to white"
    },
    "Quartz": {
        "formula": "SiO₂",
        "crystal_system": "Trigonal",
        "mohs": (7.0, 7.0),
        "sg": (2.65, 2.66),
        "ri": (1.544, 1.553),
        "luster": "Vitreous",
        "transparency": "Transparent to Opaque",
        "streak": "White",
        "geological_class": "Silicate - Tectosilicate",
        "category": "Common Mineral/Gemstone",
        "origins": [("Brazil", 0.30), ("USA", 0.20), ("Madagascar", 0.20), ("Worldwide", 0.30)],
        "treatments": ["Heat Treatment", "Irradiation", "Dyeing"],
        "price_min": 1, "price_max": 500,
        "uv": "Inert to weak"
    },
    "Amethyst": {
        "formula": "SiO₂ (Quartz var.)",
        "crystal_system": "Trigonal",
        "mohs": (7.0, 7.0),
        "sg": (2.65, 2.66),
        "ri": (1.544, 1.553),
        "luster": "Vitreous",
        "transparency": "Transparent",
        "streak": "White",
        "geological_class": "Silicate - Tectosilicate",
        "category": "Gemstone",
        "origins": [("Brazil", 0.60), ("Uruguay", 0.20), ("Zambia", 0.15), ("Sri Lanka", 0.05)],
        "treatments": ["Heat Treatment", "Irradiation"],
        "price_min": 5, "price_max": 800,
        "uv": "Inert"
    },
    "Chrysoberyl": {
        "formula": "BeAl₂O₄",
        "crystal_system": "Orthorhombic",
        "mohs": (8.5, 8.5),
        "sg": (3.70, 3.78),
        "ri": (1.746, 1.763),
        "luster": "Vitreous",
        "transparency": "Transparent to Translucent",
        "streak": "White",
        "geological_class": "Oxide",
        "category": "Gemstone",
        "origins": [("Sri Lanka", 0.40), ("Brazil", 0.30), ("Myanmar", 0.15), ("Russia", 0.15)],
        "treatments": ["No common treatments"],
        "price_min": 50, "price_max": 5000,
        "uv": "Weak to moderate green"
    },
    "Moonstone": {
        "formula": "KAlSi₃O₈ (Feldspar)",
        "crystal_system": "Monoclinic",
        "mohs": (6.0, 6.5),
        "sg": (2.56, 2.59),
        "ri": (1.518, 1.526),
        "luster": "Vitreous to Pearly",
        "transparency": "Transparent to Translucent",
        "streak": "White",
        "geological_class": "Silicate - Tectosilicate",
        "category": "Gemstone",
        "origins": [("Sri Lanka", 0.50), ("India", 0.30), ("Myanmar", 0.20)],
        "treatments": ["Rarely treated"],
        "price_min": 5, "price_max": 500,
        "uv": "Weak blue to white"
    },
    "Spessartite": {
        "formula": "Mn₃Al₂(SiO₄)₃ (Garnet)",
        "crystal_system": "Cubic (Isometric)",
        "mohs": (7.0, 7.5),
        "sg": (4.12, 4.20),
        "ri": (1.79, 1.81),
        "luster": "Vitreous",
        "transparency": "Transparent",
        "streak": "White",
        "geological_class": "Silicate - Nesosilicate",
        "category": "Gemstone",
        "origins": [("Namibia", 0.30), ("Sri Lanka", 0.25), ("Myanmar", 0.25), ("Brazil", 0.20)],
        "treatments": ["Not typically treated"],
        "price_min": 100, "price_max": 3000,
        "uv": "Inert"
    },
    "Kunzite": {
        "formula": "LiAlSi₂O₆ (Spodumene)",
        "crystal_system": "Monoclinic",
        "mohs": (6.5, 7.0),
        "sg": (3.17, 3.19),
        "ri": (1.655, 1.682),
        "luster": "Vitreous",
        "transparency": "Transparent",
        "streak": "White",
        "geological_class": "Silicate - Inosilicate",
        "category": "Gemstone",
        "origins": [("Afghanistan", 0.35), ("Brazil", 0.30), ("USA", 0.20), ("Madagascar", 0.15)],
        "treatments": ["Heat Treatment", "Irradiation"],
        "price_min": 30, "price_max": 1500,
        "uv": "Strong orange"
    },
    "Fluorite": {
        "formula": "CaF₂",
        "crystal_system": "Cubic (Isometric)",
        "mohs": (4.0, 4.0),
        "sg": (3.17, 3.19),
        "ri": (1.434, 1.434),
        "luster": "Vitreous",
        "transparency": "Transparent to Translucent",
        "streak": "White",
        "geological_class": "Halide",
        "category": "Mineral/Collector",
        "origins": [("China", 0.40), ("Mexico", 0.20), ("USA", 0.20), ("UK", 0.10), ("Other", 0.10)],
        "treatments": ["Waxing", "Coating"],
        "price_min": 1, "price_max": 200,
        "uv": "Strong blue fluorescence"
    },
    "Jadeite": {
        "formula": "NaAlSi₂O₆", "crystal_system": "Monoclinic", "mohs": (6.5, 7.0), "sg": (3.25, 3.35), "ri": (1.666, 1.680),
        "luster": "Vitreous to Greasy", "transparency": "Translucent to Opaque", "streak": "White",
        "geological_class": "Silicate - Inosilicate", "category": "Gemstone",
        "origins": [("Myanmar", 0.90), ("Guatemala", 0.05), ("Russia", 0.05)],
        "treatments": ["Bleaching", "Polymer Impregnation", "Dyeing"],
        "price_min": 100, "price_max": 500000, "uv": "Inert to weak green"
    },
    "Nephrite": {
        "formula": "Ca₂(Mg,Fe)₅Si₈O₂₂(OH)₂", "crystal_system": "Monoclinic", "mohs": (6.0, 6.5), "sg": (2.90, 3.03), "ri": (1.600, 1.627),
        "luster": "Vitreous to Greasy", "transparency": "Translucent to Opaque", "streak": "White",
        "geological_class": "Silicate - Inosilicate", "category": "Gemstone",
        "origins": [("China", 0.40), ("Canada", 0.30), ("New Zealand", 0.20), ("Russia", 0.10)],
        "treatments": ["Waxing", "Dyeing"],
        "price_min": 10, "price_max": 5000, "uv": "Inert"
    },
    "Morganite": {
        "formula": "Be₃Al₂Si₆O₁₈ (Pink Beryl)", "crystal_system": "Hexagonal", "mohs": (7.5, 8.0), "sg": (2.71, 2.90), "ri": (1.572, 1.592),
        "luster": "Vitreous", "transparency": "Transparent", "streak": "White",
        "geological_class": "Silicate - Cyclosilicate", "category": "Gemstone",
        "origins": [("Brazil", 0.40), ("Madagascar", 0.30), ("Afghanistan", 0.20), ("Mozambique", 0.10)],
        "treatments": ["Heat Treatment", "Irradiation"],
        "price_min": 100, "price_max": 2000, "uv": "Weak lilac"
    },
    "Turquoise": {
        "formula": "CuAl₆(PO₄)₄(OH)₈·4H₂O", "crystal_system": "Triclinic", "mohs": (5.0, 6.0), "sg": (2.60, 2.90), "ri": (1.61, 1.65),
        "luster": "Waxy to Subvitreous", "transparency": "Opaque", "streak": "White to Greenish",
        "geological_class": "Phosphate", "category": "Gemstone",
        "origins": [("Iran", 0.40), ("USA", 0.30), ("China", 0.20), ("Egypt", 0.10)],
        "treatments": ["Stabilization", "Waxing", "Dyeing"],
        "price_min": 1, "price_max": 500, "uv": "Weak green to yellow"
    },
    "Onyx": {
        "formula": "SiO₂ (Chalcedony)", "crystal_system": "Trigonal", "mohs": (6.5, 7.0), "sg": (2.60, 2.65), "ri": (1.543, 1.554),
        "luster": "Vitreous", "transparency": "Opaque", "streak": "White",
        "geological_class": "Silicate - Tectosilicate", "category": "Gemstone",
        "origins": [("Brazil", 0.30), ("India", 0.20), ("Madagascar", 0.20), ("Worldwide", 0.30)],
        "treatments": ["Dyeing", "Heat Treatment"],
        "price_min": 1, "price_max": 100, "uv": "Inert"
    },
    "Malachite": {
        "formula": "Cu₂(CO₃)(OH)₂", "crystal_system": "Monoclinic", "mohs": (3.5, 4.0), "sg": (3.60, 4.05), "ri": (1.655, 1.909),
        "luster": "Vitreous to Silky", "transparency": "Opaque", "streak": "Pale Green",
        "geological_class": "Carbonate", "category": "Gemstone",
        "origins": [("Congo", 0.70), ("Russia", 0.15), ("Australia", 0.10), ("USA", 0.05)],
        "treatments": ["Waxing", "Polymer Impregnation"],
        "price_min": 1, "price_max": 200, "uv": "Inert"
    },
    "Peridot": {
        "formula": "(Mg,Fe)₂SiO₄", "crystal_system": "Orthorhombic", "mohs": (6.5, 7.0), "sg": (3.27, 3.37), "ri": (1.635, 1.690),
        "luster": "Vitreous", "transparency": "Transparent", "streak": "White",
        "geological_class": "Silicate - Nesosilicate",
        "category": "Gemstone",
        "origins": [("Pakistan", 0.40), ("USA (Arizona)", 0.30), ("China", 0.20), ("Myanmar", 0.10)],
        "treatments": ["Commonly Untreated", "Occasionally Epoxied"],
        "price_min": 20, "price_max": 800, "uv": "Inert"
    },
    "Zircon": {
        "formula": "ZrSiO₄", "crystal_system": "Tetragonal", "mohs": (6.5, 7.5), "sg": (3.93, 4.73), "ri": (1.810, 2.024),
        "luster": "Adamantine to Vitreous", "transparency": "Transparent", "streak": "White",
        "geological_class": "Silicate - Nesosilicate", "category": "Gemstone",
        "origins": [("Cambodia", 0.40), ("Sri Lanka", 0.30), ("Myanmar", 0.20), ("Tanzania", 0.10)],
        "treatments": ["Heat Treatment"],
        "price_min": 30, "price_max": 1500, "uv": "Variable (often yellowish)"
    },
    "Iolite": {
        "formula": "Mg₂Al₄Si₅O₁₈", "crystal_system": "Orthorhombic", "mohs": (7.0, 7.5), "sg": (2.58, 2.66), "ri": (1.533, 1.551),
        "luster": "Vitreous", "transparency": "Transparent", "streak": "White",
        "geological_class": "Silicate - Cyclosilicate", "category": "Gemstone",
        "origins": [("India", 0.40), ("Sri Lanka", 0.30), ("Brazil", 0.20), ("Madagascar", 0.10)],
        "treatments": ["Rarely treated"],
        "price_min": 10, "price_max": 300, "uv": "Inert"
    },
    "Lapis Lazuli": {
        "formula": "(Na,Ca)₈(AlSiO₄)₆(S,Cl,SO₄)₁+ ", "crystal_system": "Cubic", "mohs": (5.0, 6.0), "sg": (2.38, 2.45), "ri": (1.50, 1.67),
        "luster": "Vitreous to Dull", "transparency": "Opaque", "streak": "Blue",
        "geological_class": "Silicate Rock", "category": "Gemstone",
        "origins": [("Afghanistan", 0.80), ("Chile", 0.10), ("Russia", 0.10)],
        "treatments": ["Dyeing", "Waxing", "Impregnation"],
        "price_min": 1, "price_max": 150, "uv": "Weak orange (Calcite)"
    },
    "Topaz": {
        "formula": "Al₂SiO₄(F,OH)₂", "crystal_system": "Orthorhombic", "mohs": (8.0, 8.0), "sg": (3.49, 3.57), "ri": (1.606, 1.644),
        "luster": "Vitreous", "transparency": "Transparent", "streak": "White",
        "geological_class": "Silicate - Nesosilicate", "category": "Gemstone",
        "origins": [("Brazil", 0.50), ("Pakistan", 0.20), ("Russia", 0.15), ("Sri Lanka", 0.15)],
        "treatments": ["Heat Treatment", "Irradiation", "Coating"],
        "price_min": 5, "price_max": 5000, "uv": "Weak yellow/green"
    },
    "Citrine": {
        "formula": "SiO₂ (Yellow Quartz)", "crystal_system": "Trigonal", "mohs": (7.0, 7.0), "sg": (2.65, 2.66), "ri": (1.544, 1.553),
        "luster": "Vitreous", "transparency": "Transparent", "streak": "White",
        "geological_class": "Silicate - Tectosilicate", "category": "Gemstone",
        "origins": [("Brazil", 0.60), ("Spain", 0.20), ("Madagascar", 0.20)],
        "treatments": ["Heat Treatment (often Amethyst)"],
        "price_min": 2, "price_max": 300, "uv": "Inert"
    },
    "Smoky Quartz": {
        "formula": "SiO₂", "crystal_system": "Trigonal", "mohs": (7.0, 7.0), "sg": (2.65, 2.66), "ri": (1.544, 1.553),
        "luster": "Vitreous", "transparency": "Transparent to Translucent", "streak": "White",
        "geological_class": "Silicate - Tectosilicate", "category": "Gemstone",
        "origins": [("Brazil", 0.40), ("USA", 0.30), ("Switzerland", 0.20), ("Madagascar", 0.10)],
        "treatments": ["Irradiation", "Heat Treatment"],
        "price_min": 1, "price_max": 100, "uv": "Inert"
    },
    "Rose Quartz": {
        "formula": "SiO₂", "crystal_system": "Trigonal", "mohs": (7.0, 7.0), "sg": (2.65, 2.66), "ri": (1.544, 1.553),
        "luster": "Vitreous", "transparency": "Transparent to Translucent", "streak": "White",
        "geological_class": "Silicate - Tectosilicate", "category": "Gemstone",
        "origins": [("Brazil", 0.50), ("Madagascar", 0.30), ("India", 0.20)],
        "treatments": ["Rarely treated"],
        "price_min": 1, "price_max": 200, "uv": "Weak purple"
    },
    "Labradorite": {
        "formula": "(Ca,Na)(Al,Si)₄O₈", "crystal_system": "Triclinic", "mohs": (6.0, 6.5), "sg": (2.68, 2.72), "ri": (1.559, 1.573),
        "luster": "Vitreous", "transparency": "Transparent to Opaque", "streak": "White",
        "geological_class": "Silicate - Tectosilicate", "category": "Gemstone",
        "origins": [("Canada", 0.40), ("Madagascar", 0.30), ("Finland", 0.20), ("Russia", 0.10)],
        "treatments": ["Rarely treated"],
        "price_min": 1, "price_max": 200, "uv": "Inert"
    },
    "Sunstone": {
        "formula": "(Ca,Na)(Al,Si)₄O₈", "crystal_system": "Triclinic", "mohs": (6.0, 6.5), "sg": (2.62, 2.65), "ri": (1.537, 1.548),
        "luster": "Vitreous", "transparency": "Transparent to Translucent", "streak": "White",
        "geological_class": "Silicate - Tectosilicate", "category": "Gemstone",
        "origins": [("USA", 0.50), ("India", 0.30), ("Norway", 0.20)],
        "treatments": ["Diffusion (rare)"],
        "price_min": 10, "price_max": 1000, "uv": "Inert"
    },
    "Amazonite": {
        "formula": "KAlSi₃O₈", "crystal_system": "Triclinic", "mohs": (6.0, 6.5), "sg": (2.56, 2.58), "ri": (1.522, 1.530),
        "luster": "Vitreous to Pearly", "transparency": "Opaque", "streak": "White",
        "geological_class": "Silicate - Tectosilicate", "category": "Gemstone",
        "origins": [("Brazil", 0.40), ("USA", 0.30), ("Russia", 0.20)],
        "treatments": ["Waxing", "Dyeing"],
        "price_min": 1, "price_max": 100, "uv": "Weak green"
    },
    "Tiger's Eye": {
        "formula": "SiO₂", "crystal_system": "Trigonal", "mohs": (6.5, 7.0), "sg": (2.64, 2.71), "ri": (1.544, 1.553),
        "luster": "Silky", "transparency": "Opaque", "streak": "White",
        "geological_class": "Silicate - Tectosilicate", "category": "Gemstone",
        "origins": [("South Africa", 0.70), ("Australia", 0.15), ("India", 0.15)],
        "treatments": ["Dyeing", "Heat Treatment"],
        "price_min": 1, "price_max": 50, "uv": "Inert"
    },
    "Rhodonite": {
        "formula": "MnSiO₃", "crystal_system": "Triclinic", "mohs": (5.5, 6.5), "sg": (3.40, 3.74), "ri": (1.716, 1.752),
        "luster": "Vitreous to Pearly", "transparency": "Transparent to Opaque", "streak": "White",
        "geological_class": "Silicate - Inosilicate", "category": "Gemstone",
        "origins": [("Russia", 0.40), ("Australia", 0.20), ("Brazil", 0.20)],
        "treatments": ["Waxing", "Impregnation"],
        "price_min": 1, "price_max": 500, "uv": "Inert to weak red"
    },
    "Rhodochrosite": {
        "formula": "MnCO₃", "crystal_system": "Trigonal", "mohs": (3.5, 4.0), "sg": (3.40, 3.70), "ri": (1.597, 1.816),
        "luster": "Vitreous to Pearly", "transparency": "Transparent to Opaque", "streak": "White",
        "geological_class": "Carbonate", "category": "Gemstone",
        "origins": [("Argentina", 0.50), ("South Africa", 0.20), ("Peru", 0.20)],
        "treatments": ["Waxing", "Impregnation"],
        "price_min": 5, "price_max": 2000, "uv": "Moderate red"
    },
    "Larimar": {
        "formula": "NaCa₂Si₃O₈(OH)", "crystal_system": "Triclinic", "mohs": (4.5, 5.0), "sg": (2.70, 2.90), "ri": (1.59, 1.63),
        "luster": "Vitreous to Silky", "transparency": "Opaque", "streak": "White",
        "geological_class": "Silicate - Inosilicate", "category": "Gemstone",
        "origins": [("Dominican Republic", 1.00)],
        "treatments": ["Commonly Untreated"],
        "price_min": 5, "price_max": 500, "uv": "Weak green"
    },
    "Charoite": {
        "formula": "(K,Sr,Ba)(Ca,Na)₂Si₄O₁₀(OH,F)·H₂O", "crystal_system": "Monoclinic", "mohs": (5.0, 6.0), "sg": (2.54, 2.78), "ri": (1.55, 1.56),
        "luster": "Vitreous to Pearly", "transparency": "Opaque", "streak": "White",
        "geological_class": "Silicate", "category": "Gemstone",
        "origins": [("Russia", 1.00)],
        "treatments": ["Waxing", "Impregnation"],
        "price_min": 5, "price_max": 300, "uv": "Weak green"
    },
    "Sugilite": {
        "formula": "KNa₂(Fe,Mn,Al)₂Li₃Si₁₂O₃₀", "crystal_system": "Hexagonal", "mohs": (5.5, 6.5), "sg": (2.74, 2.80), "ri": (1.60, 1.61),
        "luster": "Vitreous to Waxy", "transparency": "Translucent to Opaque", "streak": "White",
        "geological_class": "Silicate - Cyclosilicate", "category": "Gemstone",
        "origins": [("South Africa", 0.80), ("Japan", 0.10)],
        "treatments": ["Rarely treated"],
        "price_min": 10, "price_max": 1000, "uv": "Inert"
    },
    "Chrysocolla": {
        "formula": "Cu₂H₂Si₂O₅(OH)₄", "crystal_system": "Orthorhombic", "mohs": (2.0, 4.0), "sg": (2.00, 2.40), "ri": (1.46, 1.57),
        "luster": "Vitreous to Earthy", "transparency": "Opaque", "streak": "Pale Blue",
        "geological_class": "Silicate", "category": "Gemstone",
        "origins": [("USA", 0.40), ("Chile", 0.30)],
        "treatments": ["Stabilization", "Waxing"],
        "price_min": 1, "price_max": 300, "uv": "Inert"
    },
    "Azurite": {
        "formula": "Cu₃(CO₃)₂(OH)₂", "crystal_system": "Monoclinic", "mohs": (3.5, 4.0), "sg": (3.77, 3.89), "ri": (1.720, 1.848),
        "luster": "Vitreous", "transparency": "Transparent to Opaque", "streak": "Blue",
        "geological_class": "Carbonate", "category": "Gemstone",
        "origins": [("USA", 0.40), ("France", 0.20)],
        "treatments": ["Stabilization", "Waxing"],
        "price_min": 1, "price_max": 500, "uv": "Inert"
    },
    "Hiddenite": {
        "formula": "LiAlSi₂O₆ (Green Spodumene)", "crystal_system": "Monoclinic", "mohs": (6.5, 7.0), "sg": (3.17, 3.19), "ri": (1.655, 1.682),
        "luster": "Vitreous", "transparency": "Transparent", "streak": "White",
        "geological_class": "Silicate - Inosilicate", "category": "Gemstone",
        "origins": [("USA", 0.50), ("Afghanistan", 0.30)],
        "treatments": ["Irradiation"],
        "price_min": 50, "price_max": 3000, "uv": "Weak orange"
    },
    "Heliodor": {
        "formula": "Be₃Al₂Si₆O₁₈ (Golden Beryl)", "crystal_system": "Hexagonal", "mohs": (7.5, 8.0), "sg": (2.67, 2.78), "ri": (1.565, 1.602),
        "luster": "Vitreous", "transparency": "Transparent", "streak": "White",
        "geological_class": "Silicate - Cyclosilicate", "category": "Gemstone",
        "origins": [("Brazil", 0.40), ("Ukraine", 0.30)],
        "treatments": ["Irradiation", "Heat Treatment"],
        "price_min": 50, "price_max": 1500, "uv": "Inert"
    },
    "Goshenite": {
        "formula": "Be₃Al₂Si₆O₁₈ (Colorless Beryl)", "crystal_system": "Hexagonal", "mohs": (7.5, 8.0), "sg": (2.67, 2.78), "ri": (1.565, 1.602),
        "luster": "Vitreous", "transparency": "Transparent", "streak": "White",
        "geological_class": "Silicate - Cyclosilicate", "category": "Gemstone",
        "origins": [("Brazil", 0.40), ("USA", 0.30)],
        "treatments": ["Irradiation"],
        "price_min": 10, "price_max": 500, "uv": "Inert"
    },
    "Bixbite": {
        "formula": "Be₃Al₂Si₆O₁₈ (Red Beryl)", "crystal_system": "Hexagonal", "mohs": (7.5, 8.0), "sg": (2.66, 2.70), "ri": (1.570, 1.586),
        "luster": "Vitreous", "transparency": "Transparent", "streak": "White",
        "geological_class": "Silicate - Cyclosilicate", "category": "Gemstone",
        "origins": [("USA (Utah)", 1.00)],
        "treatments": ["Fracture Filling"],
        "price_min": 1000, "price_max": 20000, "uv": "Inert"
    },
    "Obsidian": {
        "formula": "SiO₂", "crystal_system": "Amorphous", "mohs": (5.0, 6.0), "sg": (2.35, 2.60), "ri": (1.45, 1.55),
        "luster": "Vitreous", "transparency": "Transparent to Opaque", "streak": "White",
        "geological_class": "Volcanic Glass", "category": "Gemstone",
        "origins": [("USA", 0.40), ("Mexico", 0.30)],
        "treatments": ["Commonly Untreated"],
        "price_min": 1, "price_max": 100, "uv": "Inert"
    },
    "Moldavite": {
        "formula": "SiO₂(+Al₂O₃)", "crystal_system": "Amorphous", "mohs": (5.5, 6.0), "sg": (2.27, 2.40), "ri": (1.48, 1.54),
        "luster": "Vitreous", "transparency": "Transparent to Translucent", "streak": "White",
        "geological_class": "Tektite", "category": "Gemstone",
        "origins": [("Czech Republic", 1.00)],
        "treatments": ["Commonly Untreated"],
        "price_min": 10, "price_max": 1000, "uv": "Inert"
    },
    "Amber": {
        "formula": "C₁₀H₁₆O", "crystal_system": "Amorphous", "mohs": (2.0, 2.5), "sg": (1.05, 1.10), "ri": (1.54, 1.55),
        "luster": "Resinous", "transparency": "Transparent to Opaque", "streak": "White",
        "geological_class": "Organic", "category": "Gemstone",
        "origins": [("Baltic Region", 0.70), ("Dominican Republic", 0.20)],
        "treatments": ["Heat Treatment", "Pressure Treatment"],
        "price_min": 1, "price_max": 500, "uv": "Strong blue"
    },
    "Pearl": {
        "formula": "CaCO₃", "crystal_system": "Orthorhombic", "mohs": (2.5, 4.5), "sg": (2.60, 2.85), "ri": (1.52, 1.69),
        "luster": "Pearly", "transparency": "Opaque", "streak": "White",
        "geological_class": "Organic", "category": "Gemstone",
        "origins": [("Japan", 0.30), ("China", 0.30)],
        "treatments": ["Bleaching", "Dyeing"],
        "price_min": 5, "price_max": 10000, "uv": "Variable"
    },
    "Coral": {
        "formula": "CaCO₃", "crystal_system": "Trigonal", "mohs": (3.5, 4.0), "sg": (2.60, 2.70), "ri": (1.48, 1.65),
        "luster": "Vitreous to waxy", "transparency": "Opaque", "streak": "White",
        "geological_class": "Organic", "category": "Gemstone",
        "origins": [("Mediterranean", 0.50), ("Japan", 0.30)],
        "treatments": ["Bleaching", "Dyeing"],
        "price_min": 5, "price_max": 2000, "uv": "Weak orange"
    },
    "Bloodstone": {
        "formula": "SiO₂", "crystal_system": "Trigonal", "mohs": (6.5, 7.0), "sg": (2.60, 2.65), "ri": (1.54, 1.55),
        "luster": "Vitreous to Greasy", "transparency": "Opaque", "streak": "Red",
        "geological_class": "Silicate", "category": "Gemstone",
        "origins": [("India", 0.60), ("Brazil", 0.20)],
        "treatments": ["Commonly Untreated"],
        "price_min": 1, "price_max": 200, "uv": "Inert"
    },
    "Agate": {
        "formula": "SiO₂", "crystal_system": "Trigonal", "mohs": (6.5, 7.0), "sg": (2.60, 2.65), "ri": (1.54, 1.55),
        "luster": "Vitreous", "transparency": "Translucent to Opaque", "streak": "White",
        "geological_class": "Silicate", "category": "Gemstone",
        "origins": [("Brazil", 0.40), ("India", 0.30)],
        "treatments": ["Dyeing", "Heat Treatment"],
        "price_min": 0.5, "price_max": 50, "uv": "Variable"
    },
    "Pyrite": {
        "formula": "FeS₂", "crystal_system": "Cubic", "mohs": (6.0, 6.5), "sg": (4.95, 5.10), "ri": (1.0, 1.0),
        "luster": "Metallic", "transparency": "Opaque", "streak": "Greenish-black",
        "geological_class": "Sulfide", "category": "Mineral",
        "origins": [("Peru", 0.40), ("Spain", 0.30)],
        "treatments": ["Commonly Untreated"],
        "price_min": 0.5, "price_max": 50, "uv": "Inert"
    },
    "Hematite": {
        "formula": "Fe₂O₃", "crystal_system": "Trigonal", "mohs": (5.5, 6.5), "sg": (4.90, 5.30), "ri": (2.94, 3.22),
        "luster": "Metallic", "transparency": "Opaque", "streak": "Red-brown",
        "geological_class": "Oxide", "category": "Mineral",
        "origins": [("Brazil", 0.50), ("Morocco", 0.30)],
        "treatments": ["Commonly Untreated"],
        "price_min": 0.5, "price_max": 100, "uv": "Inert"
    },
    "Rutile": {
        "formula": "TiO₂", "crystal_system": "Tetragonal", "mohs": (6.0, 6.5), "sg": (4.23, 5.50), "ri": (2.62, 2.90),
        "luster": "Adamantine to Metallic", "transparency": "Transparent to Opaque", "streak": "Brown",
        "geological_class": "Oxide", "category": "Mineral",
        "origins": [("Brazil", 0.40), ("Sri Lanka", 0.30)],
        "treatments": ["Untreated"],
        "price_min": 10, "price_max": 500, "uv": "Inert"
    },
    "Spessartine": {
        "formula": "Mn₃Al₂(SiO₄)₃", "crystal_system": "Cubic", "mohs": (7.0, 7.5), "sg": (4.12, 4.18), "ri": (1.790, 1.810),
        "luster": "Vitreous", "transparency": "Transparent", "streak": "White",
        "geological_class": "Silicate", "category": "Gemstone",
        "origins": [("Namibia", 0.40), ("Nigeria", 0.30)],
        "treatments": ["Commonly Untreated"],
        "price_min": 50, "price_max": 3000, "uv": "Inert"
    },
    "Almandine": {
        "formula": "Fe₃Al₂(SiO₄)₃", "crystal_system": "Cubic", "mohs": (7.0, 7.5), "sg": (4.10, 4.30), "ri": (1.770, 1.810),
        "luster": "Vitreous", "transparency": "Transparent to Opaque", "streak": "White",
        "geological_class": "Silicate", "category": "Gemstone",
        "origins": [("India", 0.40), ("Sri Lanka", 0.30)],
        "treatments": ["Commonly Untreated"],
        "price_min": 5, "price_max": 500, "uv": "Inert"
    },
    "Pyrope": {
        "formula": "Mg₃Al₂(SiO₄)₃", "crystal_system": "Cubic", "mohs": (7.0, 7.5), "sg": (3.62, 3.87), "ri": (1.730, 1.760),
        "luster": "Vitreous", "transparency": "Transparent", "streak": "White",
        "geological_class": "Silicate", "category": "Gemstone",
        "origins": [("Czech Republic", 0.40), ("USA", 0.30)],
        "treatments": ["Commonly Untreated"],
        "price_min": 5, "price_max": 500, "uv": "Inert"
    },
    "Hessonite": {
        "formula": "Ca₃Al₂(SiO₄)₃", "crystal_system": "Cubic", "mohs": (6.5, 7.5), "sg": (3.57, 3.73), "ri": (1.734, 1.759),
        "luster": "Vitreous", "transparency": "Transparent to Translucent", "streak": "White",
        "geological_class": "Silicate", "category": "Gemstone",
        "origins": [("Sri Lanka", 0.60), ("India", 0.20)],
        "treatments": ["Commonly Untreated"],
        "price_min": 20, "price_max": 1000, "uv": "Inert"
    },
    "Cat's Eye Chrysoberyl": {
        "formula": "BeAl₂O₄", "crystal_system": "Orthorhombic", "mohs": (8.5, 8.5), "sg": (3.70, 3.78), "ri": (1.746, 1.763),
        "luster": "Vitreous to Chatoyant", "transparency": "Translucent", "streak": "White",
        "geological_class": "Oxide", "category": "Gemstone",
        "origins": [("Sri Lanka", 0.70), ("Brazil", 0.20)],
        "treatments": ["Rarely treated"],
        "price_min": 200, "price_max": 15000, "uv": "Weak green"
    },
    "Prehnite": {
        "formula": "Ca₂Al(AlSi₃O₁₀)(OH)₂", "crystal_system": "Orthorhombic", "mohs": (6.0, 6.5), "sg": (2.80, 2.95), "ri": (1.61, 1.67),
        "luster": "Vitreous to Pearly", "transparency": "Transparent to Translucent", "streak": "White",
        "geological_class": "Silicate", "category": "Gemstone",
        "origins": [("South Africa", 0.50), ("Australia", 0.30)],
        "treatments": ["Rarely treated"],
        "price_min": 5, "price_max": 200, "uv": "Inert"
    },
    "Serpentine": {
        "formula": "(Mg,Fe)₃Si₂O₅(OH)₄", "crystal_system": "Monoclinic", "mohs": (3.0, 6.0), "sg": (2.50, 2.60), "ri": (1.55, 1.57),
        "luster": "Greasy to waxy", "transparency": "Translucent to Opaque", "streak": "White",
        "geological_class": "Silicate", "category": "Gemstone",
        "origins": [("China", 0.40), ("USA", 0.30)],
        "treatments": ["Waxing", "Dyeing"],
        "price_min": 1, "price_max": 100, "uv": "Inert"
    },
}

TREATMENT_INDICATORS = {
    "Heat Treatment": ["rutile silk dissolution", "stress fractures around inclusions", "color zoning alteration", "fingerprint inclusions"],
    "Beryllium Diffusion": ["color concentrated at surface", "abnormal color zoning", "surface coloration at facet junctions"],
    "Glass Filling": ["gas bubbles", "flow structures", "blue flash effect", "curved color boundaries"],
    "Fracture Filling": ["resin residue", "crackling pattern", "interference colors"],
    "Laser Drilling": ["laser channels", "bleached inclusions", "drill holes"],
    "Coating": ["surface layer", "color bleeding", "iridescence"],
    "Irradiation": ["color zoning", "color distribution patterns"],
    "HPHT Treatment": ["metallic inclusions", "graphite", "unusual graining patterns"]
}


# -- REAL VISION AI INTEGRATION (CLIP) --
import torch
from transformers import CLIPProcessor, CLIPModel
from sklearn.cluster import KMeans
import colorsys

# Global model cache to avoid reloading on every request
_clip_model = None
_clip_processor = None
_clip_labels = []

def get_clip_model():
    """
    Singleton-style loader for CLIP to avoid re-loading on every request.
    Returns (model, processor, labels_flattened, num_prompts_per_gem).
    """
    global _clip_model, _clip_processor, _clip_labels
    
    num_prompts = 3 # Ensemble size
    if _clip_model is None:
        print("Loading HuggingFace CLIP Vision Transformer (openai/clip-vit-base-patch32)...")
        _clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        _clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        
        # Build advanced multi-prompt ensemble to improve robustness
        _clip_labels = []
        for gem in GEM_DATA.keys():
            _clip_labels.extend([
                f"A high-quality gemological macro photo of a {gem} gemstone showing its color and luster",
                f"A close-up studio photograph of a polished {gem} gemstone",
                f"A {gem} variety gemstone in a professional laboratory setting"
            ])
            
    return _clip_model, _clip_processor, _clip_labels, num_prompts


def extract_color_features(image: Image.Image, n_colors=3):
    """
    Uses KMeans clustering on the image to extract dominant colors,
    HSV properties, and a calculated color quality score.
    """
    # Resize for faster processing
    img_small = image.resize((100, 100)).convert('RGB')
    data = np.array(img_small).reshape(-1, 3)
    
    kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10).fit(data)
    centers = kmeans.cluster_centers_
    labels = kmeans.labels_
    
    # Get dominant color
    counts = np.bincount(labels)
    dominant_idx = np.argmax(counts)
    dom_color = centers[dominant_idx]
    
    dom_hex = '#%02x%02x%02x' % (int(dom_color[0]), int(dom_color[1]), int(dom_color[2]))
    palette_hex = ['#%02x%02x%02x' % (int(c[0]), int(c[1]), int(c[2])) for c in centers]
    
    # Convert dominant color to HSV
    h, s, v = colorsys.rgb_to_hsv(dom_color[0]/255.0, dom_color[1]/255.0, dom_color[2]/255.0)
    
    # Color Quality Score calculation: favors high saturation and medium-high value (lightness)
    # Saturation (0-1), Value (0-1). Too dark (v < 0.2) or too light (v > 0.9) penalizes.
    v_score = 1.0 - abs(v - 0.7) * 2
    v_score = max(0.2, min(1.0, v_score))
    
    color_quality_score = (s * 0.7) + (v_score * 0.3)
    
    if s < 0.15:
        desc = "Low saturation, pale/colorless"
    elif s < 0.5:
        desc = "Moderate saturation"
    elif s > 0.8:
        desc = "Vivid, highly saturated"
    else:
        desc = "Strong saturation"
        
    if v < 0.3:
        desc += " and very dark."
    elif v > 0.85:
        desc += " and very light/bright."
    
    return {
        "dominant_hex": dom_hex,
        "palette_hex": palette_hex,
        "hue": h * 360,
        "saturation": s,
        "lightness": v,
        "color_quality_score": color_quality_score,
        "description": desc
    }


def analyze_image(image_bytes: bytes, manual_inputs: dict = None) -> dict:
    """
    Uses OpenAI CLIP Vision Transformer for Real Zero-Shot Image Classification
    with a multi-prompt ensemble for improved accuracy.
    Batches text labels to avoid memory/token overflow on large gem databases.
    """
    # Load Real Vision AI with ensemble configuration
    model, processor, labels, n_prompts = get_clip_model()
    
    # Process image
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    # ── Batched Gem Identification (prevents OOM with 168+ labels) ──
    BATCH_SIZE = 30  # Process this many text prompts at a time
    all_logits = []
    with torch.no_grad():
        for i in range(0, len(labels), BATCH_SIZE):
            batch_labels = labels[i:i + BATCH_SIZE]
            inputs = processor(text=batch_labels, images=image, return_tensors="pt", padding=True, truncation=True)
            outputs = model(**inputs)
            all_logits.append(outputs.logits_per_image)  # [1, batch_size]

    # Concatenate all batch logits → [1, total_labels]
    combined_logits = torch.cat(all_logits, dim=1)

    # Ensemble Averaging: Reshape and average logits for the same gem across different prompts
    with torch.no_grad():
        logits = combined_logits.view(1, -1, n_prompts)  # [1, num_gems, n_prompts]
        avg_logits = logits.mean(dim=2)                   # [1, num_gems]
        probs = avg_logits.softmax(dim=1).numpy()[0]
        
    # Apply manual input hard filters if provided
    if manual_inputs:
        ri_input = manual_inputs.get("refractive_index")
        sg_input = manual_inputs.get("specific_gravity")
        hw_input = manual_inputs.get("hardness_result")
        
        gem_keys = list(GEM_DATA.keys())
        for idx, g_key in enumerate(gem_keys):
            g_data = GEM_DATA[g_key]
            penalty = 1.0
            
            if ri_input:
                ri_min, ri_max = g_data["ri"]
                if ri_min is not None and not (ri_min - 0.01 <= ri_input <= ri_max + 0.01):
                    penalty *= 0.0001
            
            if sg_input:
                sg_min, sg_max = g_data["sg"]
                if sg_min is not None and not (sg_min - 0.1 <= sg_input <= sg_max + 0.1):
                    penalty *= 0.0001
                    
            if hw_input:
                hw_min, hw_max = g_data["mohs"]
                if hw_min is not None and not (hw_min - 0.5 <= hw_input <= hw_max + 0.5):
                    penalty *= 0.0001
                    
            probs[idx] *= penalty
            
        # Re-normalize
        if probs.sum() > 0:
            probs = probs / probs.sum()
    
    # Get top prediction from the ensemble
    top_idx = np.argmax(probs)
    primary_gem = list(GEM_DATA.keys())[top_idx]
    gem = GEM_DATA[primary_gem]
    
    # Refined confidence scaling for large class space (>100 classes)
    raw_confidence = float(probs[top_idx])
    # Calibrate so that a clear winner in a large field feels authoritative
    base_confidence = min(0.99, max(0.70, 0.40 + (raw_confidence ** 0.4) * 0.6))

    img_hash = hashlib.md5(image_bytes).hexdigest()
    
    # 2. Extract Computer Vision Color Features
    color_features = extract_color_features(image)
    
    # 3. Real Zero-Shot Inclusion Detection
    inclusion_prompts = [
        "A gemstone showing curved growth lines",
        "A gemstone showing gas bubbles",
        "A gemstone showing rutile silk inclusions",
        "A gemstone showing fracture filling",
        "A gemstone showing flame fusion indicators",
        "A gemstone showing heat treatment markers",
        "A gemstone showing fingerprint inclusions",
        "A gemstone showing needles",
        "A gemstone showing crystals",
        "A gemstone showing feathers"
    ]
    with torch.no_grad():
        inc_inputs = processor(text=inclusion_prompts, images=image, return_tensors="pt", padding=True)
        inc_outputs = model(**inc_inputs)
        
        # Use min-max scaling for inclusions so patterns vary distinctly between images
        inc_logits = inc_outputs.logits_per_image[0].numpy()
        l_min, l_max = inc_logits.min(), inc_logits.max()
        if l_max > l_min:
            inc_probs = (inc_logits - l_min) / (l_max - l_min)
        else:
            inc_probs = np.zeros_like(inc_logits)
        
    inclusion_keys = ["curved_growth_lines", "gas_bubbles", "rutile_silk", "fracture_filling", "flame_fusion_indicators", "heat_treatment_markers", "fingerprint_inclusions", "needles", "crystals", "feathers"]
    inclusion_data = {k: float(min(1.0, p * 1.2 + 0.05)) for k, p in zip(inclusion_keys, inc_probs)} # Scale slightly for UI visibility
    
    key_inclusions = [k.replace("_", " ").title() for k, v in inclusion_data.items() if v > 0.5]
    inclusion_summary = f"Notable inclusions detected: {', '.join(key_inclusions)}." if key_inclusions else "No major inclusions confidently detected above threshold."

    # 4. Real Zero-Shot Treatment & Crack Detection
    treatment_prompts = [
        "A natural, completely untreated gemstone",
        "A heat treated gemstone",
        "A glass filled gemstone",
        "A beryllium diffused gemstone",
        "A resin filled gemstone",
        "A laser drilled gemstone",
        "A coated gemstone",
        "A synthetic lab-grown gemstone"
    ]
    with torch.no_grad():
        trt_inputs = processor(text=treatment_prompts, images=image, return_tensors="pt", padding=True)
        trt_outputs = model(**trt_inputs)
        # Use softmax here to find the most dominant treatment
        trt_probs = trt_outputs.logits_per_image.softmax(dim=1).numpy()[0]
        
    natural_prob, heat_treated, glass_filled, diffusion, resin_filled, laser_drilled, coated, synthetic_prob = trt_probs
    
    treatment_map = {
        "Natural (Untreated)": natural_prob,
        "Heat Treated": heat_treated,
        "Glass Filled": glass_filled,
        "Beryllium Diffusion": diffusion,
        "Resin Filled": resin_filled,
        "Laser Drilled": laser_drilled,
        "Coated": coated,
        "Synthetic": synthetic_prob
    }
    dominant_treatment = max(treatment_map, key=treatment_map.get)

    # 5. Damage Assessment (using inclusions and basic crack estimation)
    # Using some heuristics combined with zero-shot probabilities
    crack_data = {
        "surface_cracks": float(inclusion_data["fracture_filling"] * 0.8),
        "internal_fractures": float(inclusion_data["feathers"] * 0.9),
        "chips": float(min(1.0, inclusion_data["fracture_filling"] * 0.5)),
        "abrasions": float(min(1.0, inclusion_data["heat_treatment_markers"] * 0.3)),
    }
    avg_damage = sum(crack_data.values()) / 4
    if avg_damage < 0.15:
        clarity_grade = "VVS (Very Very Slightly Included)"
    elif avg_damage < 0.30:
        clarity_grade = "VS (Very Slightly Included)"
    elif avg_damage < 0.50:
        clarity_grade = "SI (Slightly Included)"
    else:
        clarity_grade = "I (Included)"

    damage_desc_parts = [k.replace("_", " ").title() for k, v in crack_data.items() if v > 0.3]
    damage_desc = f"Damage observed: {', '.join(damage_desc_parts)}." if damage_desc_parts else "No significant surface damage detected."

    # 6. Apply manual input boosts to base confidence
    if manual_inputs:
        ri = manual_inputs.get("refractive_index")
        if ri:
            gem_ri_min, gem_ri_max = gem["ri"]
            if gem_ri_min <= ri <= gem_ri_max:
                base_confidence = min(0.99, base_confidence + 0.08)
        sg = manual_inputs.get("specific_gravity")
        if sg:
            sg_min, sg_max = gem["sg"]
            if sg_min * 0.95 <= sg <= sg_max * 1.05:
                base_confidence = min(0.99, base_confidence + 0.06)
        hw = manual_inputs.get("hardness_result")
        if hw:
            hw_min, hw_max = gem["mohs"]
            if hw_min * 0.9 <= hw <= hw_max * 1.1:
                base_confidence = min(0.99, base_confidence + 0.04)

    # 7. Deterministic Pricing Model
    carat = manual_inputs.get("carat_weight", 1.0) if manual_inputs else 1.0
    if carat is None:
        carat = 1.0
    base_min = gem["price_min"]
    base_max = gem["price_max"]

    # Treatment factor
    treatment_factor = 1.0
    if dominant_treatment == "Heat Treated":
        treatment_factor = 0.80
    elif dominant_treatment in ["Glass Filled", "Fracture Filling", "Resin Filled", "Laser Drilled"]:
        treatment_factor = 0.40
    elif dominant_treatment == "Beryllium Diffusion":
        treatment_factor = 0.70
    elif dominant_treatment == "Synthetic":
        treatment_factor = 0.05
    elif dominant_treatment == "Coated":
        treatment_factor = 0.60
        
    # Clarity factor (higher damage = lower price)
    clarity_factor = max(0.2, 1.0 - (avg_damage * 1.5))
    
    # Color factor
    color_factor = max(0.5, color_features["color_quality_score"] * 1.2)

    # Carat weight multiplier (larger = disproportionately more expensive for natural stones)
    if natural_prob > 0.5:
        carat_factor = carat ** 1.5
    else:
        carat_factor = carat

    price_min = round(base_min * treatment_factor * clarity_factor * color_factor * carat_factor * natural_prob, 2)
    # Add a realistic margin for max price (e.g. 30% spread)
    price_max = round(price_min * 1.3, 2)

    lkr_rate = 308
    price_min_lkr = round(price_min * lkr_rate, 2)
    price_max_lkr = round(price_max * lkr_rate, 2)

    price_factors = [
        f"Carat weight factor: {carat_factor:.2f}x (from {carat}ct)",
        f"Treatment penalty: {(1.0-treatment_factor)*100:.0f}%",
        f"Clarity penalty: {(1.0-clarity_factor)*100:.0f}%",
        f"Color quality multiplier: {color_factor:.2f}x",
        f"Natural probability confidence: {natural_prob:.0%}"
    ]

    # Origin Prediction (Heuristic based on gem profile + extracted color hue)
    origins_raw = gem["origins"]
    origin_predictions = []
    # Deterministic pseudo-randomness based on hue so it's consistent for the same image
    hue_seed = int(color_features["hue"])
    for i, (country, base_prob) in enumerate(origins_raw):
        # Adjust slightly based on hue deterministic value
        adj = 0.8 + ((hue_seed + i * 17) % 40) / 100.0
        origin_predictions.append({"country": country, "probability": base_prob * adj})
        
    total_origin = sum(o["probability"] for o in origin_predictions)
    for o in origin_predictions:
        o["probability"] = round(o["probability"] / total_origin, 3)
    origin_predictions.sort(key=lambda x: x["probability"], reverse=True)

    # Recommendations
    recs = ["AI Screening Result. For high-value transactions, professional laboratory testing is recommended."]
    if dominant_treatment != "Natural (Untreated)":
        recs.append(f"Possible {dominant_treatment} detected — confirm with spectroscopic analysis (FTIR/Raman).")
    if synthetic_prob > 0.3:
        recs.append("High synthetic probability — request grower certificate or Chelsea filter examination.")
    if natural_prob > 0.85:
        recs.append("High natural probability — may qualify for premium pricing. GIA/Gübelin certification advised.")

    return {
        "gem_key": primary_gem,
        "gem": gem,
        "base_confidence": float(round(base_confidence, 4)),
        "natural_prob": float(round(natural_prob, 4)),
        "synthetic_prob": float(round(synthetic_prob, 4)),
        "treatment_probs": {
            "natural": float(round(natural_prob, 4)),
            "heat_treated": float(round(heat_treated, 4)),
            "diffusion_treated": float(round(diffusion, 4)),
            "glass_filled": float(round(glass_filled, 4)),
            "resin_filled": float(round(resin_filled, 4)),
            "laser_drilled": float(round(laser_drilled, 4)),
            "coated": float(round(coated, 4)),
            "synthetic": float(round(synthetic_prob, 4)),
            "dominant_treatment": dominant_treatment,
        },
        "inclusion_data": {**inclusion_data, "summary": inclusion_summary},
        "crack_data": {**crack_data, "overall_clarity_grade": clarity_grade, "damage_description": damage_desc},
        "color_analysis": color_features,
        "price": {
            "min_usd": float(price_min), "max_usd": float(price_max),
            "min_local": float(price_min_lkr), "max_local": float(price_max_lkr),
            "currency_local": "LKR", "per_carat": True,
            "factors": price_factors
        },
        "origins": origin_predictions,
        "recommendations": recs,
        "ri": gem["ri"],
        "sg": gem["sg"],
        "mohs": gem["mohs"],
        "uv": gem.get("uv", "Unknown"),
    }


def get_gem_data():
    return GEM_DATA
