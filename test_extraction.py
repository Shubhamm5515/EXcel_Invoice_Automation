"""
Test script to verify name and address extraction
"""

# Test OCR text (from your screenshot)
ocr_text = """
Bill To:
Buen Manejo Del Campo India Pvt. Ltd.
Office no.4, 2nd Floor, Anmol Pride,
Baner, Pune - 411045
GSTIN NO: 27AAHCB7551K1ZB
Mobile: 8829952535
"""

user_text = """
Name: Buen Manejo Del Campo India Pvt. Ltd.
Mobile: 8829952535
Vehicle: Aura - Self Drive
"""

print("="*60)
print("TESTING DATA EXTRACTION")
print("="*60)

# Test with implementation_example
from implementation_example import BookingDataExtractor

extractor = BookingDataExtractor()
data = extractor.extract(ocr_text, user_text)

print("\n📊 EXTRACTED DATA:")
print("="*60)
print(f"Customer Name: {data.get('customer_name')}")
print(f"Company Name: {data.get('company_name')}")
print(f"Address: {data.get('address')}")
print(f"Mobile: {data.get('mobile_number')}")
print(f"GSTIN: {data.get('gstin')}")
print("="*60)

# Check if critical fields are present
issues = []
if not data.get('customer_name') and not data.get('company_name'):
    issues.append("❌ No customer/company name extracted")
else:
    print("✅ Customer/Company name extracted")

if not data.get('address'):
    issues.append("❌ No address extracted")
else:
    print("✅ Address extracted")

if not data.get('mobile_number'):
    issues.append("❌ No mobile number extracted")
else:
    print("✅ Mobile number extracted")

if issues:
    print("\n⚠️  ISSUES FOUND:")
    for issue in issues:
        print(f"  {issue}")
else:
    print("\n🎉 ALL CRITICAL FIELDS EXTRACTED SUCCESSFULLY!")

# Test Excel writing
print("\n" + "="*60)
print("TESTING EXCEL WRITING")
print("="*60)

from hilldrive_excel_mapper import HillDriveExcelWriter

writer = HillDriveExcelWriter('inn sample.xlsx')
output_path = 'test_invoice.xlsx'

try:
    writer.write(data, output_path)
    print(f"\n✅ Excel file created: {output_path}")
    print("   Open the file to verify name and address are filled!")
except Exception as e:
    print(f"\n❌ Excel writing failed: {e}")
    import traceback
    traceback.print_exc()
