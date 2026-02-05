"""
OCR.space API Integration Service
Free tier: 25,000 requests/month
"""
import requests
from typing import Optional, Dict, Any
from PIL import Image
import io
import base64
from config import settings


class OCRSpaceService:
    """Service for OCR.space API integration"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.ocr_space_api_key
        self.api_url = settings.ocr_space_api_url
    
    def extract_text_from_file(
        self, 
        file_content: bytes,
        language: str = "eng",
        detect_orientation: bool = True,
        scale: bool = True
    ) -> Dict[str, Any]:
        """
        Extract text from image file using OCR.space API
        
        Args:
            file_content: Image file content as bytes
            language: OCR language (eng, ara, chs, etc.)
            detect_orientation: Auto-rotate image
            scale: Upscale image for better OCR
            
        Returns:
            Dictionary with OCR results
        """
        try:
            # Prepare the payload
            payload = {
                'apikey': self.api_key,
                'language': language,
                'isOverlayRequired': False,
                'detectOrientation': detect_orientation,
                'scale': scale,
                'OCREngine': 2  # Engine 2 is better for complex layouts
            }
            
            # Prepare the file
            files = {
                'file': ('image.jpg', file_content, 'image/jpeg')
            }
            
            # Make API request
            response = requests.post(
                self.api_url,
                files=files,
                data=payload,
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Check for errors
            if result.get('IsErroredOnProcessing'):
                error_msg = result.get('ErrorMessage', ['Unknown error'])[0]
                return {
                    'success': False,
                    'error': error_msg,
                    'text': None
                }
            
            # Extract text from all pages
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
    
    def extract_text_from_url(
        self,
        image_url: str,
        language: str = "eng"
    ) -> Dict[str, Any]:
        """
        Extract text from image URL
        
        Args:
            image_url: Public URL of the image
            language: OCR language
            
        Returns:
            Dictionary with OCR results
        """
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
    
    def _calculate_confidence(self, result: Dict) -> float:
        """
        Calculate average confidence from OCR result
        
        Args:
            result: OCR.space API response
            
        Returns:
            Confidence score (0-100)
        """
        try:
            if not result.get('ParsedResults'):
                return 0.0
            
            # OCR.space doesn't provide confidence directly
            # We estimate based on error status and text quality
            if result.get('IsErroredOnProcessing'):
                return 0.0
            
            # If we got text, assume reasonable confidence
            # In production, you might want more sophisticated logic
            return 85.0
            
        except Exception:
            return 0.0
    
    def preprocess_image(self, file_content: bytes) -> bytes:
        """
        Preprocess image for better OCR results
        
        Args:
            file_content: Original image bytes
            
        Returns:
            Preprocessed image bytes
        """
        try:
            # Open image
            image = Image.open(io.BytesIO(file_content))
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize if too large (OCR.space free tier limit: 1MB)
            max_size = (2000, 2000)
            if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
                image.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Save to bytes
            output = io.BytesIO()
            image.save(output, format='JPEG', quality=95)
            return output.getvalue()
            
        except Exception as e:
            # If preprocessing fails, return original
            return file_content


# Create service instance
ocr_service = OCRSpaceService()
