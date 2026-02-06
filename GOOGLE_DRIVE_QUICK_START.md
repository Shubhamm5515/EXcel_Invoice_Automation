# 🚀 Google Drive - Quick Start (5 Minutes)

Get Google Drive auto-upload working in 5 minutes!

---

## Step 1: Get Credentials (3 minutes)

1. **Go to:** https://console.cloud.google.com
2. **Create project:** "Hill Drive Invoices"
3. **Enable API:** Search "Google Drive API" → Enable
4. **Create Service Account:**
   - APIs & Services → Credentials
   - Create Credentials → Service Account
   - Name: `invoice-uploader`
   - Role: Editor
5. **Download JSON Key:**
   - Click service account
   - Keys tab → Add Key → Create new key → JSON
   - **Save the downloaded file!**

---

## Step 2: Add to Your Project (1 minute)

### For Local Development:

1. Rename downloaded file to: `google_credentials.json`
2. Move to project folder (same folder as `main.py`)
3. Done!

### For Render/Railway:

1. Open `google_credentials.json` in notepad
2. Copy entire content
3. In Render/Railway dashboard:
   - Add environment variable
   - Name: `GOOGLE_CREDENTIALS_JSON`
   - Value: Paste entire JSON content
4. Redeploy

---

## Step 3: Test (1 minute)

### Test Connection:

```bash
py -c "from google_drive_storage import GoogleDriveStorage; storage = GoogleDriveStorage(); print('✅ Works!' if storage.service else '❌ Failed')"
```

### Create Test Invoice:

1. Go to your app: `http://localhost:8001`
2. Create an invoice
3. Check console - should see:
   ```
   ✅ Uploaded to Google Drive: HD-20260205-abc123.xlsx
      Folder: Feb 2026
   ```

### Check Google Drive:

1. Go to: https://drive.google.com
2. Look for folder: **"Hill Drive Invoices"**
3. Open: **2026 → Feb 2026**
4. Your invoice is there!

---

## ✅ You're Done!

Now every invoice is automatically:
- ✅ Uploaded to Google Drive
- ✅ Organized by month
- ✅ Accessible from anywhere

---

## 📱 Using the Features

### View Month Summary:

```
GET http://localhost:8001/api/drive/month-summary?year=2026&month=2
```

Response:
```json
{
  "month": "Feb 2026",
  "count": 5,
  "files": [...]
}
```

### Download Entire Month:

```
GET http://localhost:8001/api/drive/download-month?year=2026&month=2
```

Downloads ZIP file with all February invoices!

### Or Use Google Drive:

1. Go to: https://drive.google.com
2. Open: **Hill Drive Invoices → 2026 → Feb 2026**
3. Right-click folder → **Download**
4. Get ZIP with all invoices!

---

## 🎯 Monthly Workflow

### End of Month:

1. **Check count:**
   ```
   /api/drive/month-summary?year=2026&month=2
   ```

2. **Download all:**
   ```
   /api/drive/download-month?year=2026&month=2
   ```
   Or download from Google Drive directly

3. **Backup:**
   - Save ZIP to external drive
   - Keep for accounting

4. **Done!**

---

## 👥 Share with Team

1. Go to Google Drive
2. Right-click **"Hill Drive Invoices"**
3. Click **"Share"**
4. Add team emails
5. Set permission (Viewer/Editor)
6. Send

Now team can access all invoices!

---

## 🔧 Troubleshooting

### "Credentials not found"

**Fix:** Make sure `google_credentials.json` is in project root folder

### "Permission denied"

**Fix:** 
1. Check Google Drive API is enabled
2. Regenerate service account key
3. Try again

### Works locally but not on Render

**Fix:** Add credentials as environment variable (see Step 2)

---

## 📊 Storage

- **Free:** 15 GB (enough for ~30,000 invoices)
- **Paid:** $2/month for 100 GB

---

## 🎉 Success!

Your invoices are now:
- ✅ Auto-backed up to cloud
- ✅ Organized by month
- ✅ Downloadable in bulk
- ✅ Accessible from anywhere
- ✅ Shareable with team

---

**For detailed setup, see: GOOGLE_DRIVE_COMPLETE_SETUP.md**
