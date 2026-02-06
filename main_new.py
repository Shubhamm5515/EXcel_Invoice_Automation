"""
Hill Drive Invoice Automation - Refactored FastAPI Backend
Clean, modular architecture
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

from config import settings
from app.routers import (
    invoices_router,
    ocr_router,
    counter_router,
    health_router
)

# Initialize FastAPI app
app = FastAPI(
    title="Hill Drive Invoice Automation API",
    description="Automated invoice generation with OCR.space integration",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router)
app.include_router(invoices_router)
app.include_router(ocr_router)
app.include_router(counter_router)


@app.get("/", response_class=HTMLResponse)
@app.head("/")
async def root():
    """Serve the frontend"""
    try:
        if not os.path.exists("static/index.html"):
            return HTMLResponse(
                content="""
                <html>
                <body style="background: white; color: black; padding: 20px; font-family: Arial;">
                    <h1>Error: Frontend files not found</h1>
                    <p>The static/index.html file is missing.</p>
                    <p>Please ensure the 'static' folder exists with index.html, style.css, and script.js</p>
                    <p><a href="/docs">Go to API Documentation</a></p>
                </body>
                </html>
                """,
                status_code=500
            )
        
        with open("static/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except Exception as e:
        return HTMLResponse(
            content=f"""
            <html>
            <body style="background: white; color: black; padding: 20px; font-family: Arial;">
                <h1>Error Loading Frontend</h1>
                <p>Error: {str(e)}</p>
                <p><a href="/docs">Go to API Documentation</a></p>
            </body>
            </html>
            """,
            status_code=500
        )


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'success': False,
            'error': exc.detail,
            'status_code': exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            'success': False,
            'error': 'Internal server error',
            'details': str(exc)
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main_new:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
