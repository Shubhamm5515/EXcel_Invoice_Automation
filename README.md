# 🚗 Hill Drive Invoice Automation System

Automated invoice generation system with OCR, AI extraction, and cloud storage for Hill Drive car rental business.

## ✨ Features

- 🔍 **OCR Text Extraction** - Extract data from booking images
- 🤖 **AI-Powered Extraction** - Smart data extraction using OpenRouter AI
- 📄 **Excel Invoice Generation** - Professional invoices using custom template
- 📸 **Document Embedding** - Embed customer documents (Aadhaar, DL) in invoices
- ☁️ **Cloud Storage** - Auto-upload to Google Drive with month-wise folders
- 🔢 **Sequential Numbering** - HD/2026-27/036, 037, 038...
- 🌐 **Web Interface** - Easy-to-use web UI
- 🚀 **REST API** - Full API for integrations

## 🎯 Tech Stack

- **Backend:** FastAPI (Python 3.10+)
- **OCR:** OCR.space API
- **AI:** OpenRouter (Gemini 2.5 Flash)
- **Excel:** openpyxl
- **Storage:** Google Drive API
- **Deployment:** PythonAnywhere (Free, Always-On)

## 📋 Prerequisites

- Python 3.10 or higher
- OCR.space API key (free tier available)
- OpenRouter API key
- Google Drive API credentials (optional)

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/hilldrive-invoice.git
cd hilldrive-invoice
```

### 2. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment

Create `.env` file:

```env
OCR_SPACE_API_KEY=your_ocr_api_key
OPENROUTER_API_KEY=your_openrouter_key
OPENROUTER_MODEL=google/gemini-2.5-flash
USE_OPENROUTER=true
USE_MASTER_FILE=false
TEMPLATE_PATH=inn sample.xlsx
OUTPUT_DIR=generated_invoices
```

### 4. Run Server

```bash
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

Open: http://localhost:8001

## 📚 Documentation

- **[Deployment Guide](PYTHONANYWHERE_COMPLETE_GUIDE.md)** - Deploy to PythonAnywhere (Free)
- **[Google Drive Setup](GOOGLE_DRIVE_SETUP.md)** - Cloud storage configuration
- **[API Documentation](API_DOCUMENTATION.md)** - API endpoints reference
- **[Template Verification](TEMPLATE_VERIFICATION_COMPLETE.md)** - Template mapping

## 🌐 API Endpoints

### Health Check
```bash
GET /health
```

### Create Invoice (Manual)
```bash
POST /api/invoice/create
Content-Type: application/json

{
  "customer_name": "John Doe",
  "mobile_number": "9999888877",
  "vehicle_name": "Swift Dzire",
  "vehicle_number": "RJ14AB1234",
  "start_datetime": "2026-02-05 10:00",
  "end_datetime": "2026-02-07 10:00",
  "duration_days": 2,
  "base_rent": 3000,
  "security_deposit": 5000,
  "total_amount": 8000,
  "advance_paid": 8000
}
```

### Create Invoice (OCR)
```bash
POST /api/invoice/create-from-ocr
Content-Type: multipart/form-data

file: [booking_image.jpg]
user_text: "Additional details"
document_images: [aadhaar.jpg, dl.jpg]
```

### Download Invoice
```bash
GET /api/invoice/download/{invoice_id}
```

## 📁 Project Structure

```
hilldrive-invoice/
├── main.py                          # FastAPI application
├── config.py                        # Configuration
├── schemas.py                       # Pydantic models
├── hilldrive_excel_mapper.py        # Excel generation
├── ocr_service.py                   # OCR integration
├── openrouter_service.py            # AI extraction
├── google_drive_storage.py          # Cloud storage
├── implementation_example.py        # Data extraction
├── requirements.txt                 # Dependencies
├── .env                             # Environment variables (not in Git)
├── inn sample.xlsx                  # Invoice template
├── invoice_counter.json             # Sequential counter
├── static/                          # Web interface
│   ├── index.html
│   ├── style.css
│   └── script.js
└── generated_invoices/              # Output folder
```

## 🔧 Configuration

### Sequential Invoice Numbers

Edit `invoice_counter.json`:

```json
{
  "last_invoice_number": 35,
  "financial_year": "2026-27"
}
```

Next invoice will be: HD/2026-27/036

### Google Drive Integration

1. Setup Google Cloud project
2. Enable Drive API
3. Create service account
4. Download credentials as `google_credentials.json`
5. Place in project root

See [GOOGLE_DRIVE_SETUP.md](GOOGLE_DRIVE_SETUP.md) for details.

## 🚀 Deployment

### PythonAnywhere (Recommended - Free)

**Features:**
- ✅ Always-on (no cold start)
- ✅ Free forever
- ✅ Easy setup (30 minutes)

**Guide:** [PYTHONANYWHERE_COMPLETE_GUIDE.md](PYTHONANYWHERE_COMPLETE_GUIDE.md)

### Alternative Options

- **Railway.app** - $5/month, no cold start
- **Render.com** - Free tier with cold start
- **Oracle Cloud** - Free forever VPS

See [NO_COLD_START_DEPLOYMENT.md](NO_COLD_START_DEPLOYMENT.md) for comparison.

## 📊 Features in Detail

### Invoice Generation

- Professional Excel invoices
- Custom template support
- Formula preservation
- Sequential numbering
- Auto-calculation of GST

### OCR & AI Extraction

- Extract text from booking images
- AI-powered semantic understanding
- Automatic field mapping
- Fallback to pattern matching

### Document Management

- Embed customer documents in invoices
- High-quality image embedding (800x600, PNG, 300 DPI)
- Support for Aadhaar, DL, PAN, etc.

### Cloud Storage

- Auto-upload to Google Drive
- Month-wise folder organization (Feb 2026, Mar 2026)
- Download entire month at once
- Share access with team

## 🔒 Security

- Environment variables for sensitive data
- `.gitignore` for credentials
- HTTPS in production
- Service account for Drive API

## 🧪 Testing

```bash
# Test sequential numbering
python test_sequential_numbers.py

# Test individual files mode
python test_individual_files.py

# Test template verification
python test_template_verification.py

# Test Google Drive (requires credentials)
python google_drive_storage.py
```

## 📝 License

This project is private and proprietary to Hill Drive.

## 🤝 Support

For issues or questions:
- Check documentation in `/docs` folder
- Review deployment guides
- Contact: [Your Contact Info]

## 🎯 Roadmap

- [ ] Database integration for invoice history
- [ ] Email notifications
- [ ] SMS integration
- [ ] Mobile app
- [ ] Analytics dashboard
- [ ] Multi-language support

## 📸 Screenshots

### Web Interface
![Web Interface](docs/screenshots/web-interface.png)

### Invoice Sample
![Invoice Sample](docs/screenshots/invoice-sample.png)

### Google Drive Organization
![Drive Folders](docs/screenshots/drive-folders.png)

## 🙏 Acknowledgments

- FastAPI for the excellent framework
- OCR.space for OCR API
- OpenRouter for AI access
- Google Drive for cloud storage
- PythonAnywhere for free hosting

---

**Made with ❤️ for Hill Drive**

**Version:** 1.0.0  
**Last Updated:** February 2026
