"""
Invoice management endpoints
"""
from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse
from datetime import datetime
from typing import Optional
import os

from app.models import BookingDataInput, InvoiceResponse
from app.services import (
    ocr_service,
    extraction_service,
    excel_service,
    storage_service
)
from config import settings

router = APIRouter(prefix="/api/invoice", tags=["Invoices"])


@router.post("/create", response_model=InvoiceResponse)
async def create_invoice_from_data(data: BookingDataInput):
    """
    Create invoice from manual booking data (no OCR)
    
    Provide booking details directly as JSON
    """
    try:
        start_time = datetime.now()
        
        # Convert Pydantic model to dict
        booking_data = data.model_dump(exclude_none=True)
        
        # Create invoice
        invoice_result = excel_service.create_invoice(booking_data)
        
        # Upload to cloud storage
        storage_service.upload_invoice(invoice_result['file_path'])
        
        # Calculate processing time
        processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
        
        message = f"Invoice added as sheet '{invoice_result.get('sheet_name')}' in master file" if invoice_result['mode'] == 'master' else "Invoice created successfully"
        
        return InvoiceResponse(
            success=True,
            message=message,
            invoice_id=invoice_result['invoice_id'],
            file_path=invoice_result['file_path'],
            download_url=f"/api/invoice/download/{invoice_result['invoice_id']}",
            extracted_data=booking_data,
            confidence=booking_data.get('extraction_confidence', 'high'),
            calculation_verified=booking_data.get('calculation_verified', True),
            processing_time_ms=processing_time,
            sheet_name=invoice_result.get('sheet_name')
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Invoice creation failed: {str(e)}"
        )


@router.post("/create-from-ocr", response_model=InvoiceResponse)
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
    - **document_images**: Customer document images (Aadhaar, DL, etc.)
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
        
        # Step 2: Extract booking data using AI
        booking_data = extraction_service.extract_booking_data(ocr_text, user_text or "")
        
        # Step 3: Process document images if provided
        document_image_data = []
        if document_images:
            for doc_img in document_images:
                try:
                    img_content = await doc_img.read()
                    if len(img_content) <= settings.max_file_size_bytes:
                        document_image_data.append(img_content)
                    else:
                        print(f"⚠️  Skipping large document image: {doc_img.filename}")
                except Exception as e:
                    print(f"⚠️  Failed to read document image: {e}")
        
        # Add document images to booking data
        if document_image_data:
            booking_data['document_images'] = document_image_data
        
        # Step 4: Generate invoice
        invoice_result = excel_service.create_invoice(booking_data)
        
        # Step 5: Upload to cloud storage
        storage_service.upload_invoice(invoice_result['file_path'])
        
        # Calculate processing time
        processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
        
        # Remove binary data before returning
        response_data = {k: v for k, v in booking_data.items() if k != 'document_images'}
        if document_image_data:
            response_data['document_count'] = len(document_image_data)
        
        message = f"Invoice added as sheet '{invoice_result.get('sheet_name')}' in master file" if invoice_result['mode'] == 'master' else "Invoice created successfully from OCR"
        
        return InvoiceResponse(
            success=True,
            message=message,
            invoice_id=invoice_result['invoice_id'],
            file_path=invoice_result['file_path'],
            download_url=f"/api/invoice/download/{invoice_result['invoice_id']}",
            extracted_data=response_data,
            confidence=booking_data.get('extraction_confidence'),
            calculation_verified=booking_data.get('calculation_verified'),
            processing_time_ms=processing_time,
            sheet_name=invoice_result.get('sheet_name')
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Invoice creation failed: {str(e)}"
        )


@router.get("/download/{invoice_id}")
async def download_invoice(invoice_id: str):
    """
    Download generated invoice by ID
    
    - **invoice_id**: Invoice identifier (or 'master' to download all invoices)
    """
    try:
        if settings.use_master_file:
            file_path = settings.master_file_path
            
            if not os.path.exists(file_path):
                raise HTTPException(
                    status_code=404,
                    detail=f"Master invoice file not found. No invoices have been created yet."
                )
            
            return FileResponse(
                path=file_path,
                filename="all_invoices.xlsx",
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
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


@router.get("/list")
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


@router.delete("/delete/{invoice_id}")
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
