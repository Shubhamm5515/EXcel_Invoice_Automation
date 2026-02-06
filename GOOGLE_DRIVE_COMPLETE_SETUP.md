# 📁 Google Drive API - Complete Setup Guide

Automatically upload invoices to Google Drive organized by month, and download entire months at once.

---

## 📂 Folder Structure

Your invoices will be organized like this:

```
Google Drive/
└── Hill Drive Invoices/
    └── 2026/
        ├── Jan 2026/
        │   ├── HD-20260115-abc123.xlsx
        │   ├── HD-20260120-def456.xlsx
        │   └── HD-20260125-ghi789.xlsx
        ├── Feb 2026/
        │   ├── HD-20260205-jkl012.xlsx
        │   ├── HD-20260210-mno345.xlsx
        │   └── HD-20260215-pqr678.xlsx
        └── Mar 2026/
            └── ...
```

**Features:**
- ✅ Auto-upload after invoice creation
- ✅ Month-wise organization
- ✅ Download entire month at once
- ✅ View month summary via API
- ✅ 15 GB free storage

---

## 🚀 Setup (15 Minutes)

### Step 1: Create Google Cloud Project (3 minutes)

1. **Go to:** https://console.cloud.google.com
2. **Sign in** with your Google account
3. Click **"Select a project"** → **"New Project"**
4. **Project name:** `Hill Drive Invoices`
5. Click **"Create"**
6. Wait for project creation (~30 seconds)

---

### Step 2: Enable Google Drive API (2 minutes)

1. Make sure your new project is selected (top bar)
2. Go to **"APIs & Services"** → **"Library"**
3. Search: **"Google Drive API"**
4. Click on it
5. Click **"Enable"**
6. Wait for activation

---

### Step 3: Create Service Account (3 minutes)

1. Go to **"APIs & Services"** → **"Credentials"**
2. Click **"Create Credentials"** → **"Service Account"**
3. Fill in:
   - **Service account name:** `invoice-uploader`
   - **Service account ID:** (auto-filled)
   - **Description:** `Uploads invoices to Google Drive`
4. Click **"Create and Continue"**
5. **Grant this service account access to project:**
   - **Role:** Select **"Basic"** → **"Editor"**
6. Click **"Continue"**
7. Click **"Done"**

---

### Step 4: Generate JSON Key (2 minutes)

1. In **"Credentials"** page, find your service account
2. Click on the service account email
3. Go to **"Keys"** tab
4. Click **"Add Key"** → **"Create new key"**
5. Select **"JSON"**
6. Click **"Create"**
7. **JSON file downloads automatically** - save it!

**Important:** This file contains your credentials. Keep it secure!

---

### Step 5: Upload Credentials (2 minutes)

#### For Local Development:

1. Rename the downloaded file to: `google_credentials.json`
2. Move it to your project folder (same folder as `main.py`)
3. Make sure it's in `.gitignore` (already added)

#### For Render/Railway Deployment:

**Option A: Upload as File (Render)**
1. Go to Render dashboard → Your service
2. Go to **"Shell"** tab
3. Upload `google_credentials.json` to project root

**Option B: Environment Variable (Better)**
1. Open `google_credentials.json` in text editor
2. Copy entire content
3. In Render/Railway dashboard:
   - Add environment variable: `GOOGLE_CREDENTIALS_JSON`
   - Paste the entire JSON content as value

