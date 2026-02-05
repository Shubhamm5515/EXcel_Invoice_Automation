# 🚀 Render.com + Keep-Alive Bot = FREE 24/7 Uptime

Deploy to Render free tier + use a bot to ping your app every 10 minutes = No downtime!

---

## Part 1: Deploy to Render (5 minutes)

### Step 1: Push to GitHub (if not done)

Your code is already on GitHub: `https://github.com/Shubhamm5515/EXcel_Invoice_Automation`

### Step 2: Sign Up on Render

1. Go to: **https://render.com**
2. Click **"Get Started"**
3. Sign up with **GitHub**
4. Authorize Render to access your repos

### Step 3: Create Web Service

1. Click **"New +"** (top right)
2. Select **"Web Service"**
3. Click **"Connect account"** if needed
4. Find and select: **`EXcel_Invoice_Automation`**
5. Click **"Connect"**

### Step 4: Configure Service

Fill in these settings:

**Basic Settings:**
- **Name:** `hilldrive-invoice` (or any name you like)
- **Region:** `Oregon (US West)` (or closest to you)
- **Branch:** `master` (or `main`)
- **Root Directory:** (leave blank)
- **Environment:** `Python 3`
- **Build Command:** 
  ```
  pip install -r requirements.txt
  ```
- **Start Command:**
  ```
  uvicorn main:app --host 0.0.0.0 --port $PORT
  ```

**Instance Type:**
- Select: **Free** (0.1 CPU, 512 MB RAM)

### Step 5: Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**

Add these one by one:

```
OCR_SPACE_API_KEY = K88999613688957
OCR_SPACE_API_URL = https://api.ocr.space/parse/image
GEMINI_API_KEY = AIzaSyCqib0TlPBYcH3qoqlQvkgWJXkXu7t0jOk
GEMINI_MODEL = gemini-1.5-flash
USE_GEMINI = false
OPENROUTER_API_KEY = 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
OPENROUTER_MODEL = google/gemini-2.5-flash
USE_OPENROUTER = true
API_HOST = 0.0.0.0
API_PORT = 8000
DEBUG = True
MAX_FILE_SIZE_MB = 5
ALLOWED_EXTENSIONS = jpg,jpeg,png,pdf
TEMPLATE_PATH = inn sample.xlsx
OUTPUT_DIR = generated_invoices
USE_MASTER_FILE = false
MASTER_FILE_PATH = generated_invoices/all_invoices.xlsx
CORS_ORIGINS = http://localhost:3000,http://localhost:8080
```

### Step 6: Deploy

1. Click **"Create Web Service"**
2. Wait 5-10 minutes for deployment
3. Watch the logs for any errors
4. Once deployed, you'll get a URL like: `https://hilldrive-invoice.onrender.com`

### Step 7: Test Your App

Open: `https://hilldrive-invoice.onrender.com/health`

Should return:
```json
{"status":"healthy","version":"1.0.0",...}
```

---

## Part 2: Keep-Alive Bot (Prevent Cold Start)

Render free tier spins down after 15 minutes of inactivity. We'll create a bot to ping it every 10 minutes.

### Option A: UptimeRobot (Easiest - Recommended)

**Free monitoring service that pings your app every 5 minutes**

1. **Go to:** https://uptimerobot.com
2. **Sign up** (free account)
3. Click **"Add New Monitor"**
4. **Configure:**
   - Monitor Type: `HTTP(s)`
   - Friendly Name: `Hill Drive Invoice`
   - URL: `https://hilldrive-invoice.onrender.com/health`
   - Monitoring Interval: `5 minutes`
5. Click **"Create Monitor"**

**Done!** UptimeRobot will ping your app every 5 minutes, keeping it awake 24/7.

**Bonus:** You'll get email alerts if your app goes down!

---

### Option B: Cron-Job.org (Alternative)

1. **Go to:** https://cron-job.org
2. **Sign up** (free)
3. Click **"Create cronjob"**
4. **Configure:**
   - Title: `Keep Invoice App Alive`
   - URL: `https://hilldrive-invoice.onrender.com/health`
   - Schedule: `Every 10 minutes`
5. Click **"Create"**

---

### Option C: GitHub Actions (Free, Automated)

Create a GitHub Action that pings your app every 10 minutes.

**Create file:** `.github/workflows/keepalive.yml`

```yaml
name: Keep 