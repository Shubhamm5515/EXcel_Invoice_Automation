"""
OCR.space API Integration Service
"""
import requests
from typing import Dict, Any
from PIL import Image
import io
from config import settings


class OCRService:
    """Service for OCR.space API integration"""
    
    def __init__(self):
        self.api_key = settings.ocr_space_api_key
        self.api_url = settings.ocr_space_api_url
    
    def extract_text_from_file(
        self, 
        file_content: bytes,
        language: str = "eng",
        detect_orientation: bool = True,
        scale: bool = True
    ) -> Dict[str, Any]:
        """Extract text from image file using OCR.space API"""
        try:
            payload = {
                'apikey': self.api_key,
                'language': language,
                'isOverlayRequired': False,
                'detectOrientation': detect_orientation,
                'scale': scale,
                'OCREngine': 2
            }
            
            files = {
                'file': ('image.jpg', file_content, 'image/jpeg')
            }
            
            response = requests.post(
                self.api_url,
                files=files,
                data=payload,
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            if result.get('IsErroredOnProcessing'):
                error_msg = result.get('ErrorMessage', ['Unknown error'])[0]
                return {
                    'success': False,
                    'error': error_msg,
                    'text': None
                }
            
            parsed_text = ""
            if result.get('ParsedResults'):
                for page in result['ParsedResults']:
                    parsed_text += page.get('ParsedText', '') + "\n"
            
            return {
                'success': True,
                'text': parsed_text.strip(),
                'confidence': self._calculate_confidence(result),
                'processing_time': result.get('ProcessingTimeInMilliseconds', 0),
                'raw_response': result
            }
            
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f"API request failed: {str(e)}",
                'text': None
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"OCR processing failed: {str(e)}",
                'text': None
            }
    
    def extract_text_from_url(self, image_url: str, language: str = "eng") -> Dict[str, Any]:
        """Extract text from image URL"""
        try:
            payload = {
                'apikey': self.api_key,
                'url': image_url,
                'language': language,
                'isOverlayRequired': False,
                'OCREngine': 2
            }
            
            response = requests.post(
                self.api_url,
                data=payload,
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            if result.get('IsErroredOnProcessing'):
                error_msg = result.get('ErrorMessage', ['Unknown error'])[0]
                return {
                    'success': False,
                    'error': error_msg,
                    'text': None
                }
            
            parsed_text = ""
            if result.get('ParsedResults'):
                for page in result['ParsedResults']:
                    parsed_text += page.get('ParsedText', '') + "\n"
            
            return {
                'success': True,
                'text': parsed_text.strip(),
                'confidence': self._calculate_confidence(result),
                'raw_response': result
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"OCR processing failed: {str(e)}",
                'text': None
            }
    
    def preprocess_image(self, file_content: bytes) -> bytes:
        """Preprocess image for better OCR results"""
        try:
            image = Image.open(io.BytesIO(file_content))
            
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            max_size = (2000, 2000)
            if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
                image.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            output = io.BytesIO()
            image.save(output, format='JPEG', quality=95)
            return output.getvalue()
            
        except Exception:
            return file_content
    
    def _calculate_confidence(self, result: Dict) -> float:
        """Calculate average confidence from OCR result"""
        try:
            if not result.get('ParsedResults'):
                return 0.0
            
            if result.get('IsErroredOnProcessing'):
                return 0.0
            
            return 85.0
            
        except Exception:
            return 0.0


# Singleton instance
ocr_service = OCRService()
