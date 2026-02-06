"""
Integration tests for API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from main_new import app

client = TestClient(app)


class TestHealthEndpoints:
    """Test health check endpoints"""
    
    def test_health_check(self):
        """Test /health endpoint"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'healthy'
        assert 'version' in data
        assert 'ocr_service' in data
        assert 'ai_service' in data
    
    def test_static_files_check(self):
        """Test /test-static endpoint"""
        response = client.get("/test-static")
        
        assert response.status_code == 200
        data = response.json()
        assert 'static_folder_exists' in data


class TestCounterEndpoints:
    """Test invoice counter endpoints"""
    
    def test_get_counter_status(self):
        """Test GET /api/counter/status"""
        response = client.get("/api/counter/status")
        
        assert response.status_code == 200
        data = response.json()
        assert 'current_number' in data
        assert 'financial_year' in data
        assert 'next_invoice' in data


class TestInvoiceEndpoints:
    """Test invoice management endpoints"""
    
    def test_list_invoices(self):
        """Test GET /api/invoice/list"""
        response = client.get("/api/invoice/list")
        
        assert response.status_code == 200
        data = response.json()
        assert 'invoices' in data
        assert 'count' in data
        assert isinstance(data['invoices'], list)
    
    def test_create_invoice_manual(self):
        """Test POST /api/invoice/create"""
        invoice_data = {
            "customer_name": "Test Customer",
            "mobile_number": "9999888877",
            "vehicle_name": "Swift Dzire",
            "start_datetime": "2026-02-10 10:00",
            "end_datetime": "2026-02-12 10:00",
            "duration_days": 2,
            "base_rent": 3000,
            "total_amount": 3000
        }
        
        response = client.post("/api/invoice/create", json=invoice_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data['success'] == True
        assert 'invoice_id' in data
        assert 'download_url' in data


class TestOCREndpoints:
    """Test OCR endpoints"""
    
    def test_ocr_extract_no_file(self):
        """Test OCR endpoint without file"""
        response = client.post("/api/ocr/extract")
        
        # Should fail without file
        assert response.status_code == 422  # Validation error


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
