# 🔧 Fix Google Drive "Service Account Storage Quota" Error

## Error Message:
```
Service Accounts do not have storage quota. Leverage shared drives or use OAuth delegation instead.
```

## 🎯 Solution: Use Shared Drive (Recommended)

Service accounts can't upload to regular Google Drive folders. You need to use a **Shared Drive** (formerly Team Drive).

---

## Option 1: Create Shared Drive (Best Solution)

### Step 1: Create Shared Drive

1. **Go to:** https://drive.google.com
2. **Click** "Shared drives" in left sidebar
3. **Click** "+ New" button
4. **Name:** "Hill Drive Invoices"
5. **Click** "Create"

### Step 2: Add Service Account as Member

1. **Open** the "Hill Drive Invoices" shared drive
2. **Click** the settings icon (⚙️) → "Manage members"
3. **Click** "Add members"
4. **Paste** your service account email:
   - Open `google_credentials.json`
   - Find `"client_email"`: `"invoice-uploader@xxxxx.iam.gserviceaccount.com"`
   - Copy that email
5. **Set role:** "Content manager" or "Manager"
6. **Uncheck** "Notify people"
7. **Click** "Send"

### Step 3: Update Code to Use Shared Drive

The code has been updated to support shared drives automatically!

Just restart your server:
```cmd
py -m uvicorn main:app --host 0.0.0.0 --port 8002 --reload
```

---

## Option 2: Share Regular Folder with Your Personal Account (Workaround)

If you can't create a Shared Drive:

### Step 1: Find Service Account Email

Open `google_credentials.json`:
```json
{
  "client_email": "invoice-uploader@hill-drive-invoices.iam.gserviceaccount.com"
}
```

### Step 2: Share Folder

1. Go to https://drive.google.com
2. Find "Hill Drive Invoices" folder
3. Right-click → Share
4. Add your **personal Gmail address** (not service account)
5. Give yourself "Editor" permission
6. Click "Share"

### Step 3: Upload to Your Drive

The service account will create folders in your personal Drive, and you'll have access to them.

**Note:** This is a workaround. Shared Drive is better for production.

---

## Option 3: Disable Google Drive Upload (Temporary)

If you want to skip Google Drive for now:

### Method 1: Rename Credentials File

```cmd
ren google_credentials.json google_credentials.json.backup
```

### Method 2: Comment Out in .env

Edit `.env`:
```env
# GOOGLE_CREDENTIALS_JSON=...
```

### Result:
- Invoices will be saved locally in `generated_invoices/` folder
- No cloud backup
- You can manually upload to Google Drive later

---

## Option 4: Use OAuth Instead of Service Account (Advanced)

This gives full access but requires user authentication.

### Not Recommended Because:
- More complex setup
- Requires user to login
- Token expires and needs refresh
- Service account is better for automation

---

## 🎯 Recommended Solution

**Use Option 1: Create Shared Drive**

This is the proper way to use service accounts with Google Drive:
1. Create Shared Drive (free, no limits)
2. Add service account as member
3. Upload works perfectly
4. No storage quota issues

---

## ✅ Verify Fix

After setting up Shared Drive:

1. **Restart server:**
   ```cmd
   py -m uvicorn main:app --host 0.0.0.0 --port 8002 --reload
   ```

2. **Create invoice**

3. **Check console output:**
   ```
   ✅ Uploaded to Google Drive: HD-20260205-abc123.xlsx
      Folder: Feb 2026
      Link: https://drive.google.com/...
   ```

4. **Verify in Google Drive:**
   - Go to "Shared drives" → "Hill Drive Invoices"
   - Check folders: 2026 → Feb 2026
   - Your invoice should be there!

---

## 🔍 Troubleshooting

### Issue: Can't create Shared Drive

**Reason:** Shared Drives require Google Workspace (paid) or Google One (paid)

**Solution:** Use Option 2 (share with personal account) or Option 3 (disable for now)

### Issue: Service account still can't upload

**Check:**
1. Service account has "Content manager" or "Manager" role
2. Shared Drive name is exactly "Hill Drive Invoices"
3. Credentials file is valid

### Issue: Folder not found

**Fix:** Delete old "Hill Drive Invoices" folder from regular Drive, create new one in Shared Drive

---

## 📊 Storage Limits

### Shared Drive:
- **Free (Google Workspace):** 30 GB per user
- **Paid:** Unlimited (Business plans)

### Regular Drive:
- **Free:** 15 GB
- **Paid:** 100 GB ($2/month), 200 GB ($3/month)

---

## 🎉 Summary

**Best Solution:**
1. Create Shared Drive named "Hill Drive Invoices"
2. Add service account as member with "Manager" role
3. Restart server
4. Upload works!

**Quick Workaround:**
1. Share "Hill Drive Invoices" folder with your personal Gmail
2. Service account uploads to your Drive
3. You can access files

**Temporary Fix:**
1. Disable Google Drive (rename credentials file)
2. Invoices saved locally only
3. Manual upload later

---

**Choose Option 1 if you have Google Workspace, otherwise use Option 2 or 3!**
