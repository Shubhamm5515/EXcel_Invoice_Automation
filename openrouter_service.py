"""
OpenRouter AI Service for Semantic Data Extraction
Uses OpenRouter API to access multiple AI models
"""

import requests
from typing import Dict, Any
import json
from config import settings


class OpenRouterDataExtractor:
    """Extract structured invoice data using OpenRouter AI"""
    
    def __init__(self):
        """Initialize OpenRouter API"""
        if settings.openrouter_api_key and settings.openrouter_api_key != "your_openrouter_api_key_here":
            self.api_key = settings.openrouter_api_key
            self.model = settings.openrouter_model
            self.api_url = "https://openrouter.ai/api/v1/chat/completions"
            self.enabled = True
            print(f"✅ OpenRouter AI enabled with model: {self.model}")
        else:
            self.enabled = False
            print("⚠️  OpenRouter API key not configured. Using basic extraction.")
    
    def extract_invoice_data(self, ocr_text: str, user_text: str = "") -> Dict[str, Any]:
        """
        Extract structured invoice data from OCR text using OpenRouter AI
        
        Args:
            ocr_text: Raw text from OCR
            user_text: Additional user-provided text
            
        Returns:
            Structured dictionary with invoice data
        """
        if not self.enabled:
            return self._fallback_extraction(ocr_text, user_text)
        
        try:
            prompt = self._build_extraction_prompt(ocr_text, user_text)
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:8001",
                "X-Title": "Hill Drive Invoice Automation"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.1,  # Low temperature for consistent extraction
                "max_tokens": 1000  # Limit tokens to avoid credit issues
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Extract the response text
            result_text = result['choices'][0]['message']['content'].strip()
            
            # Remove markdown code blocks if present
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.startswith("```"):
                result_text = result_text[3:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            
            data = json.loads(result_text.strip())
            
            # Add metadata
            data['extraction_method'] = 'openrouter'
            data['extraction_confidence'] = 'high'
            
            return data
            
        except Exception as e:
            print(f"⚠️  OpenRouter extraction failed: {e}")
            return self._fallback_extraction(ocr_text, user_text)
    
    def _build_extraction_prompt(self, ocr_text: str, user_text: str) -> str:
        """Build the extraction prompt for OpenRouter"""
        
        prompt = f"""You are an expert invoice data extraction system for a car rental company called Hill Drive.

Extract structured booking data from the provided OCR text and user input. Return ONLY valid JSON with no markdown formatting.

**OCR TEXT (from image):**
{ocr_text}

**USER TEXT (typed details):**
{user_text}

**EXTRACTION RULES:**

1. **Customer Details (CRITICAL - MUST EXTRACT):**
   - Extract customer_name OR company_name (handle formats like "Cx name:-Anirudh sharma", "NAME", "Bill To", "Company:")
   - If you see a company name, put it in BOTH customer_name AND company_name fields
   - Extract mobile_number (10 digits, handle "Cx no:- 6367498546", "Mobile:", "Phone:", "Contact:")
   - Extract address (VERY IMPORTANT - look for ANY text with 6-digit pincode)
     * Address can be: Plot no, Office no, Shop no, House no, Flat no
     * Include: street, area, city, state, pincode
     * Combine multiple lines if needed
     * Example: "Plot no 80 Balaji vihar 62 niwaru road jhotwara jaipur Rajasthan, 302012"
     * Example: "Office no.4, 2nd Floor, Anmol Pride, Baner, Pune - 411045"
   - Clean up formatting (proper capitalization)
   - If address is missing from OCR, try to extract from any text with pincode

2. **Vehicle Details:**
   - Extract vehicle_name from "Cat type:-Aura(RJ59CB2547)"
   - Extract vehicle_number from parentheses
   - Extract included_km from "Running km:-150km"

3. **Booking Period:**
   - Handle format: "21jan to 23jan 2026"
   - Handle time: "Time:-08:30am to 07:00pm"
   - Convert to format: "YYYY-MM-DD HH:MM"
   - Calculate duration_days

4. **Pricing:**
   - Extract base_rent from "Rent:-₹3200"
   - Extract security_deposit from "Security:-₹5000"
   - Extract total_amount from "Total:-₹8200"
   - Extract advance_paid from "Online received:-500"

5. **Inclusions:**
   - Handle "Fuel & Toll:-exclude" → fuel_included=false, toll_included=false

**REQUIRED JSON SCHEMA:**

{{
  "customer_name": "string or null",
  "mobile_number": "string or null",
  "address": "string or null (full address with plot/street/city/state/pincode)",
  "vehicle_name": "string or null",
  "vehicle_number": "string or null",
  "start_datetime": "YYYY-MM-DD HH:MM or null",
  "end_datetime": "YYYY-MM-DD HH:MM or null",
  "duration_days": number or null,
  "base_rent": number or null,
  "included_km": number or null,
  "security_deposit": number or null,
  "total_amount": number or null,
  "advance_paid": number or null,
  "fuel_included": boolean or null,
  "toll_included": boolean or null
}}

**IMPORTANT:**
- Return ONLY the JSON object, no markdown, no explanations
- Use null for missing values
- All amounts should be numbers (not strings)
- Dates must be in YYYY-MM-DD HH:MM format
- Phone numbers should be 10 digits

Extract the data now:"""
        
        return prompt
    
    def _fallback_extraction(self, ocr_text: str, user_text: str) -> Dict[str, Any]:
        """Fallback extraction when OpenRouter is not available"""
        from implementation_example import BookingDataExtractor
        
        extractor = BookingDataExtractor()
        return extractor.extract(ocr_text, user_text)
    
    def enhance_extracted_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhance and validate extracted data
        
        Args:
            data: Raw extracted data
            
        Returns:
            Enhanced and validated data
        """
        # Calculate missing fields
        if data.get('extra_km') and data.get('extra_km_rate') and not data.get('extra_km_charge'):
            data['extra_km_charge'] = data['extra_km'] * data['extra_km_rate']
        
        # Set defaults for missing boolean fields
        if 'fuel_included' not in data or data['fuel_included'] is None:
            data['fuel_included'] = False
        if 'toll_included' not in data or data['toll_included'] is None:
            data['toll_included'] = False
        
        return data


# Singleton instance
openrouter_extractor = OpenRouterDataExtractor()
