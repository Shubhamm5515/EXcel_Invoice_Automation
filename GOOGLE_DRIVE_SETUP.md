# 🔧 Google Drive Setup Guide

## Overview

This guide will help you setup Google Drive API to automatically upload invoices to cloud storage organized by month.

---

## Step 1: Create Google Cloud Project (5 minutes)

1. **Go to:** https://console.cloud.google.com
2. **Sign in** with your Google account
3. **Click** "Select a project" → "New Project"
4. **Name:** "Hill Drive Invoices"
5. **Click** "Create"

---

## Step 2: Enable Google Drive API (2 minutes)

1. **Go to:** APIs & Services → Library
2. **Search:** "Google Drive API"
3. **Click** on it
4. **Click** "Enable"

---

## Step 3: Create Service Account (5 minutes)

1. **Go to:** APIs & Services → Credentials
2. **Click** "Create Credentials" → "Service Account"
3. **Name:** "invoice-uploader"
4. **Click** "Create and Continue"
5. **Role:** Select "Editor" (or "Drive File Creator")
6. **Click** "Done"

---

## Step 4: Generate JSON Key (2 minutes)

1. **Click** on the service account you just created
2. **Go to** "Keys" tab
3. **Click** "Add Key" → "Create new key"
4. **Select** "JSON"
5. **Click** "Create"
6. **Download** the JSON file

---

## Step 5: Setup in Your Project (1 minute)

1. **Rename** the downloaded file to `google_credentials.json`
2. **Move** it to your project folder (same folder as main.py)
3. **Add to .gitignore:**
   ```
   google_credentials.json
   ```

---

## Step 6: Install Required Package

```bash
pip install google-api-python-client google-auth
```

Or add to `requirements.txt`:
```
google-api-python-client==2.108.0
google-auth==2.25.2
```

---

## Step 7: Test Connection

```python
from google_drive_storage import GoogleDriveStorage

storage = GoogleDriveStorage()
# Should print: ✅ Google Drive connected
```

---

## Folder Structure

Invoices will be organized as:

```
Google Drive/
└── Hill Drive Invoices/
    └── 2026/
        ├── Jan 2026/
        │   ├── HD-2026-27-001.xlsx
        │   └── HD-2026-27-002.xlsx
        ├── Feb 2026/
        │   ├── HD-2026-27-036.xlsx
        │   ├── HD-2026-27-037.xlsx
        │   └── HD-2026-27-038.xlsx
        └── Mar 2026/
            └── HD-2026-27-039.xlsx
```

---

## Usage

### Auto-Upload After Invoice Creation

```python
from google_drive_storage import GoogleDriveStorage

storage = GoogleDriveStorage()

# After creating invoice
storage.upload_invoice('generated_invoices/HD-20260205-abc123.xlsx')
```

### Download Entire Month

```python
# Download all Feb 2026 invoices
storage.download_month_folder(2026, 2, 'downloads/Feb_2026')
```

### Get Month Summary

```python
summary = storage.get_month_summary(2026, 2)
print(f"Month: {summary['month']}")
print(f"Total invoices: {summary['count']}")
```

---

## Security Notes

⚠️ **Important:**

1. **Never commit** `google_credentials.json` to Git
2. **Add to .gitignore** immediately
3. **Keep secure** - it has access to your Drive
4. **Rotate keys** periodically for security

---

## Sharing Access

To give others access to the invoices folder:

1. **Open** Google Drive
2. **Find** "Hill Drive Invoices" folder
3. **Right-click** → Share
4. **Add** email addresses
5. **Set** permission (Viewer/Editor)

---

## Free Tier Limits

Google Drive API Free Tier:
- ✅ 15 GB storage
- ✅ Unlimited API calls
- ✅ No time limit
- ✅ No credit card required

Perfect for invoice storage!

---

## Troubleshooting

### "Credentials not found"
- Check file name: `google_credentials.json`
- Check location: Same folder as main.py

### "Permission denied"
- Check service account has Drive access
- Re-create credentials with correct role

### "Folder not created"
- Check API is enabled
- Check credentials are valid
- Check internet connection

---

## Alternative: Manual Setup

If you don't want to use API:

1. Create folders manually in Google Drive
2. Upload invoices manually
3. Share folder with team

But API is much better for automation!

---

## Next Steps

1. ✅ Setup Google Drive API (follow steps above)
2. ✅ Test connection
3. ✅ Enable auto-upload in main.py
4. ✅ Create first invoice
5. ✅ Verify it appears in Google Drive

**Total setup time: ~15 minutes**
