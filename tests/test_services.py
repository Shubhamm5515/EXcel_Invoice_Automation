"""
Unit tests for services
"""
import pytest
from app.services import (
    extraction_service,
    counter_service,
    storage_service
)


class TestExtractionService:
    """Test data extraction service"""
    
    def test_extract_customer_name(self):
        """Test customer name extraction"""
        ocr_text = "Customer name: John Doe"
        user_text = "Mobile: 9999888877"
        
        result = extraction_service.extract_booking_data(ocr_text, user_text)
        
        assert result is not None
        assert 'customer_name' in result
    
    def test_extract_mobile_number(self):
        """Test mobile number extraction"""
        ocr_text = "Cx no: 9876543210"
        user_text = ""
        
        result = extraction_service.extract_booking_data(ocr_text, user_text)
        
        assert result.get('mobile_number') == "9876543210"
    
    def test_extraction_method(self):
        """Test extraction method detection"""
        method = extraction_service.get_extraction_method()
        
        assert method in ["OpenRouter AI", "Gemini AI", "Pattern Matching"]


class TestCounterService:
    """Test invoice counter service"""
    
    def test_get_status(self):
        """Test getting counter status"""
        status = counter_service.get_status()
        
        assert 'current_number' in status
        assert 'financial_year' in status
        assert 'next_invoice' in status
        assert status['next_invoice'].startswith('HD/')
    
    def test_invoice_format(self):
        """Test invoice number format"""
        status = counter_service.get_status()
        next_invoice = status['next_invoice']
        
        # Format: HD/YYYY-YY/XXX
        parts = next_invoice.split('/')
        assert len(parts) == 3
        assert parts[0] == 'HD'
        assert len(parts[1]) == 7  # YYYY-YY
        assert len(parts[2]) == 3  # XXX


class TestStorageService:
    """Test cloud storage service"""
    
    def test_get_storage_status(self):
        """Test storage status"""
        status = storage_service.get_storage_status()
        
        assert 'telegram' in status
        assert 'google_drive' in status
        assert 'enabled' in status['telegram']
        assert 'priority' in status['telegram']
    
    def test_storage_priority(self):
        """Test storage priority order"""
        status = storage_service.get_storage_status()
        
        # Telegram should have priority 1
        assert status['telegram']['priority'] == 1
        # Google Drive should have priority 2
        assert status['google_drive']['priority'] == 2


# Sample data for testing
SAMPLE_OCR_TEXT = """
Bill To:
Buen Manejo Del Campo India Pvt. Ltd.
Office no.4, 2nd Floor, Anmol Pride,
Baner, Pune - 411045
GSTIN NO: 27AAHCB7551K1ZB
"""

SAMPLE_USER_TEXT = """
Name- Buen manejo del Campo India pvt . Ltd
Mobile - 8889302969
Vehicle - Baleno
Rent :-₹16200
Kms-600km
Extra km charged:-551×8:-4408
Total:-20608
Duration -6 days
Start date and time - 25/01/2026 7am to 31/01/2026 7am
"""


class TestFullExtraction:
    """Test complete extraction pipeline"""
    
    def test_complete_extraction(self):
        """Test extracting all fields from sample data"""
        result = extraction_service.extract_booking_data(
            SAMPLE_OCR_TEXT,
            SAMPLE_USER_TEXT
        )
        
        # Check customer details
        assert result.get('customer_name') is not None
        assert result.get('mobile_number') == "8889302969"
        
        # Check vehicle details
        assert result.get('vehicle_name') is not None
        
        # Check pricing
        assert result.get('base_rent') == 16200
        assert result.get('total_amount') == 20608
        
        # Check duration
        assert result.get('duration_days') == 6


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
