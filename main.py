"""
Hill Drive Invoice Automation - FastAPI Backend
OCR.space Integration + Excel Generation
"""
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os
import uuid
from typing import Optional

from config import settings
from schemas import (
    BookingDataInput, OCRRequest, InvoiceResponse, 
    OCRResponse, HealthResponse, ErrorResponse
)
from ocr_service import ocr_service
from gemini_service import gemini_extractor
from openrouter_service import openrouter_extractor
from hilldrive_excel_mapper import HillDriveExcelWriter, process_booking_to_excel
from implementation_example import BookingDataExtractor
from google_drive_storage import GoogleDriveStorage

# Initialize Google Drive storage (optional - works without credentials)
drive_storage = GoogleDriveStorage()

# Initialize FastAPI app
app = FastAPI(
    title="Hill Drive Invoice Automation API",
    description="Automated invoice generation with OCR.space integration",
    version="1.0.0",
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


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the frontend"""
    try:
        # Check if static files exist
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


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Detailed health check"""
    ai_service = "OpenRouter AI" if openrouter_extractor.enabled else ("Gemini AI" if gemini_extractor.enabled else "Basic Pattern Matching")
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "ocr_service": "OCR.space (Free Tier)",
        "ai_service": ai_service
    }


@app.get("/test-static")
async def test_static():
    """Test if static files are accessible"""
    return {
        "static_folder_exists": os.path.exists("static"),
        "index_html_exists": os.path.exists("static/index.html"),
        "style_css_exists": os.path.exists("static/style.css"),
        "script_js_exists": os.path.exists("static/script.js"),
        "static_files": os.listdir("static") if os.path.exists("static") else []
    }



@app.post("/api/ocr/extract", response_model=OCRResponse)
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


@app.post("/api/ocr/extract-url", response_model=OCRResponse)
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



@app.post("/api/invoice/create", response_model=InvoiceResponse)
async def create_invoice_from_data(data: BookingDataInput):
    """
    Create invoice from manual booking data (no OCR)
    
    Provide booking details directly as JSON
    """
    try:
        start_time = datetime.now()
        
        # Convert Pydantic model to dict
        booking_data = data.model_dump(exclude_none=True)
        
        # Generate unique invoice ID
        invoice_id = f"HD-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6]}"
        
        # Create invoice
        writer = HillDriveExcelWriter(settings.template_path, settings.master_file_path)
        
        if settings.use_master_file:
            # Add as new sheet to master file
            result = writer.write_to_master(booking_data)
            output_path = result['master_file']
            sheet_name = result['sheet_name']
            message = f"Invoice added as sheet '{sheet_name}' in master file"
        else:
            # Create separate file
            output_filename = f"{invoice_id}.xlsx"
            output_path = os.path.join(settings.output_dir, output_filename)
            writer.write(booking_data, output_path)
            message = "Invoice created successfully"
            
            # Upload to Google Drive (if configured)
            if drive_storage.service:
                drive_storage.upload_invoice(output_path)
        
        # Calculate processing time
        processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
        
        return InvoiceResponse(
            success=True,
            message=message,
            invoice_id=invoice_id,
            file_path=output_path,
            download_url=f"/api/invoice/download/{invoice_id}",
            extracted_data=booking_data,
            confidence=booking_data.get('extraction_confidence', 'high'),
            calculation_verified=booking_data.get('calculation_verified', True),
            processing_time_ms=processing_time
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Invoice creation failed: {str(e)}"
        )


