"""
Invoice Counter Service
"""
import json
import os
from datetime import datetime
from typing import Dict, Any


class CounterService:
    """Manage invoice counter and numbering"""
    
    def __init__(self, counter_file: str = 'invoice_counter.json'):
        self.counter_file = counter_file
    
    def get_status(self) -> Dict[str, Any]:
        """Get current counter status"""
        counter_data = self._load_counter()
        
        next_number = counter_data['last_invoice_number'] + 1
        next_invoice = f"HD/{counter_data['financial_year']}/{next_number:03d}"
        
        return {
            'current_number': counter_data['last_invoice_number'],
            'financial_year': counter_data['financial_year'],
            'next_invoice': next_invoice,
            'last_invoice': f"HD/{counter_data['financial_year']}/{counter_data['last_invoice_number']:03d}" if counter_data['last_invoice_number'] > 0 else None
        }
    
    def set_counter(self, start_number: int, financial_year: str = None) -> Dict[str, Any]:
        """Set counter to specific number"""
        if start_number < 1:
            raise ValueError("Start number must be at least 1")
        
        if not financial_year:
            financial_year = self._get_current_financial_year()
        
        counter_data = {
            'last_invoice_number': start_number - 1,
            'financial_year': financial_year
        }
        
        self._save_counter(counter_data)
        
        return {
            'success': True,
            'next_invoice': f"HD/{financial_year}/{start_number:03d}",
            'financial_year': financial_year,
            'start_number': start_number
        }
    
    def reset_counter(self, financial_year: str = None) -> Dict[str, Any]:
        """Reset counter for new financial year"""
        if not financial_year:
            financial_year = self._get_current_financial_year()
        
        counter_data = {
            'last_invoice_number': 0,
            'financial_year': financial_year
        }
        
        self._save_counter(counter_data)
        
        return {
            'success': True,
            'next_invoice': f"HD/{financial_year}/001",
            'financial_year': financial_year
        }
    
    def _load_counter(self) -> Dict[str, Any]:
        """Load counter from file"""
        if os.path.exists(self.counter_file):
            with open(self.counter_file, 'r') as f:
                return json.load(f)
        else:
            return {
                'last_invoice_number': 0,
                'financial_year': self._get_current_financial_year()
            }
    
    def _save_counter(self, counter_data: Dict[str, Any]):
        """Save counter to file"""
        with open(self.counter_file, 'w') as f:
            json.dump(counter_data, f, indent=2)
    
    def _get_current_financial_year(self) -> str:
        """Get current financial year in YYYY-YY format"""
        now = datetime.now()
        year = now.year
        next_year = (year + 1) % 100
        return f"{year}-{next_year:02d}"


# Singleton instance
counter_service = CounterService()
