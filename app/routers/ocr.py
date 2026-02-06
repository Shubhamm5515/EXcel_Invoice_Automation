"""
OCR endpoints
"""
from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from app.models import OCRRequest, OCRResponse
from app.services import ocr_service
from config import settings

router = APIRouter(prefix="/api/ocr", tags=["OCR"])


@router.post("/extract", response_model=OCRResponse)
async def extract_text_from_image(
    file: UploadFile = File(...),
    language: str = Form("eng")
):
    """
    Extract text from uploaded image using OCR.space
    
    - **file**: Image file (JPG, PNG, PDF)
    - **language**: OCR language code (default: eng)
    """
    try:
        # Validate file size
        file_content = await file.read()
        if len(file_content) > settings.max_file_size_bytes:
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds {settings.max_file_size_mb}MB limit"
            )
        
        # Validate file extension
        file_ext = file.filename.split('.')[-1].lower()
        if file_ext not in settings.allowed_extensions_list:
            raise HTTPException(
                status_code=400,
                detail=f"File type not allowed. Allowed: {', '.join(settings.allowed_extensions_list)}"
            )
        
        # Preprocess image
        processed_content = ocr_service.preprocess_image(file_content)
        
        # Perform OCR
        result = ocr_service.extract_text_from_file(
            processed_content,
            language=language
        )
        
        if not result['success']:
            raise HTTPException(
                status_code=500,
                detail=result.get('error', 'OCR processing failed')
            )
        
        return OCRResponse(
            success=True,
            text=result['text'],
            confidence=result.get('confidence'),
            processing_time_ms=result.get('processing_time', 0)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR extraction failed: {str(e)}")


@router.post("/extract-url", response_model=OCRResponse)
async def extract_text_from_url(request: OCRRequest):
    """
    Extract text from image URL using OCR.space
    
    - **image_url**: Public URL of the image
    - **language**: OCR language code
    """
    try:
        if not request.image_url:
            raise HTTPException(status_code=400, detail="image_url is required")
        
        result = ocr_service.extract_text_from_url(
            request.image_url,
            language=request.language
        )
        
        if not result['success']:
            raise HTTPException(
                status_code=500,
                detail=result.get('error', 'OCR processing failed')
            )
        
        return OCRResponse(
            success=True,
            text=result['text'],
            confidence=result.get('confidence'),
            processing_time_ms=result.get('processing_time', 0)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR extraction failed: {str(e)}")
