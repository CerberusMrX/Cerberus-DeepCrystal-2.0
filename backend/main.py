"""
Cerberus DeepCrystal - Mineral & Gemstone Forensic AI System
Author: Sudeepa Wanigarathna
Backend: FastAPI (Unified - serves frontend + API)
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import os
import sys

from routers import analysis, blockchain, database, auth

app = FastAPI(
    title="Cerberus DeepCrystal API",
    description="Advanced AI-Powered Mineral & Gemstone Forensic Laboratory",
    version="2.0.0",
    contact={"name": "Sudeepa Wanigarathna"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Static files for QR codes ──────────────────────────
os.makedirs("static/qrcodes", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# ── API Routers ────────────────────────────────────────
app.include_router(analysis.router, prefix="/api/analysis", tags=["Analysis"])
app.include_router(blockchain.router, prefix="/api/blockchain", tags=["Blockchain"])
app.include_router(database.router, prefix="/api/database", tags=["Database"])
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])

# ── Serve built React frontend ─────────────────────────
FRONTEND_DIST = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
FRONTEND_DIST = os.path.abspath(FRONTEND_DIST)

if os.path.exists(FRONTEND_DIST):
    # Serve assets (JS/CSS/images)
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIST, "assets")), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_frontend(request: Request, full_path: str):
        # Don't intercept API routes
        if full_path.startswith("api/") or full_path.startswith("static/"):
            return JSONResponse({"detail": "Not found"}, status_code=404)
        file_path = os.path.join(FRONTEND_DIST, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        # SPA fallback: return index.html for all frontend routes
        return FileResponse(os.path.join(FRONTEND_DIST, "index.html"))
else:
    @app.get("/")
    def root():
        return {
            "system": "Cerberus DeepCrystal",
            "status": "API Running - Frontend not built. Run install.bat first.",
            "docs": "/docs"
        }


@app.on_event("startup")
async def startup_event():
    """Pre-load the AI model on startup so the first scan is instant."""
    print("=" * 60)
    print("  CERBERUS DEEPCRYSTAL v2.0 - Starting...")
    print("=" * 60)
    try:
        print("  [AI] Pre-loading Vision Transformer model...")
        from services.ml_pipeline import get_clip_model
        get_clip_model()
        print("  [AI] Model loaded and ready!")
    except Exception as e:
        print(f"  [WARNING] Could not pre-load model: {e}")
        print("  [WARNING] Model will load on first scan request.")
    print("  [OK] Server ready at http://localhost:8000")
    print("=" * 60)


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
