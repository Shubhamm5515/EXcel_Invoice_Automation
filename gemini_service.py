"""
Gemini AI Service for Semantic Data Extraction
Uses Google's Gemini API to intelligently extract and structure invoice data
"""

import google.generativeai as genai
from typing import Dict, Any, Optional
import json
from config import settings


class GeminiDataExtractor:
    """Extract structured invoice data using Gemini AI"""
    
    def __init__(self):
        """Initialize Gemini API"""
        if settings.gemini_api_key and settings.gemini_api_key != "your_gemini_api_key_here":
            genai.configure(api_key=settings.gemini_api_key)
            self.model = genai.GenerativeModel(settings.gemini_model)
            self.enabled = True
        else:
            self.enabled = False
            print("⚠️  Gemini API key not configured. Using basic extraction.")
    
    def extract_invoice_data(self, ocr_text: str, user_text: str = "") -> Dict[str, Any]:
        """
        Extract structured invoice data from OCR text using Gemini AI
        
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
            response = self.model.generate_content(prompt)
            
            # Parse JSON response
            result_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.startswith("```"):
                result_text = result_text[3:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            
            data = json.loads(result_text.strip())
            
            # Add metadata
            data['extraction_method'] = 'gemini'
            data['extraction_confidence'] = 'high'
            
            return data
            
        except Exception as e:
            print(f"⚠️  Gemini extraction failed: {e}")
            return self._fallback_extraction(ocr_text, user_text)
    
    def _build_extraction_prompt(self, ocr_text: str, user_text: str) -> str:
        """Build the extraction prompt for Gemini"""
        
        prompt = f"""You are an expert invoice data extraction system for a car rental company called Hill Drive.

Extract structured booking data from the provided OCR text and user input. Return ONLY valid JSON with no markdown formatting.

**OCR TEXT (from image):**
{ocr_text}

**USER TEXT (typed details):**
{user_text}

**EXTRACTION RULES:**

1. **Customer Details:**
   - Extract customer_name, company_name, mobile_number, address
   - Clean up formatting (remove extra spaces, fix capitalization)
   - Validate phone numbers (10 digits)

2. **Vehicle Details:**
   - Extract vehicle_name (e.g., "Swift Dzire", "Baleno", "Ertiga")
   - Extract vehicle_number if available (e.g., "RJ14AB1234")

3. **Booking Period:**
   - Extract start_datetime and end_datetime
   - Convert to format: "YYYY-MM-DD HH:MM"
   - Handle formats like "25/01/2026 7am", "25-01-2026", "Jan 25, 2026"
   - Calculate duration_days from date range

4. **Pricing:**
   - Extract base_rent (base rental amount)
   - Extract included_km (kilometers included in base rent)
   - Extract extra_km (additional kilometers driven)
   - Extract extra_km_rate (rate per extra km)
   - Calculate extra_km_charge = extra_km × extra_km_rate
   - Extract extra_hour_rate if mentioned
   - Extract total_amount (final amount)

5. **Additional Charges:**
   - Extract security_deposit if mentioned
   - Extract pickup_drop_charges if mentioned
   - Extract other_charges if any

6. **Inclusions:**
   - Set fuel_included (true/false) - check for "fuel included" or "fuel not included"
   - Set toll_included (true/false) - check for "toll included" or "toll not included"
   - Set pickup_drop_extra (true/false) - check for "pickup drop extra" or "pickup drop included"

7. **Location:**
   - Extract place_of_supply (city/state)
   - Extract delivery_address if mentioned

8. **Calculation Verification:**
   - Verify: base_rent + extra_km_charge + other charges ≈ total_amount
   - Set calculation_verified to true if amounts match (within ±10 rupees)
   - Add notes if there's a mismatch

**REQUIRED JSON SCHEMA:**

