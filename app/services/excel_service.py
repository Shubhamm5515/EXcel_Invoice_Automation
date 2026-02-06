"""
Excel Invoice Generation Service
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
from hilldrive_excel_mapper import HillDriveExcelWriter
from config import settings


class ExcelService:
    """Handle Excel invoice generation"""
    
    def __init__(self):
        self.writer = HillDriveExcelWriter(
            settings.template_path,
            settings.master_file_path
        )
    
    def create_invoice(
        self,
        booking_data: Dict[str, Any],
        invoice_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create Excel invoice from booking data
        
        Returns:
            Dict with invoice_id, file_path, and other metadata
        """
        # Generate invoice ID if not provided
        if not invoice_id:
            invoice_id = self._generate_invoice_id()
        
        # Create invoice based on mode
        if settings.use_master_file:
            result = self._create_master_file_invoice(booking_data)
            return {
                'invoice_id': invoice_id,
                'file_path': result['master_file'],
                'sheet_name': result['sheet_name'],
                'mode': 'master'
            }
        else:
            file_path = self._create_separate_invoice(booking_data, invoice_id)
            return {
                'invoice_id': invoice_id,
                'file_path': file_path,
                'mode': 'separate'
            }
    
    def _create_master_file_invoice(self, booking_data: Dict[str, Any]) -> Dict[str, str]:
        """Add invoice as new sheet to master file"""
        result = self.writer.write_to_master(booking_data)
        return result
    
    def _create_separate_invoice(self, booking_data: Dict[str, Any], invoice_id: str) -> str:
        """Create separate invoice file"""
        import os
        output_filename = f"{invoice_id}.xlsx"
        output_path = os.path.join(settings.output_dir, output_filename)
        self.writer.write(booking_data, output_path)
        return output_path
    
    def _generate_invoice_id(self) -> str:
        """Generate unique invoice ID"""
        return f"HD-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6]}"


# Singleton instance
excel_service = ExcelService()
