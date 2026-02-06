# 🚀 Quick Start Guide - Hill Drive Invoice Automation

## ✅ System Status

Your invoice automation system is **COMPLETE** and ready to use!

---

## 🎯 What You Have Now

✅ **OCR Processing** - Extract text from booking images  
✅ **AI Extraction** - Smart data extraction with OpenRouter  
✅ **Excel Generation** - Professional invoices with formulas  
✅ **Sequential Numbering** - HD/2026-27/007 (next invoice)  
✅ **Local Storage** - All invoices saved in `generated_invoices/`  
✅ **Cloud Backup** - Dropbox integration ready (needs setup)  
✅ **Month Organization** - Automatic month-wise folders  
✅ **Bulk Download** - Download entire month as ZIP  

---

## 🏃 Start Using NOW (2 Steps)

### Step 1: Install MEGA Package

```bash
pip install mega.py
```

### Step 2: Start Server

```bash
python main.py
```

Server will start on: **http://localhost:8002**

### Step 3: Create Invoice

1. Open: http://localhost:8002
2. Upload booking image OR type details
3. Click "Generate Invoice"
4. Download your invoice!

**That's it!** 🎉 You can start creating invoices immediately.

---

## ☁️ Enable Cloud Backup (Optional - 3 Minutes)

### Why Enable Cloud Backup?

- ✅ Automatic backup to MEGA
- ✅ **20GB FREE storage** (10x more than Dropbox!)
- ✅ End-to-end encryption
- ✅ Month-wise organization
- ✅ Download entire month as ZIP
- ✅ Access from anywhere

### How to Enable:

1. **Create MEGA Account** (2 minutes)
   - Go to: https://mega.nz/register
   - Enter email, password, name
   - Verify your email (check inbox)

2. **Add to .env** (1 minute)
   - Open `.env` file
   - Add:
     ```env
     MEGA_EMAIL=your_email@example.com
     MEGA_PASSWORD=your_password
     ```
   - Save file

3. **Install Package**
   ```bash
   pip install mega.py
   ```

4. **Restart Server**
   ```bash
   # Stop server (Ctrl+C)
   python main.py
   ```

**Done!** Invoices now auto-upload to MEGA with 20GB FREE storage! 🎉

**Detailed Guide:** See `MEGA_SETUP_GUIDE.md`

---

## 📊 Current Configuration

### Invoice Counter
- **Current:** HD/2026-27/006
- **Next:** HD/2026-27/007
- **Financial Year:** 2026-27

### Storage
- **Local:** `generated_invoices/` folder ✅
- **Cloud:** MEGA (not configured yet) ⚠️ - **20GB FREE when setup**

### AI Services
- **OCR:** OCR.space ✅
- **AI Extraction:** OpenRouter (Gemini 2.5 Flash) ✅

---

## 🎯 Common Tasks

### Create Invoice from Image

1. Open http://localhost:8002
2. Click "Choose File" or drag & drop
3. Upload booking screenshot
4. (Optional) Add details in "Additional Details"
5. Click "Generate Invoice"
6. Download invoice

### Create Invoice Manually

1. Open http://localhost:8002
2. Scroll to "Manual Entry" section
3. Fill in customer details
4. Fill in booking details
5. Click "Generate Invoice"
6. Download invoice

### Download Month as ZIP

**Via API:**
```bash
curl http://localhost:8002/api/mega/download-month?year=2026&month=2 -o Feb_2026.zip
```

**Via Browser:**
```
http://localhost:8002/api/mega/download-month?year=2026&month=2
```

### Check Invoice Counter

**Via API:**
```bash
curl http://localhost:8002/api/counter/status
```

**Via Browser:**
```
http://localhost:8002/api/counter/status
```

### Set Invoice Counter

**Via API:**
```bash
curl -X POST http://localhost:8002/api/counter/set \
  -F "start_number=100" \
  -F "financial_year=2026-27"
```

---

## 🔧 Troubleshooting

### Issue: Port 8002 already in use

**Solution:**
```bash
# Find process using port 8002
netstat -ano | findstr :8002

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F

# Or use a different port
python main.py --port 8003
```

### Issue: "Module not found: dropbox"

**Solution:**
```bash
pip install dropbox
```

### Issue: Name/Address not filling in Excel

**Solution:** This is already fixed! The system now:
- Extracts name from multiple patterns
- Extracts address with flexible patterns (any text with pincode)
- Tries both `mobile_number` and `phone_number` fields

### Issue: Dropbox not uploading

**Solution:**
1. Check `.env` has `MEGA_EMAIL` and `MEGA_PASSWORD`
2. Check credentials are correct (try logging in at https://mega.nz)
3. Check email is verified
4. Restart server

---

## 📚 Documentation

- **[MEGA_SETUP_GUIDE.md](MEGA_SETUP_GUIDE.md)** - Detailed MEGA setup
- **[CLOUD_BACKUP_COMPLETE.md](CLOUD_BACKUP_COMPLETE.md)** - Complete system overview
- **[DEPLOYMENT_QUICK_START.md](DEPLOYMENT_QUICK_START.md)** - Deploy to cloud
- **[INVOICE_COUNTER_GUIDE.md](INVOICE_COUNTER_GUIDE.md)** - Manage invoice numbers
- **[README.md](README.md)** - Full documentation

---

## 🎉 You're Ready!

Your invoice automation system is complete and ready to use. You can:

1. ✅ **Start creating invoices NOW** (without cloud backup)
2. ⚠️ **Setup MEGA** (3 minutes) for automatic cloud backup with 20GB FREE
3. 🚀 **Deploy to cloud** (optional) for remote access

**Next Steps:**
1. Create a test invoice to verify everything works
2. Setup MEGA for cloud backup (recommended - 20GB FREE)
3. Start using for real invoices!

**Need Help?** Check the documentation files listed above.

---

**Happy Invoicing! 🚗💨**
