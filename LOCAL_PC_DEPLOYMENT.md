# 💻 Deploy on Your Windows PC - Step by Step

**Time:** 10 minutes  
**Cost:** $0 (completely free!)  
**Difficulty:** ⭐⭐ Medium  
**No Cold Start!** ✅

---

## Why Deploy Locally?

- ✅ **Completely free** (no monthly costs)
- ✅ **No cold start** (always instant)
- ✅ **Full control** over everything
- ✅ **Unlimited resources** (your PC's power)
- ✅ **Private** (data stays on your PC)

**Requirements:**
- Windows PC that stays on 24/7
- Internet connection
- Your project already working locally

---

## Option 1: Local Network Only (Easiest)

Use this if you only need access from your local network (home/office).

### Step 1: Start Your App

1. Open **Command Prompt** in your project folder
2. Run:
   ```cmd
   py -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload
   ```

### Step 2: Find Your Local IP

1. Open Command Prompt
2. Run:
   ```cmd
   ipconfig
   ```
3. Look for **"IPv4 Address"** (e.g., `192.168.1.100`)

### Step 3: Access from Any Device

On any device in your network, open:
```
http://192.168.1.100:8001
```

**Done!** Anyone on your WiFi can use the app.

---

## Option 2: Public Internet Access (Using ngrok)

Use this to make your app accessible from anywhere on the internet.

### Step 1: Install ngrok

1. **Download ngrok:**
   - Go to: https://ngrok.com/download
   - Download Windows version
   - Extract `ngrok.exe` to your project folder

2. **Sign up for free account:**
   - Go to: https://dashboard.ngrok.com/signup
   - Sign up (free)

3. **Get your auth token:**
   - Go to: https://dashboard.ngrok.com/get-started/your-authtoken
   - Copy your token

4. **Configure ngrok:**
   ```cmd
   ngrok config add-authtoken YOUR_TOKEN_HERE
   ```

### Step 2: Start Your App

Open Command Prompt in project folder:
```cmd
py -m uvicorn main:app --host 0.0.0.0 --port 8001
```

Keep this window open!

### Step 3: Start ngrok Tunnel

Open **another** Command Prompt:
```cmd
ngrok http 8001
```

You'll see:
```
Forwarding  https://abc123.ngrok.io -> http://localhost:8001
```

### Step 4: Share the URL

Copy the `https://abc123.ngrok.io` URL and share it!

Anyone can access your app at:
```
https://abc123.ngrok.io
```

**Note:** Free ngrok URLs change every time you restart. Paid plan ($8/mo) gives you a permanent URL.

---

## Option 3: Auto-Start on Windows Boot

Make your app start automatically when Windows starts.

### Step 1: Create Startup Script

Create `start_invoice_server.bat` in your project folder:

```batch
@echo off
echo Starting Hill Drive Invoice Server...

REM Change to project directory
cd /d C:\Users\ASUS\Desktop\Invoice

REM Start the FastAPI server
start "Invoice API Server" py -m uvicorn main:app --host 0.0.0.0 --port 8001

REM Wait 5 seconds for server to start
timeout /t 5 /nobreak

REM Start ngrok tunnel (optional - for public access)
start "Ngrok Tunnel" ngrok http 8001

echo.
echo ========================================
echo Invoice Server Started!
echo ========================================
echo.
echo Local Access: http://localhost:8001
echo Network Access: http://YOUR_IP:8001
echo.
echo Check ngrok window for public URL
echo.
pause
```

**Important:** Change `C:\Users\ASUS\Desktop\Invoice` to your actual project path!

### Step 2: Add to Windows Startup

1. Press `Win + R`
2. Type: `shell:startup`
3. Press Enter
4. Copy `start_invoice_server.bat` to this folder

Now your server starts automatically when Windows boots!

---

## Option 4: Run as Windows Service (Advanced)

Make your app run as a background Windows service.

### Step 1: Install NSSM

1. Download NSSM: https://nssm.cc/download
2. Extract to `C:\nssm`

### Step 2: Create Service

Open Command Prompt as Administrator:

```cmd
cd C:\nssm\win64
nssm install HillDriveInvoice
```

In the GUI that opens:
- **Path:** `C:\Users\ASUS\AppData\Local\Programs\Python\Python312\python.exe`
- **Startup directory:** `C:\Users\ASUS\Desktop\Invoice`
- **Arguments:** `-m uvicorn main:app --host 0.0.0.0 --port 8001`

Click **"Install service"**

### Step 3: Start Service

```cmd
nssm start HillDriveInvoice
```

Your app now runs as a Windows service!

**Manage service:**
```cmd
nssm stop HillDriveInvoice    # Stop
nssm restart HillDriveInvoice # Restart
nssm remove HillDriveInvoice  # Remove
```

---

## 🔒 Port Forwarding (For Public Access Without ngrok)

If you want a permanent public URL without ngrok:

### Step 1: Configure Router

1. Open router admin panel (usually `192.168.1.1`)
2. Find **"Port Forwarding"** section
3. Add new rule:
   - **External Port:** 8001
   - **Internal Port:** 8001
   - **Internal IP:** Your PC's IP (e.g., `192.168.1.100`)
   - **Protocol:** TCP

### Step 2: Find Your Public IP

Go to: https://whatismyipaddress.com

Copy your public IP (e.g., `203.45.67.89`)

### Step 3: Access from Internet

Anyone can access your app at:
```
http://203.45.67.89:8001
```

**Security Warning:** This exposes your PC to the internet. Use with caution!

---

## 🔐 Security Best Practices

### 1. Use HTTPS (with ngrok)

ngrok automatically provides HTTPS. Always use the `https://` URL, not `http://`.

### 2. Add Authentication

Add basic auth to your FastAPI app:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != "admin" or credentials.password != "your_password":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    return credentials

# Protect routes
@app.get("/api/invoice/list", dependencies=[Depends(verify_credentials)])
async def list_invoices():
    ...
```

### 3. Firewall Rules

Add Windows Firewall rule:
```cmd
netsh advfirewall firewall add rule name="Invoice API" dir=in action=allow protocol=TCP localport=8001
```

### 4. Keep PC Secure

- ✅ Install antivirus
- ✅ Keep Windows updated
- ✅ Use strong passwords
- ✅ Enable Windows Defender

---

## 📊 Monitor Your Server

### View Logs

Logs appear in the Command Prompt window where you started uvicorn.

### Check if Server is Running

```cmd
netstat -ano | findstr :8001
```

### Restart Server

1. Close Command Prompt window
2. Run start command again

---

## 💡 Tips & Tricks

### 1. Keep PC Awake

Prevent PC from sleeping:
1. Settings → System → Power & Sleep
2. Set "Sleep" to "Never"

### 2. Handle Power Outages

Use a UPS (Uninterruptible Power Supply) to keep PC running during power cuts.

### 3. Remote Access

Use TeamViewer or Chrome Remote Desktop to access your PC remotely.

### 4. Backup Invoices

Regularly backup the `generated_invoices` folder to:
- External hard drive
- Google Drive (already implemented!)
- Cloud storage

---

## 🔧 Troubleshooting

### Issue 1: Port Already in Use

**Error:** `Address already in use`

**Fix:**
```cmd
netstat -ano | findstr :8001
taskkill /PID <PID_NUMBER> /F
```

### Issue 2: Can't Access from Other Devices

**Fix:**
1. Check Windows Firewall
2. Make sure you're using `0.0.0.0` not `127.0.0.1`
3. Check if PC and device are on same network

### Issue 3: ngrok Not Working

**Fix:**
1. Check auth token is configured
2. Make sure server is running first
3. Try different port

---

## 💰 Cost Comparison

### Your PC (24/7):
- **Electricity:** ~$5-10/month (depends on PC)
- **Internet:** Already paying
- **Total:** ~$5-10/month

### ngrok Paid (Optional):
- **Free:** Random URL, 40 connections/min
- **Paid ($8/mo):** Permanent URL, unlimited connections

### Total Cost:
- **Without ngrok:** $5-10/month (electricity only)
- **With ngrok:** $13-18/month

Still cheaper than most cloud hosting!

---

## 🎯 When to Use Local Deployment

**Good for:**
- ✅ Small business with 24/7 PC
- ✅ Testing before cloud deployment
- ✅ Complete control needed
- ✅ Budget constraints
- ✅ Data privacy concerns

**Not good for:**
- ❌ No 24/7 PC available
- ❌ Unreliable internet
- ❌ High traffic expected
- ❌ Need professional hosting

---

## 🆘 Need Help?

- **ngrok Docs:** https://ngrok.com/docs
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **NSSM Docs:** https://nssm.cc/usage

---

## 🎉 Success!

Your invoice system is now running on your PC!

**Next Steps:**
1. Test from different devices
2. Share URL with team
3. Setup automatic backups
4. Monitor server regularly
5. Consider cloud hosting for production

---

**Your app is running locally and accessible! 💻✨**
