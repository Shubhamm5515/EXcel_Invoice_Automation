# 🚗 Hill Drive Invoice Automation System

Automated invoice generation system with OCR, AI extraction, and cloud storage for Hill Drive car rental business.

## ✨ Features

- 🔍 **OCR Text Extraction** - Extract data from booking images
- 🤖 **AI-Powered Extraction** - Smart data extraction using OpenRouter AI
- 📄 **Excel Invoice Generation** - Professional invoices using custom template
- 📸 **Document Embedding** - Embed customer documents (Aadhaar, DL) in invoices
- ☁️ **Cloud Backup** - Auto-upload to Dropbox (FREE 2GB) or Google Drive
- 🔢 **Sequential Numbering** - HD/2026-27/036, 037, 038...
- 📦 **Month-wise Organization** - Invoices organized by month
- 💾 **Bulk Download** - Download entire month as ZIP
- 🌐 **Web Interface** - Easy-to-use web UI
- 🚀 **REST API** - Full API for integrations

## 🎯 Tech Stack

- **Backend:** FastAPI (Python 3.10+)
- **OCR:** OCR.space API
- **AI:** OpenRouter (Gemini 2.5 Flash)
- **Excel:** openpyxl
- **Cloud Storage:** Dropbox (recommended) or Google Drive
- **Deployment:** Render, Railway, or Local PC

## 📋 Prerequisites

- Python 3.10 or higher
- OCR.space API key (free tier available)
- OpenRouter API key (optional, for AI extraction)
- Dropbox access token (optional, for cloud backup - **RECOMMENDED**)
- Google Drive API credentials (optional, alternative to Dropbox)

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

# Cloud Backup (Optional - Recommended)
DROPBOX_ACCESS_TOKEN=your_dropbox_token
```

### 4. Run Server

```bash
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

Open: http://localhost:8001

## 📚 Documentation

- **[Cloud Backup Setup](DROPBOX_SETUP_GUIDE.md)** - Setup Dropbox cloud backup (5 minutes)
- **[Deployment Guide](DEPLOYMENT_QUICK_START.md)** - Deploy to Render, Railway, or Local PC
- **[Google Drive Alternative](GOOGLE_DRIVE_FIX.md)** - Why Dropbox is recommended over Google Drive
- **[Invoice Counter Guide](INVOICE_COUNTER_GUIDE.md)** - Manage sequential numbering
- **[Complete Status](CLOUD_BACKUP_COMPLETE.md)** - Full system overview

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

### Cloud Backup Status
```bash
GET /api/dropbox/status
GET /api/drive/status
```

### Download Month as ZIP
```bash
GET /api/dropbox/download-month?year=2026&month=2
```

### Invoice Counter Management
```bash
GET /api/counter/status
POST /api/counter/set
POST /api/counter/reset
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
├── dropbox_storage.py               # Dropbox cloud backup
├── google_drive_storage.py          # Google Drive (alternative)
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

### Cloud Backup Integration

**Dropbox (Recommended):**

1. Create Dropbox app at https://www.dropbox.com/developers/apps/create
2. Generate access token
3. Add to `.env`: `DROPBOX_ACCESS_TOKEN=your_token`
4. Restart server

**Features:**
- ✅ FREE 2GB storage
- ✅ Month-wise folders (Feb 2026, Mar 2026)
- ✅ Auto-upload after invoice creation
- ✅ Download entire month as ZIP
- ✅ No service account issues

See [DROPBOX_SETUP_GUIDE.md](DROPBOX_SETUP_GUIDE.md) for detailed instructions.

**Google Drive (Alternative):**

⚠️ **Not Recommended** - Service accounts have storage quota issues.

See [GOOGLE_DRIVE_FIX.md](GOOGLE_DRIVE_FIX.md) for details.

## 🚀 Deployment

### Render.com (Recommended)

**Features:**
- ✅ Free tier available
- ✅ Easy deployment
- ✅ Auto-deploy from Git
- ⚠️ Cold start on free tier

**Guide:** [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)

### Railway.app

**Features:**
- ✅ $5 free credit/month
- ✅ No cold start
- ✅ Simple setup

**Guide:** [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md)

### Local PC with ngrok

**Features:**
- ✅ Completely FREE
- ✅ Full control
- ✅ No cold start

**Guide:** [LOCAL_PC_DEPLOYMENT.md](LOCAL_PC_DEPLOYMENT.md)

See [DEPLOYMENT_QUICK_START.md](DEPLOYMENT_QUICK_START.md) for comparison.

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

- Auto-upload to Dropbox or Google Drive
- Month-wise folder organization (Feb 2026, Mar 2026)
- Download entire month as ZIP
- Priority: Dropbox → Google Drive → Local only
- FREE 2GB storage with Dropbox

## 🔒 Security

- Environment variables for sensitive data
- `.gitignore` for credentials
- HTTPS in production
- Service account for Drive API

## 🧪 Testing

```bash
# Test invoice creation
curl -X POST http://localhost:8002/api/invoice/create \
  -H "Content-Type: application/json" \
  -d '{"customer_name":"Test User","mobile_number":"9999888877"}'

# Check Dropbox status
curl http://localhost:8002/api/dropbox/status

# Check invoice counter
curl http://localhost:8002/api/counter/status
```

## 📝 License

This project is private and proprietary to Hill Drive.

## 🤝 Support

For issues or questions:
- Check documentation in `/docs` folder
- Review deployment guides
- Contact: [Your Contact Info]

## 🎯 Roadmap

- [x] OCR text extraction
- [x] AI-powered data extraction
- [x] Excel invoice generation
- [x] Sequential invoice numbering
- [x] Cloud backup (Dropbox)
- [x] Month-wise organization
- [x] Bulk download as ZIP
- [ ] Database integration for invoice history
- [ ] Email notifications
- [ ] SMS integration
- [ ] Mobile app
- [ ] Analytics dashboard

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
- Dropbox for cloud storage
- Google Drive for alternative storage
- Render/Railway for hosting options

---

**Made with ❤️ for Hill Drive**

**Version:** 2.0.0  
**Last Updated:** February 5, 2026  
**Status:** ✅ Production Ready with Cloud Backup