{{
  "customer_name": "string or null",
  "company_name": "string or null",
  "mobile_number": "string or null",
  "address": "string or null",
  "gstin": "string or null",
  
  "vehicle_name": "string or null",
  "vehicle_number": "string or null",
  
  "start_datetime": "YYYY-MM-DD HH:MM or null",
  "end_datetime": "YYYY-MM-DD HH:MM or null",
  "duration_days": number or null,
  
  "base_rent": number or null,
  "included_km": number or null,
  "extra_km": number or null,
  "extra_km_rate": number or null,
  "extra_km_charge": number or null,
  "extra_hour_rate": number or null,
  
  "security_deposit": number or null,
  "pickup_drop_charges": number or null,
  "other_charges": number or null,
  
  "fuel_included": boolean or null,
  "toll_included": boolean or null,
  "pickup_drop_extra": boolean or null,
  
  "place_of_supply": "string or null",
  "delivery_address": "string or null",
  
  "total_amount": number or null,
  "advance_paid": number or null,
  
  "calculation_verified": boolean,
  "notes": "string or null"
}}

**IMPORTANT:**
- Return ONLY the JSON object, no markdown, no explanations
- Use null for missing values, don't invent data
- All amounts should be numbers (not strings)
- Dates must be in YYYY-MM-DD HH:MM format
- Phone numbers should be 10 digits (remove country code if present)
- Be smart about variations: "₹16200", "16,200", "16200/-" all mean 16200

Extract the data now:"""
        
        return prompt
    
    def _fallback_extraction(self, ocr_text: str, user_text: str) -> Dict[str, Any]:
        """Fallback extraction when Gemini is not available"""
        import re
        from datetime import datetime
        
        combined_text = f"{ocr_text}\n{user_text}"
        
        data = {
            'extraction_method': 'fallback',
            'extraction_confidence': 'medium',
            'notes': 'Extracted using basic pattern matching'
        }
        
        # Extract phone number
        phone_match = re.search(r'\b(\d{10})\b', combined_text)
        if phone_match:
            data['mobile_number'] = phone_match.group(1)
        
        # Extract amounts
        amounts = re.findall(r'₹?\s*(\d+(?:,\d+)*)', combined_text)
        if amounts:
            # Clean and convert
            amounts = [int(a.replace(',', '')) for a in amounts]
            if amounts:
                data['total_amount'] = max(amounts)  # Assume largest is total
        
        # Extract vehicle names (common models)
        vehicles = ['Swift', 'Dzire', 'Baleno', 'Ertiga', 'Innova', 'Fortuner', 'Creta']
        for vehicle in vehicles:
            if vehicle.lower() in combined_text.lower():
                data['vehicle_name'] = vehicle
                break
        
        # Extract dates
        date_patterns = [
            r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            r'(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4})'
        ]
        
        dates = []
        for pattern in date_patterns:
            dates.extend(re.findall(pattern, combined_text, re.IGNORECASE))
        
        if len(dates) >= 2:
            data['start_datetime'] = dates[0]
            data['end_datetime'] = dates[1]
        
        return data
    
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
        
        # Verify calculations
        if data.get('base_rent') and data.get('total_amount'):
            base = data['base_rent']
            extra = data.get('extra_km_charge', 0)
            other = data.get('other_charges', 0)
            pickup = data.get('pickup_drop_charges', 0)
            
            calculated_total = base + extra + other + pickup
            actual_total = data['total_amount']
            
            # Allow 10 rupee tolerance
            if abs(calculated_total - actual_total) <= 10:
                data['calculation_verified'] = True
            else:
                data['calculation_verified'] = False
                if not data.get('notes'):
                    data['notes'] = f"Amount mismatch: calculated {calculated_total}, actual {actual_total}"
        
        # Set defaults for missing boolean fields
        if 'fuel_included' not in data:
            data['fuel_included'] = False
        if 'toll_included' not in data:
            data['toll_included'] = False
        if 'pickup_drop_extra' not in data:
            data['pickup_drop_extra'] = False
        
        return data


# Singleton instance
gemini_extractor = GeminiDataExtractor()
