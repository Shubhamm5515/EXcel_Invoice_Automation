# 🚀 PythonAnywhere + Google Drive - Complete Setup Guide

## Overview

Deploy your invoice system to PythonAnywhere (free, always-on) with Google Drive API for cloud storage.

**Total Cost:** $0/month  
**Setup Time:** 30 minutes  
**Result:** Always-on API with cloud storage  

---

## Part 1: PythonAnywhere Deployment (15 min)

### Step 1: Create Account (2 min)

1. Go to: **https://www.pythonanywhere.com**
2. Click **"Pricing & signup"**
3. Choose **"Create a Beginner account"** (FREE)
4. Fill in details:
   - Username (e.g., `hilldrive`)
   - Email
   - Password
5. Verify email
6. Login

**Your URL will be:** `https://hilldrive.pythonanywhere.com`

---

### Step 2: Upload Your Code (5 min)

#### Option A: Using Git (Recommended)

1. Go to **"Consoles"** tab
2. Click **"Bash"**
3. Clone your repository:

```bash
git clone https://github.com/YOUR_USERNAME/hilldrive-invoice.git
cd hilldrive-invoice
```

#### Option B: Upload Files

1. Go to **"Files"** tab
2. Create folder: `hilldrive-invoice`
3. Upload all your files:
   - `main.py`
   - `config.py`
   - `schemas.py`
   - `hilldrive_excel_mapper.py`
   - `ocr_service.py`
   - `openrouter_service.py`
   - `google_drive_storage.py`
   - `requirements.txt`
   - `inn sample.xlsx`
   - `.env`

---

### Step 3: Install Dependencies (3 min)

In the Bash console:

```bash
cd hilldrive-invoice

# Create virtual environment
python3.10 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Wait for installation to complete (~2 min)**

---

### Step 4: Create Web App (5 min)

1. Go to **"Web"** tab
2. Click **"Add a new web app"**
3. Click **"Next"**
4. Choose **"Manual configuration"**
5. Select **"Python 3.10"**
6. Click **"Next"**

#### Configure WSGI File:

1. Click on **WSGI configuration file** link
2. Delete all content
3. Paste this:

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/hilldrive/hilldrive-invoice'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Activate virtual environment
activate_this = os.path.join(project_home, 'venv/bin/activate_this.py')
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Load environment variables
from dotenv import load_dotenv
load_dotenv(os.path.join(project_home, '.env'))

# Import FastAPI app
from main import app as application
```

4. Click **"Save"**

#### Configure Virtual Environment:

1. In **"Web"** tab, find **"Virtualenv"** section
2. Enter path: `/home/hilldrive/hilldrive-invoice/venv`
3. Click checkmark

#### Set Working Directory:

1. Find **"Code"** section
2. Set **"Source code"**: `/home/hilldrive/hilldrive-invoice`
3. Set **"Working directory"**: `/home/hilldrive/hilldrive-invoice`

---

### Step 5: Create Folders (1 min)

In Bash console:

```bash
cd hilldrive-invoice
mkdir -p generated_invoices
mkdir -p static
```

---

### Step 6: Reload Web App (1 min)

1. Go to **"Web"** tab
2. Click big green **"Reload"** button
3. Wait for reload to complete

---

### Step 7: Test Your App (1 min)

Open: `https://hilldrive.pythonanywhere.com`

You should see your web interface!

Test API:
```
https://hilldrive.pythonanywhere.com/health
```

Should return:
```json
{"status":"healthy","timestamp":"...","version":"1.0.0",...}
```

---

## Part 2: Google Drive API Setup (15 min)

### Step 1: Create Google Cloud Project (5 min)

1. Go to: **https://console.cloud.google.com**
2. Sign in with Google account
3. Click **"Select a project"** → **"New Project"**
4. Name: **"Hill Drive Invoices"**
5. Click **"Create"**
6. Wait for project creation

---

### Step 2: Enable Google Drive API (2 min)

1. Go to **"APIs & Services"** → **"Library"**
2. Search: **"Google Drive API"**
3. Click on it
4. Click **"Enable"**
5. Wait for activation

---

### Step 3: Create Service Account (5 min)

1. Go to **"APIs & Services"** → **"Credentials"**
2. Click **"Create Credentials"** → **"Service Account"**
3. Fill in:
   - **Name:** `invoice-uploader`
   - **Description:** `Uploads invoices to Google Drive`
4. Click **"Create and Continue"**
5. **Role:** Select **"Basic"** → **"Editor"**
6. Click **"Continue"**
7. Click **"Done"**

---

### Step 4: Generate JSON Key (3 min)

1. Click on the service account you just created
2. Go to **"Keys"** tab
3. Click **"Add Key"** → **"Create new key"**
4. Select **"JSON"**
5. Click **"Create"**
6. **Download** the JSON file (saves to your computer)

**Important:** Keep this file secure!

---

### Step 5: Upload Credentials to PythonAnywhere (2 min)

1. Go to PythonAnywhere **"Files"** tab
2. Navigate to: `/home/hilldrive/hilldrive-invoice/`
3. Click **"Upload a file"**
4. Upload the JSON file
5. Rename it to: **`google_credentials.json`**

---

### Step 6: Install Google API Package (2 min)

In Bash console:

```bash
cd hilldrive-invoice
source venv/bin/activate
pip install google-api-python-client google-auth
```

---

### Step 7: Test Google Drive Connection (1 min)

In Bash console:

```bash
python3
```

Then:

```python
from google_drive_storage import GoogleDriveStorage

storage = GoogleDriveStorage()
# Should print: ✅ Google Drive connected

exit()
```

---

### Step 8: Enable Auto-Upload (3 min)

