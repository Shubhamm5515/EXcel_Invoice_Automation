# 🎯 MEGA Cloud Backup Setup Guide

## Why MEGA?

✅ **FREE 20GB storage** (10x more than Dropbox!)  
✅ **No API token complexity** - just email & password  
✅ **End-to-end encryption** - Maximum security  
✅ **Month-wise folder organization**  
✅ **Bulk download as ZIP**  
✅ **Works immediately** - simple setup

---

## 📋 Step-by-Step Setup

### Step 1: Create MEGA Account

1. Go to **MEGA**: https://mega.nz/register

2. Fill in the form:
   - **Email**: Your email address
   - **Password**: Strong password (save it!)
   - **Name**: Your name
   - **Confirm**: Check the box

3. Click **"Create Account"**

4. **Verify your email** - Check your inbox and click the verification link

---

### Step 2: Add Credentials to .env

1. Open your `.env` file

2. Add your MEGA credentials:
```env
MEGA_EMAIL=your_email@example.com
MEGA_PASSWORD=your_strong_password
```

3. Save the file

⚠️ **IMPORTANT**: Keep your `.env` file secure! Don't share it or commit to Git.

---

### Step 3: Install MEGA Package

Run this command:

```bash
pip install mega.py
```

Or if using requirements.txt:

```bash
pip install -r requirements.txt
```

---

### Step 4: Restart Your Server

```bash
# Stop the server (Ctrl+C)

# Start again
python main.py
```

---

## ✅ Verify Setup

### Check Status API

Visit: http://localhost:8002/api/mega/status

You should see:
```json
{
  "enabled": true,
  "storage": "20 GB FREE",
  "message": "MEGA is connected"
}
```

### Test Upload

1. Create an invoice through the web interface
2. Check your MEGA account at: https://mega.nz/fm
3. Navigate to: `/Hill Drive Invoices/2026/Feb 2026/`
4. You should see the invoice file uploaded!

---

## 📁 Folder Structure

MEGA will automatically create this structure:

```
/Hill Drive Invoices/
  └── 2026/
      ├── Jan 2026/
      │   ├── HD-20260115-abc123.xlsx
      │   └── HD-20260120-def456.xlsx
      ├── Feb 2026/
      │   ├── HD-20260205-ghi789.xlsx
      │   └── HD-20260210-jkl012.xlsx
      └── Mar 2026/
          └── ...
```

---

## 🎯 API Endpoints

### 1. Check MEGA Status
```
GET /api/mega/status
```

### 2. Get Month Summary
```
GET /api/mega/month-summary?year=2026&month=2
```

Response:
```json
{
  "month": "Feb 2026",
  "count": 15,
  "files": [
    {
      "name": "HD-20260205-abc123.xlsx",
      "size": 45678,
      "timestamp": 1738742400
    }
  ]
}
```

### 3. Download Month as ZIP
```
GET /api/mega/download-month?year=2026&month=2
```

Downloads all invoices from February 2026 as a ZIP file.

---

## 🔄 How It Works

1. **Automatic Upload**: Every time you create an invoice, it's automatically uploaded to MEGA
2. **Month-wise Organization**: Invoices are organized by year and month
3. **Local + Cloud**: Invoices are saved locally AND uploaded to MEGA
4. **Bulk Download**: Download all invoices from any month as a single ZIP file

---

## 🆚 MEGA vs Others

| Feature | MEGA | Dropbox | Google Drive |
|---------|------|---------|--------------|
| Free Storage | **20 GB** | 2 GB | 15 GB |
| Setup Complexity | ⭐ Easy | ⭐ Easy | ⭐⭐⭐ Complex |
| Authentication | Email/Password | API Token | OAuth/JSON |
| Service Account Issues | ❌ None | ❌ None | ✅ Yes |
| Encryption | ✅ E2E | ❌ No | ❌ No |
| Works Immediately | ✅ Yes | ✅ Yes | ❌ Needs config |
| **Recommended** | ✅ **YES** | ⚠️ OK | ❌ No |

---

## 🚨 Troubleshooting

### Issue: "MEGA not configured"

**Solution**: Check your `.env` file has `MEGA_EMAIL` and `MEGA_PASSWORD` set

### Issue: "MEGA login failed"

**Solutions**: 
1. **Wrong credentials**: Double-check email and password
2. **Email not verified**: Check your inbox and verify email
3. **Special characters in password**: Try changing password to alphanumeric only
4. **Account suspended**: Login to https://mega.nz to check account status

### Issue: "Two-factor authentication enabled"

**Solution**: 
- MEGA API doesn't support 2FA
- Disable 2FA in MEGA settings: https://mega.nz/fm/account/security
- Or create a new MEGA account without 2FA

### Issue: Storage full

**Solution**: 
- Free tier: 20 GB
- Each invoice: ~50 KB
- Capacity: ~400,000 invoices
- If full, download old months and delete from MEGA
- Or upgrade to MEGA Pro (400 GB) = €4.99/month

---

## 💡 Pro Tips

1. **Download Monthly**: At the end of each month, download the ZIP and archive it locally
2. **Delete Old Months**: Free up MEGA space by deleting old months after archiving
3. **Use Strong Password**: MEGA is end-to-end encrypted, password is crucial
4. **Backup Credentials**: Save your email/password in a password manager
5. **Monitor Storage**: Check storage at https://mega.nz/fm/account

---

## 🔒 Security Features

MEGA provides **end-to-end encryption**:
- ✅ Files encrypted before upload
- ✅ Only you can decrypt (not even MEGA)
- ✅ Secure password-based authentication
- ✅ Zero-knowledge architecture

**This means your invoice data is completely private and secure!**

---

## 📊 Storage Capacity

**FREE Account:**
- Storage: 20 GB
- Transfer: 5 GB/month
- Perfect for: ~400,000 invoices

**MEGA Pro I (€4.99/month):**
- Storage: 400 GB
- Transfer: 1 TB/month
- Perfect for: Large businesses

**MEGA Pro II (€9.99/month):**
- Storage: 2 TB
- Transfer: 2 TB/month
- Perfect for: Enterprise

---

## 🎉 You're All Set!

Your invoices are now automatically backed up to MEGA in month-wise folders with **20GB FREE storage**!

**Next Steps**:
1. Create a test invoice
2. Check MEGA to see it uploaded
3. Try downloading a month as ZIP
4. Enjoy automatic cloud backup with 10x more storage! 🚀

---

## 🌐 MEGA Resources

- **Website**: https://mega.nz
- **Login**: https://mega.nz/login
- **File Manager**: https://mega.nz/fm
- **Account Settings**: https://mega.nz/fm/account
- **Help Center**: https://help.mega.io

---

**Made with ❤️ for Hill Drive**
