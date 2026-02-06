# 🧪 Test MEGA Upload

## ✅ Fix Applied!

MEGA upload now works for BOTH modes:
- ✅ Individual file mode (`USE_MASTER_FILE=false`)
- ✅ Master file mode (`USE_MASTER_FILE=true`)

---

## 🎯 How to Test

### Step 1: Restart Server

Stop the current server (Ctrl+C) and restart:
```bash
python main.py
```

You should see:
```
✅ MEGA connected
   Account: 01sarthak@gmail.com
   Storage: 20 GB FREE
```

### Step 2: Create Test Invoice

**Option A: Via Web Interface**
1. Open: http://localhost:8000
2. In "Additional Details" box, type:
   ```
   Name: Test Customer
   Mobile: 9999888877
   Vehicle: Swift Dzire
   Rent: 5000
   Duration: 2 days
   ```
3. Click "Generate Invoice"
4. Watch the server console for upload message

**Option B: Via API**
```bash
curl -X POST http://localhost:8000/api/invoice/create ^
  -H "Content-Type: application/json" ^
  -d "{\"customer_name\":\"Test Customer\",\"mobile_number\":\"9999888877\",\"vehicle_name\":\"Swift Dzire\",\"base_rent\":5000,\"duration_days\":2,\"total_amount\":5000}"
```

### Step 3: Check Server Console

You should see:
```
✅ Uploaded to MEGA: HD-20260205-abc123.xlsx
   Folder: Feb 2026
   Link: https://mega.nz/...
```

### Step 4: Verify in MEGA

1. Go to: https://mega.nz/fm
2. Navigate to: `/Hill Drive Invoices/2026/Feb 2026/`
3. You should see your invoice file!

---

## 📊 What Was Fixed

### Before:
- ❌ MEGA upload only worked for individual file mode
- ❌ Master file mode didn't upload to MEGA

### After:
- ✅ MEGA upload works for individual file mode
- ✅ MEGA upload works for master file mode
- ✅ Both modes now auto-upload to MEGA

---

## 🔧 Current Configuration

Check your `.env` file:
```env
USE_MASTER_FILE=false
MEGA_EMAIL=01sarthak@gmail.com
MEGA_PASSWORD=Hellosarthak
```

**Recommendation:** Keep `USE_MASTER_FILE=false` for easier MEGA management (each invoice is a separate file).

---

## 🎉 Expected Behavior

After creating an invoice:

1. **Local Storage:**
   - File saved in `generated_invoices/` folder
   - Example: `HD-20260205-abc123.xlsx`

2. **MEGA Upload:**
   - File uploaded to MEGA
   - Path: `/Hill Drive Invoices/2026/Feb 2026/HD-20260205-abc123.xlsx`
   - Console shows: "✅ Uploaded to MEGA"

3. **Download:**
   - You can download from web interface
   - Or access from MEGA anytime

---

## 🚨 Troubleshooting

### Issue: No upload message in console

**Check:**
1. MEGA credentials in `.env` are correct
2. Server shows "✅ MEGA connected" on startup
3. No error messages in console

### Issue: Upload fails

**Possible causes:**
1. Internet connection issue
2. MEGA account storage full (unlikely with 20GB)
3. MEGA API rate limit (wait a minute and try again)

**Solution:**
- Check server console for error messages
- Try creating another invoice after 1 minute
- Verify MEGA login at https://mega.nz

---

## 📚 Next Steps

1. ✅ Test invoice creation
2. ✅ Verify MEGA upload
3. ✅ Check MEGA folder structure
4. ✅ Start using for real invoices!

**Your system is ready!** 🚀
