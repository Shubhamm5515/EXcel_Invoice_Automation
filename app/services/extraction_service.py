"""
Data Extraction Service - Coordinates AI and fallback extraction
"""
from typing import Dict, Any
from config import settings
from openrouter_service import openrouter_extractor
from gemini_service import gemini_extractor
from implementation_example import BookingDataExtractor


class ExtractionService:
    """Coordinate data extraction from multiple sources"""
    
    def __init__(self):
        self.fallback_extractor = BookingDataExtractor()
    
    def extract_booking_data(self, ocr_text: str, user_text: str = "") -> Dict[str, Any]:
        """
        Extract booking data using best available method
        
        Priority: OpenRouter → Gemini → Pattern Matching
        """
        # Try OpenRouter first
        if settings.use_openrouter and openrouter_extractor.enabled:
            try:
                data = openrouter_extractor.extract_invoice_data(ocr_text, user_text)
                data = openrouter_extractor.enhance_extracted_data(data)
                return data
            except Exception as e:
                print(f"⚠️  OpenRouter extraction failed: {e}")
        
        # Try Gemini as fallback
        if settings.use_gemini and gemini_extractor.enabled:
            try:
                data = gemini_extractor.extract_invoice_data(ocr_text, user_text)
                data = gemini_extractor.enhance_extracted_data(data)
                return data
            except Exception as e:
                print(f"⚠️  Gemini extraction failed: {e}")
        
        # Use pattern matching as last resort
        return self.fallback_extractor.extract(ocr_text, user_text)
    
    def get_extraction_method(self) -> str:
        """Get the current extraction method being used"""
        if settings.use_openrouter and openrouter_extractor.enabled:
            return "OpenRouter AI"
        elif settings.use_gemini and gemini_extractor.enabled:
            return "Gemini AI"
        else:
            return "Pattern Matching"


# Singleton instance
extraction_service = ExtractionService()
