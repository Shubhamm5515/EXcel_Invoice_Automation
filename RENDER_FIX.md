# 🔧 Fix Render Deployment Error

The error you're seeing is because Render is using Python 3.13, which has compatibility issues with some packages.

---

## ✅ Quick Fix (2 Steps)

### Step 1: Push New Files to GitHub

I've created 2 new files that fix the issue:

1. **runtime.txt** - Forces Python 3.10
2. **render.yaml** - Proper Render configuration

**Push to GitHub:**

```bash
git add runtime.txt render.yaml requirements.txt
git commit -m "Fix Render deployment - use Python 3.10"
git push
```

### Step 2: Redeploy on Render

Render will automatically detect the changes and redeploy with Python 3.10.

**Or manually trigger:**
1. Go to Render dashboard
2. Click your service
3. Click **"Manual Deploy"** → **"Deploy latest commit"**

---

## 🎯 What Was Fixed?

### 1. runtime.txt
Forces Render to use Python 3.10.13 instead of 3.13:
```
python-3.10.13
```

### 2. requirements.txt
Added missing packages:
- `google-generativeai==0.3.1` (for Gemini)
- `asgiref==3.7.2` (for ASGI/WSGI compatibility)

### 3. render.yaml
Proper Render configuration with:
- Correct build command
- Correct start command
- Python version specification
- Environment variables template

---

## 🚀 Alternative: Manual Configuration

If you prefer to configure manually in Render dashboard:

### 1. Set Python Version

In Render dashboard:
1. Go to **"Environment"** tab
2. Add environment variable:
   ```
   PYTHON_VERSION = 3.10.13
   ```

### 2. Update Build Command

In **"Settings"** tab:
```bash
pip install --upgrade pip && pip install -r requirements.txt
```

### 3. Update Start Command

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

## 🔍 Verify Deployment

After redeployment, check:

1. **Build logs** should show:
   ```
   Using Python version 3.10.13
   ```

2. **Health check** should work:
   ```
   https://your-app.onrender.com/health
   ```

3. **Homepage** should load:
   ```
   https://your-app.onrender.com
   ```

---

## ⚠️ Common Issues

### Issue 1: Still Using Python 3.13

**Fix:** Make sure `runtime.txt` is in the root directory and pushed to GitHub.

### Issue 2: Build Still Failing

**Fix:** Check build logs for specific package errors. May need to update package versions.

### Issue 3: Environment Variables Missing

**Fix:** Add them manually in Render dashboard under "Environment" tab.

---

## 📋 Environment Variables to Add

If using manual configuration, add these in Render dashboard:

```
OCR_SPACE_API_KEY=K88999613688957
OCR_SPACE_API_URL=https://api.ocr.space/parse/image

GEMINI_API_KEY=AIzaSyCqib0TlPBYcH3qoqlQvkgWJXkXu7t0jOk
GEMINI_MODEL=gemini-1.5-flash
USE_GEMINI=false

OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL=google/gemini-2.5-flash
USE_OPENROUTER=true

API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false

MAX_FILE_SIZE_MB=5
ALLOWED_EXTENSIONS=jpg,jpeg,png,pdf

TEMPLATE_PATH=inn sample.xlsx
OUTPUT_DIR=generated_invoices
USE_MASTER_FILE=false
MASTER_FILE_PATH=generated_invoices/all_invoices.xlsx

CORS_ORIGINS=*
```

---

## ✅ Success Checklist

- [ ] `runtime.txt` created and pushed
- [ ] `render.yaml` created and pushed
- [ ] `requirements.txt` updated and pushed
- [ ] Changes pushed to GitHub
- [ ] Render redeployed automatically
- [ ] Build succeeded (check logs)
- [ ] Health check works
- [ ] App loads successfully

---

## 🎉 Done!

Your app should now deploy successfully on Render with Python 3.10!

**Next steps:**
1. Test your app
2. Setup UptimeRobot (to prevent downtime)
3. Share URL with team

---

**Need help? Check the build logs in Render dashboard for specific errors.**
