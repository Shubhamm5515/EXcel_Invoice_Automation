"""
Invoice counter management endpoints
"""
from fastapi import APIRouter, HTTPException, Form
from app.services import counter_service

router = APIRouter(prefix="/api/counter", tags=["Counter"])


@router.get("/status")
async def get_counter_status():
    """Get current invoice counter status"""
    try:
        return counter_service.get_status()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get counter status: {str(e)}"
        )


@router.post("/set")
async def set_counter(
    start_number: int = Form(...),
    financial_year: str = Form(None)
):
    """
    Set invoice counter to a specific number
    
    - **start_number**: Starting invoice number (e.g., 36 for HD/2025-26/036)
    - **financial_year**: Financial year (e.g., "2025-26", optional)
    """
    try:
        result = counter_service.set_counter(start_number, financial_year)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to set counter: {str(e)}"
        )


@router.post("/reset")
async def reset_counter(financial_year: str = Form(None)):
    """
    Reset invoice counter to 0 for a new financial year
    
    - **financial_year**: Financial year (e.g., "2026-27", optional)
    """
    try:
        result = counter_service.reset_counter(financial_year)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to reset counter: {str(e)}"
        )
