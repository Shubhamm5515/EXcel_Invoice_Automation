# 🔍 Debug MEGA Upload

## Changes Made

Added debug logging to track the upload process:

### What You'll See:

When you create an invoice, the console will show:

```
🔍 Checking cloud upload... MEGA connected: True
📤 Calling MEGA upload for: generated_invoices/HD-20260205-abc123.xlsx
🔄 MEGA upload called for: generated_invoices/HD-20260205-abc123.xlsx
📤 Starting MEGA upload...
📁 Creating folder structure: /Hill Drive Invoices/2026/Feb 2026/
⬆️  Uploading HD-20260205-abc123.xlsx to MEGA...
✅ Uploaded to MEGA: HD-20260205-abc123.xlsx
   Folder: Feb 2026
   Link: https://mega.nz/...
```

---

## 🎯 Test Steps:

1. **Stop the current server** (Ctrl+C)

2. **Restart server:**
   ```bash
   python main.py
   ```

3. **Create a test invoice:**
   - Open: http://localhost:8000
   - Type in "Additional Details":
     ```
     Name: Debug Test
     Mobile: 9999888877
     Vehicle: Swift
     Rent: 3000
     Duration: 1 day
     ```
   - Click "Generate Invoice"

4. **Watch the console** - you should see all the debug messages

5. **Check for errors:**
   - If upload fails, you'll see the error message
   - If it succeeds, you'll see the MEGA link

---

## 🚨 Possible Issues:

### If you see: "MEGA connected: False"
- MEGA credentials not loaded properly
- Check `.env` file has correct email/password

### If you see: "File not found"
- Invoice wasn't created locally
- Check `generated_invoices/` folder

### If you see: "MEGA upload failed: [error]"
- Network issue
- MEGA API issue
- Folder creation failed

---

## 📝 What to Share:

Copy the **entire console output** after creating an invoice, including:
- All debug messages (🔍 📤 🔄 📁 ⬆️)
- Any error messages
- The final result (✅ or ⚠️)

This will help identify exactly where the issue is!

---

**Ready to test!** Restart the server and create an invoice. 🚀
