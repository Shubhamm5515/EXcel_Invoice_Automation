"""
Health check and status endpoints
"""
from fastapi import APIRouter
from datetime import datetime
from app.models import HealthResponse
from app.services import extraction_service

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
@router.head("/health")
async def health_check():
    """Detailed health check"""
    ai_service = extraction_service.get_extraction_method()
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "ocr_service": "OCR.space (Free Tier)",
        "ai_service": ai_service
    }


@router.get("/test-static")
async def test_static():
    """Test if static files are accessible"""
    import os
    return {
        "static_folder_exists": os.path.exists("static"),
        "index_html_exists": os.path.exists("static/index.html"),
        "style_css_exists": os.path.exists("static/style.css"),
        "script_js_exists": os.path.exists("static/script.js"),
        "static_files": os.listdir("static") if os.path.exists("static") else []
    }