Then update `google_drive_storage.py` to read from env var (I'll provide code below).

---

### Step 6: Test Connection (1 minute)

Run this in your project folder:

```bash
py -c "from google_drive_storage import GoogleDriveStorage; storage = GoogleDriveStorage(); print('✅ Connected!' if storage.service else '❌ Failed')"
```

You should see: `✅ Google Drive connected`

---

### Step 7: Share Folder Access (Optional - 2 minutes)

If you want to access invoices from your personal Google Drive:

1. Go to: https://drive.google.com
2. Find **"Hill Drive Invoices"** folder (created automatically)
3. Right-click → **"Share"**
4. Add your email address
5. Set permission: **"Editor"** or **"Viewer"**
6. Click **"Send"**

Now you can access invoices from your Google Drive!

---

## 🔧 Update Code for Environment Variable (Optional)

If deploying to Render/Railway, update `google_drive_storage.py`:

### Add this at the top:

```python
import json
import os
from google.oauth2 import service_account
```

### Update `__init__` method:

```python
def __init__(self, credentials_file: str = 'google_credentials.json'):
    """Initialize Google Drive client"""
    self.service = None
    self.root_folder_id = None
    
    # Try environment variable first (for deployment)
    credentials_json = os.getenv('GOOGLE_CREDENTIALS_JSON')
    
    if credentials_json:
        try:
            # Load from environment variable
            credentials_dict = json.loads(credentials_json)
            SCOPES = ['https://www.googleapis.com/auth/drive.file']
            credentials = service_account.Credentials.from_service_account_info(
                credentials_dict, scopes=SCOPES
            )
            self.service = build('drive', 'v3', credentials=credentials)
            print("✅ Google Drive connected (from environment)")
            return
        except Exception as e:
            print(f"⚠️  Failed to load from environment: {e}")
    
    # Fallback to file
    if os.path.exists(credentials_file):
        self._initialize_service()
    else:
        print(f"⚠️  Google Drive credentials not found")
        print(f"   Upload feature disabled. See GOOGLE_DRIVE_COMPLETE_SETUP.md")
```

---

## 📊 API Endpoints

Your app already has these endpoints:

### 1. Upload Invoice (Automatic)

When you create an invoice, it's automatically uploaded to Google Drive.

```
POST /api/invoice/create
POST /api/invoice/create-from-ocr
```

### 2. Get Month Summary

```
GET /api/drive/month-summary?year=2026&month=2
```

Response:
```json
{
  "month": "Feb 2026",
  "count": 15,
  "files": [
    {
      "id": "abc123",
      "name": "HD-20260205-abc123.xlsx",
      "createdTime": "2026-02-05T10:30:00Z",
      "size": "45678",
      "webViewLink": "https://drive.google.com/..."
    }
  ]
}
```

### 3. Download Month (Coming Soon)

I'll add an endpoint to download entire month as ZIP file.

---

## 🎯 How It Works

### Auto-Upload Flow:

1. User creates invoice via web interface
2. Invoice saved to `generated_invoices/` folder
3. **Automatically uploaded to Google Drive**
4. Organized in month folder (e.g., "Feb 2026")
5. User can download from Google Drive anytime

### Month-End Download:

1. User goes to Google Drive
2. Opens **"Hill Drive Invoices/2026/Feb 2026"**
3. Right-click folder → **"Download"**
4. Gets ZIP file with all February invoices

**Or via API:**
```
GET /api/drive/download-month?year=2026&month=2
```

---

## 💡 Usage Examples

### View February 2026 Invoices:

```
https://your-app.com/api/drive/month-summary?year=2026&month=2
```

### Download February 2026:

Go to Google Drive:
```
Hill Drive Invoices → 2026 → Feb 2026 → Right-click → Download
```

Or use API (I'll add this endpoint).

---

## 🔐 Security Best Practices

### 1. Never Commit Credentials

`.gitignore` already includes:
```
google_credentials.json
```

### 2. Use Environment Variables for Deployment

Store credentials as environment variable, not as file.

### 3. Limit Service Account Permissions

Only grant "Editor" role, not "Owner".

### 4. Rotate Keys Regularly

Generate new keys every 6-12 months.

### 5. Monitor Usage

Check Google Cloud Console for unusual activity.

---

## 📈 Storage Limits

### Free Tier (Google Drive):
- **15 GB** storage
- Shared with Gmail and Photos
- Enough for ~30,000 invoices (assuming 500 KB each)

### If You Need More:

**Google One Plans:**
- **100 GB:** $2/month
- **200 GB:** $3/month
- **2 TB:** $10/month

---

## 🧪 Testing

### Test Upload:

```python
from google_drive_storage import GoogleDriveStorage

storage = GoogleDriveStorage()

# Upload test file
file_id = storage.upload_invoice('generated_invoices/test.xlsx')
print(f"Uploaded! File ID: {file_id}")
```

### Test Download:

```python
# Download February 2026 invoices
storage.download_month_folder(2026, 2, 'downloads/Feb_2026')
```

### Test Summary:

```python
# Get February summary
summary = storage.get_month_summary(2026, 2)
print(f"February has {summary['count']} invoices")
```

---

## 🔧 Troubleshooting

### Issue 1: "Credentials not found"

**Fix:**
- Make sure `google_credentials.json` is in project root
- Check file name is exactly `google_credentials.json`
- Verify file is valid JSON

### Issue 2: "Permission denied"

**Fix:**
- Make sure Google Drive API is enabled
- Check service account has "Editor" role
- Regenerate credentials if needed

### Issue 3: "Folder not created"

**Fix:**
- Check internet connection
- Verify API quota not exceeded
- Check service account permissions

### Issue 4: Upload works locally but not on Render

**Fix:**
- Use environment variable method
- Add `GOOGLE_CREDENTIALS_JSON` to Render environment variables
- Update code to read from environment variable

---

## 📱 Mobile Access

### Access from Phone:

1. Install Google Drive app
2. Sign in with your Google account
3. Navigate to **"Hill Drive Invoices"**
4. View/download any invoice
5. Share invoices directly from app

---

## 👥 Team Access

### Share with Team Members:

1. Go to Google Drive
2. Right-click **"Hill Drive Invoices"** folder
3. Click **"Share"**
4. Add team member emails:
   - **Viewer:** Can only view/download
   - **Editor:** Can add/edit/delete files
5. Click **"Send"**

Team members can now access all invoices!

---

## 📊 Monthly Workflow

### End of Month Process:

1. **View Summary:**
   ```
   GET /api/drive/month-summary?year=2026&month=2
   ```

2. **Download All Invoices:**
   - Go to Google Drive
   - Open month folder
   - Right-click → Download
   - Get ZIP file with all invoices

3. **Backup:**
   - Save ZIP file to external drive
   - Or upload to another cloud service

4. **Accounting:**
   - Extract ZIP
   - Import to accounting software
   - Generate reports

---

## ✅ Setup Checklist

- [ ] Google Cloud project created
- [ ] Google Drive API enabled
- [ ] Service account created
- [ ] JSON key downloaded
- [ ] Credentials file in project folder
- [ ] Connection tested successfully
- [ ] Folder shared with team (optional)
- [ ] Test invoice uploaded
- [ ] Month summary works
- [ ] Download tested

---

## 🎉 You're All Set!

Your invoice system now:
- ✅ Auto-uploads to Google Drive
- ✅ Organizes by month automatically
- ✅ Allows bulk download
- ✅ Accessible from anywhere
- ✅ Shareable with team
- ✅ 15 GB free storage

---

## 🆘 Need Help?

- **Google Drive API Docs:** https://developers.google.com/drive
- **Service Account Guide:** https://cloud.google.com/iam/docs/service-accounts
- **Troubleshooting:** https://developers.google.com/drive/api/guides/troubleshoot

---

**Your invoices are now safely backed up to Google Drive! 📁✨**