@app.post("/api/invoice/create-from-ocr", response_model=InvoiceResponse)
async def create_invoice_from_ocr(
    file: UploadFile = File(...),
    user_text: Optional[str] = Form(None),
    language: str = Form("eng"),
    document_images: Optional[list[UploadFile]] = File(None)
):
    """
    Create invoice from OCR image + optional user text + optional document images
    
    - **file**: Image file with booking details
    - **user_text**: Additional booking details (optional)
    - **language**: OCR language code
    - **document_images**: Customer document images (Aadhaar, DL, etc.) to embed in Excel
    """
    try:
        start_time = datetime.now()
        
        # Step 1: Extract text from image
        file_content = await file.read()
        
        # Validate file
        if len(file_content) > settings.max_file_size_bytes:
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds {settings.max_file_size_mb}MB limit"
            )
        
        # Preprocess and OCR
        processed_content = ocr_service.preprocess_image(file_content)
        ocr_result = ocr_service.extract_text_from_file(
            processed_content,
            language=language
        )
        
        if not ocr_result['success']:
            raise HTTPException(
                status_code=500,
                detail=f"OCR failed: {ocr_result.get('error')}"
            )
        
        ocr_text = ocr_result['text']
        
        # Step 2: Extract booking data using AI (semantic understanding)
        if settings.use_openrouter and openrouter_extractor.enabled:
            # Use OpenRouter for intelligent extraction
            booking_data = openrouter_extractor.extract_invoice_data(ocr_text, user_text or "")
            booking_data = openrouter_extractor.enhance_extracted_data(booking_data)
        elif settings.use_gemini and gemini_extractor.enabled:
            # Use Gemini for intelligent extraction
            booking_data = gemini_extractor.extract_invoice_data(ocr_text, user_text or "")
            booking_data = gemini_extractor.enhance_extracted_data(booking_data)
        else:
            # Fallback to basic extraction
            extractor = BookingDataExtractor()
            booking_data = extractor.extract(ocr_text, user_text or "")
        
        # Step 2.5: Process document images if provided
        document_image_data = []
        if document_images:
            for doc_img in document_images:
                try:
                    img_content = await doc_img.read()
                    # Validate image size
                    if len(img_content) <= settings.max_file_size_bytes:
                        document_image_data.append(img_content)
                    else:
                        print(f"⚠️  Skipping large document image: {doc_img.filename}")
                except Exception as e:
                    print(f"⚠️  Failed to read document image: {e}")
        
        # Add document images to booking data
        if document_image_data:
            booking_data['document_images'] = document_image_data
        
        # Step 3: Generate invoice
        invoice_id = f"HD-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6]}"
        
        writer = HillDriveExcelWriter(settings.template_path, settings.master_file_path)
        
        if settings.use_master_file:
            # Add as new sheet to master file
            result = writer.write_to_master(booking_data)
            output_path = result['master_file']
            sheet_name = result['sheet_name']
            message = f"Invoice added as sheet '{sheet_name}' in master file"
        else:
            # Create separate file
            output_filename = f"{invoice_id}.xlsx"
            output_path = os.path.join(settings.output_dir, output_filename)
            writer.write(booking_data, output_path)
            message = "Invoice created successfully from OCR"
            
            # Upload to Google Drive (if configured)
            if drive_storage.service:
                drive_storage.upload_invoice(output_path)
        
        # Calculate processing time
        processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
        
        # Remove binary data before returning (can't serialize to JSON)
        response_data = {k: v for k, v in booking_data.items() if k != 'document_images'}
        if document_image_data:
            response_data['document_count'] = len(document_image_data)
        
        return InvoiceResponse(
            success=True,
            message=message,
            invoice_id=invoice_id,
            file_path=output_path,
            download_url=f"/api/invoice/download/{invoice_id}",
            extracted_data=response_data,
            confidence=booking_data.get('extraction_confidence'),
            calculation_verified=booking_data.get('calculation_verified'),
            processing_time_ms=processing_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Invoice creation failed: {str(e)}"
        )


@app.post("/api/invoice/create-full-pipeline", response_model=InvoiceResponse)
async def create_invoice_full_pipeline(
    file: Optional[UploadFile] = File(None),
    user_text: Optional[str] = Form(None),
    image_url: Optional[str] = Form(None),
    language: str = Form("eng")
):
    """
    Full pipeline: OCR (file or URL) + User Text → Invoice
    
    Provide either:
    - **file**: Upload image file, OR
    - **image_url**: Public image URL
    
    Plus:
    - **user_text**: Additional booking details
    - **language**: OCR language code
    """
    try:
        start_time = datetime.now()
        ocr_text = ""
        
        # Step 1: Get OCR text (from file or URL)
        if file:
            file_content = await file.read()
            processed_content = ocr_service.preprocess_image(file_content)
            ocr_result = ocr_service.extract_text_from_file(
                processed_content,
                language=language
            )
        elif image_url:
            ocr_result = ocr_service.extract_text_from_url(
                image_url,
                language=language
            )
        else:
            # No OCR, just use user text
            ocr_result = {'success': True, 'text': ''}
        
        if ocr_result['success']:
            ocr_text = ocr_result.get('text', '')
        
        # Step 2: Extract and create invoice
        result = process_booking_to_excel(
            ocr_text,
            user_text or "",
            template_path=settings.template_path,
            output_path=None  # Will generate path
        )
        
        # Generate unique invoice ID and path
        invoice_id = f"HD-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6]}"
        output_filename = f"{invoice_id}.xlsx"
        output_path = os.path.join(settings.output_dir, output_filename)
        
        # Move/rename the generated file
        if os.path.exists(result['output_file']):
            os.rename(result['output_file'], output_path)
        
        processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
        
        return InvoiceResponse(
            success=True,
            message="Invoice created successfully",
            invoice_id=invoice_id,
            file_path=output_path,
            download_url=f"/api/invoice/download/{invoice_id}",
            extracted_data=result['extracted_data'],
            confidence=result.get('confidence'),
            calculation_verified=result.get('calculation_verified'),
            processing_time_ms=processing_time
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Full pipeline failed: {str(e)}"
        )



