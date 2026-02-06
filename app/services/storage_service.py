"""
Cloud Storage Service - Local storage only
"""
from typing import Optional
from datetime import datetime
import os


class StorageService:
    """Local storage service - saves invoices to disk"""
    
    def __init__(self):
        self.output_dir = "generated_invoices"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def upload_invoice(
        self,
        file_path: str,
        invoice_date: Optional[datetime] = None
    ) -> dict:
        """
        Save invoice locally
        
        Returns:
            Dict with save status and details
        """
        result = {
            'uploaded': False,
            'provider': 'local',
            'file_id': None,
            'error': None,
            'file_path': file_path
        }
        
        # Check if file exists
        if os.path.exists(file_path):
            result['uploaded'] = True
            result['file_id'] = os.path.basename(file_path)
            print(f"✅ Invoice saved locally: {file_path}")
        else:
            result['error'] = "File not found"
            print(f"❌ File not found: {file_path}")
        
        return result
    
    def get_storage_status(self) -> dict:
        """Get status of storage"""
        return {
            'local': {
                'enabled': True,
                'priority': 1,
                'output_dir': self.output_dir
            }
        }


# Singleton instance
storage_service = StorageService()