Edit `main.py` to add auto-upload after invoice creation.

In PythonAnywhere, go to **"Files"** → open `main.py`

Add at the top (after other imports):

```python
from google_drive_storage import GoogleDriveStorage

# Initialize Google Drive storage
drive_storage = GoogleDriveStorage()
```

Find the invoice creation endpoints and add upload after file creation:

```python
# After: writer.write(booking_data, output_path)
# Add:
if drive_storage.service:
    drive_storage.upload_invoice(output_path)
```

**Save the file**

---

### Step 9: Reload Web App (1 min)

1. Go to **"Web"** tab
2. Click **"Reload"** button

---

### Step 10: Test Complete System (2 min)

1. Create an invoice via web interface
2. Check it appears in Google Drive:
   - Go to: https://drive.google.com
   - Look for folder: **"Hill Drive Invoices"**
   - Check month folder (e.g., **"Feb 2026"**)
   - Your invoice should be there!

---

## ✅ You're Live!

Your system is now:
- ✅ **Deployed** on PythonAnywhere (free, always-on)
- ✅ **Cloud storage** on Google Drive (15 GB free)
- ✅ **Month-wise folders** (Feb 2026, Mar 2026, etc.)
- ✅ **Auto-upload** after invoice creation
- ✅ **No cold start** - Always active

**URL:** `https://hilldrive.pythonanywhere.com`

---

## Folder Structure in Google Drive

```
Google Drive/
└── Hill Drive Invoices/
    └── 2026/
        ├── Jan 2026/
        ├── Feb 2026/
        │   ├── HD-20260205-abc123.xlsx
        │   ├── HD-20260205-def456.xlsx
        │   └── HD-20260205-ghi789.xlsx
        └── Mar 2026/
```

---

## Download Entire Month

### Option 1: Via Google Drive Web

1. Go to Google Drive
2. Navigate to month folder (e.g., "Feb 2026")
3. Right-click folder
4. Click "Download"
5. Gets all invoices as ZIP file

### Option 2: Via Python Script

Create `download_month.py`:

```python
from google_drive_storage import GoogleDriveStorage

storage = GoogleDriveStorage()

# Download all Feb 2026 invoices
storage.download_month_folder(2026, 2, 'downloads/Feb_2026')

print("✅ Downloaded all invoices!")
```

Run in Bash:
```bash
python download_month.py
```

---

## Share Access with Team

1. Go to Google Drive
2. Find "Hill Drive Invoices" folder
3. Right-click → "Share"
4. Add email addresses:
   - Accountant
   - Manager
   - Team members
5. Set permission:
   - **Viewer** - Can only view/download
   - **Editor** - Can add/edit files
6. Click "Send"

They can now access all invoices!

---

## Monitoring & Maintenance

### Check Logs

PythonAnywhere:
1. Go to **"Web"** tab
2. Click **"Log files"**
3. View:
   - Error log
   - Server log
   - Access log

### Check Storage Usage

Google Drive:
1. Go to: https://drive.google.com/settings/storage
2. See: Used / 15 GB
3. Upgrade if needed ($2/mo for 100 GB)

### Update Code

```bash
# In Bash console
cd hilldrive-invoice
git pull  # If using Git

# Or upload new files via Files tab

# Reload web app
# Go to Web tab → Click Reload
```

---

## Troubleshooting

### Web App Not Loading

**Check:**
1. WSGI file is correct
2. Virtual environment path is correct
3. All files uploaded
4. Dependencies installed

**Fix:**
- Check error log in Web tab
- Reload web app

### Google Drive Upload Failing

**Check:**
1. `google_credentials.json` exists
2. File has correct permissions
3. API is enabled

**Fix:**
```bash
# Test connection
python3
from google_drive_storage import GoogleDriveStorage
storage = GoogleDriveStorage()
```

### Import Errors

**Fix:**
```bash
cd hilldrive-invoice
source venv/bin/activate
pip install -r requirements.txt
```

Then reload web app.

---

## Upgrade Options

### PythonAnywhere

**Free (Current):**
- Always on
- 512 MB disk
- pythonanywhere.com domain

**Hacker ($5/month):**
- Custom domain
- More CPU time
- More disk space

### Google Drive

**Free (Current):**
- 15 GB storage

**Google One ($2/month):**
- 100 GB storage
- More than enough for years

---

## Security Checklist

- [x] `google_credentials.json` not in Git
- [x] `.env` not in Git
- [x] API keys in environment variables
- [x] HTTPS enabled (automatic on PythonAnywhere)
- [x] Service account has minimal permissions

---

## Backup Strategy

### Automatic (Google Drive)
- All invoices auto-uploaded
- Google Drive has version history
- Can restore deleted files

### Manual (Optional)
- Download month folders regularly
- Keep local backup
- Export to external drive

---

## Cost Summary

| Service | Cost | What You Get |
|---------|------|--------------|
| **PythonAnywhere** | $0 | Always-on hosting |
| **Google Drive** | $0 | 15 GB storage |
| **Domain (optional)** | $10/year | Custom domain |
| **Total** | **$0/month** | Full system! |

---

## Next Steps

1. ✅ Deploy to PythonAnywhere
2. ✅ Setup Google Drive API
3. ✅ Test invoice creation
4. ✅ Verify auto-upload
5. ✅ Share access with team
6. ✅ Start using!

---

## Support

**PythonAnywhere:**
- Forum: https://www.pythonanywhere.com/forums/
- Help: https://help.pythonanywhere.com/

**Google Drive API:**
- Docs: https://developers.google.com/drive
- Support: Google Cloud Console

---

**You now have a free, always-on invoice system with cloud storage!** 🎉

Need help with any step? Let me know!