@app.get("/api/invoice/download/{invoice_id}")
async def download_invoice(invoice_id: str):
    """
    Download generated invoice by ID
    
    - **invoice_id**: Invoice identifier (or 'master' to download all invoices)
    """
    try:
        # Check if master file mode is enabled
        if settings.use_master_file:
            # In master file mode, download the master file
            file_path = settings.master_file_path
            
            if not os.path.exists(file_path):
                raise HTTPException(
                    status_code=404,
                    detail=f"Master invoice file not found. No invoices have been created yet."
                )
            
            # Return the master file with all invoices
            return FileResponse(
                path=file_path,
                filename="all_invoices.xlsx",
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            # Separate file mode - find the specific file
            filename = f"{invoice_id}.xlsx"
            file_path = os.path.join(settings.output_dir, filename)
            
            if not os.path.exists(file_path):
                raise HTTPException(
                    status_code=404,
                    detail=f"Invoice {invoice_id} not found"
                )
            
            return FileResponse(
                path=file_path,
                filename=filename,
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Download failed: {str(e)}"
        )


@app.get("/api/invoice/list")
async def list_invoices(limit: int = 50):
    """
    List all generated invoices
    
    - **limit**: Maximum number of invoices to return
    """
    try:
        if not os.path.exists(settings.output_dir):
            return {"invoices": [], "count": 0}
        
        files = [
            f for f in os.listdir(settings.output_dir)
            if f.endswith('.xlsx')
        ]
        
        # Sort by modification time (newest first)
        files.sort(
            key=lambda x: os.path.getmtime(
                os.path.join(settings.output_dir, x)
            ),
            reverse=True
        )
        
        # Limit results
        files = files[:limit]
        
        invoices = []
        for filename in files:
            file_path = os.path.join(settings.output_dir, filename)
            invoice_id = filename.replace('.xlsx', '')
            
            invoices.append({
                'invoice_id': invoice_id,
                'filename': filename,
                'created_at': datetime.fromtimestamp(
                    os.path.getmtime(file_path)
                ).isoformat(),
                'size_bytes': os.path.getsize(file_path),
                'download_url': f"/api/invoice/download/{invoice_id}"
            })
        
        return {
            'invoices': invoices,
            'count': len(invoices),
            'total': len([f for f in os.listdir(settings.output_dir) if f.endswith('.xlsx')])
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list invoices: {str(e)}"
        )


@app.delete("/api/invoice/delete/{invoice_id}")
async def delete_invoice(invoice_id: str):
    """
    Delete an invoice by ID
    
    - **invoice_id**: Invoice identifier
    """
    try:
        filename = f"{invoice_id}.xlsx"
        file_path = os.path.join(settings.output_dir, filename)
        
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=404,
                detail=f"Invoice {invoice_id} not found"
            )
        
        os.remove(file_path)
        
        return {
            'success': True,
            'message': f'Invoice {invoice_id} deleted successfully'
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Delete failed: {str(e)}"
        )


@app.post("/api/gemini/extract")
async def extract_with_gemini(
    ocr_text: str = Form(...),
    user_text: Optional[str] = Form(None)
):
    """
    Test Gemini extraction without creating invoice
    
    - **ocr_text**: OCR extracted text
    - **user_text**: Additional user-provided text
    """
    try:
        if not gemini_extractor.enabled:
            raise HTTPException(
                status_code=503,
                detail="Gemini API is not configured. Please add GEMINI_API_KEY to .env file"
            )
        
        # Extract data using Gemini
        extracted_data = gemini_extractor.extract_invoice_data(ocr_text, user_text or "")
        enhanced_data = gemini_extractor.enhance_extracted_data(extracted_data)
        
        return {
            'success': True,
            'message': 'Data extracted successfully using Gemini AI',
            'data': enhanced_data,
            'extraction_method': enhanced_data.get('extraction_method'),
            'confidence': enhanced_data.get('extraction_confidence')
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Gemini extraction failed: {str(e)}"
        )


@app.get("/api/gemini/status")
async def gemini_status():
    """Check if Gemini AI is configured and available"""
    return {
        'enabled': gemini_extractor.enabled,
        'model': settings.gemini_model if gemini_extractor.enabled else None,
        'use_gemini': settings.use_gemini,
        'message': 'Gemini AI is ready' if gemini_extractor.enabled else 'Gemini API key not configured'
    }


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
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
