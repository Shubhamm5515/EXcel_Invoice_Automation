"""
Pydantic schemas for Hill Drive Invoice API
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class BookingDataInput(BaseModel):
    """Schema for manual booking data input"""
    customer_name: Optional[str] = None
    company_name: Optional[str] = None
    mobile_number: Optional[str] = None
    address: Optional[str] = None
    vehicle_name: Optional[str] = None
    vehicle_number: Optional[str] = None
    start_datetime: Optional[str] = None
    end_datetime: Optional[str] = None
    duration_days: Optional[int] = None
    base_rent: Optional[float] = None
    security_deposit: Optional[float] = None
    total_amount: Optional[float] = None
    advance_paid: Optional[float] = None
    place_of_supply: Optional[str] = "Jaipur"
    delivery_address: Optional[str] = "Jaipur hub"
    payment_mode: Optional[str] = "Online"
    included_km: Optional[int] = None
    extra_km: Optional[int] = None
    extra_km_rate: Optional[float] = None
    extra_km_charge: Optional[float] = None
    pickup_drop_charges: Optional[float] = None
    other_charges: Optional[float] = None
    invoice_number: Optional[str] = None
    invoice_date: Optional[str] = None


class OCRRequest(BaseModel):
    """Schema for OCR request"""
    image_url: Optional[str] = None
    language: str = "eng"
    isOverlayRequired: bool = False


class OCRResponse(BaseModel):
    """Schema for OCR response"""
    success: bool
    text: str
    confidence: Optional[float] = None
    processing_time_ms: Optional[int] = None
    error: Optional[str] = None


class InvoiceResponse(BaseModel):
    """Schema for invoice creation response"""
    success: bool
    message: str
    invoice_id: str
    file_path: str
    download_url: str
    extracted_data: Optional[Dict[str, Any]] = None
    confidence: Optional[str] = None
    calculation_verified: Optional[bool] = None
    processing_time_ms: Optional[int] = None
    sheet_name: Optional[str] = None


class HealthResponse(BaseModel):
    """Schema for health check response"""
    status: str
    timestamp: str
    version: str
    ocr_service: str
    ai_service: str


class ErrorResponse(BaseModel):
    """Schema for error response"""
    success: bool = False
    error: str
    detail: Optional[str] = None
    timestamp: Optional[str] = None


class InvoiceListResponse(BaseModel):
    """Schema for invoice list response"""
    success: bool
    invoices: List[Dict[str, Any]]
    count: int


class DeleteResponse(BaseModel):
    """Schema for delete response"""
    success: bool
    message: str
    deleted_file: Optional[str] = None
