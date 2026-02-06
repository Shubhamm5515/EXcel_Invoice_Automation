# 🚀 Deploy Your Updated Frontend (with 3D Car Viewer)

## What's New in Your Frontend

✅ **3D Car Viewer** - Interactive Three.js model  
✅ **CSS 3D Car** - Animated car in header  
✅ **Cleaner Code** - Removed unused storage services  
✅ **Simplified Backend** - Local storage only  
✅ **Better Performance** - Fewer dependencies  

---

## Deployment Options

### Option 1: Render.com (Recommended - FREE)
- ✅ Free tier available
- ✅ Auto-deploy from GitHub
- ✅ HTTPS included
- ✅ No cold start issues
- ✅ Supports large files (3D model)

### Option 2: Railway.app (FREE)
- ✅ $5 free credit monthly
- ✅ GitHub integration
- ✅ Easy setup
- ✅ Good for development

### Option 3: PythonAnywhere (FREE)
- ✅ Always-on free tier
- ✅ No credit card needed
- ✅ Manual deployment
- ✅ Good for production

---

## 🎯 Quick Deploy to Render.com (5 Minutes)

### Step 1: Prepare Your Code

1. **Update Dockerfile for new structure:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories
RUN mkdir -p generated_invoices static/models

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run with main_new.py
CMD ["uvicorn", "main_new:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. **Update render.yaml:**

```yaml
services:
  - type: web
    name: hilldrive-invoice
    runtime: python
    plan: free
    region: singapore
    buildCommand: pip install --upgrade pip && pip install -r requirements.txt
    startCommand: uvicorn main_new:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.9
      - key: OCR_SPACE_API_KEY
        sync: false
      - key: OPENROUTER_API_KEY
        sync: false
      - key: OPENROUTER_MODEL
        value: google/gemini-2.5-flash
      - key: USE_OPENROUTER
        value: true
      - key: DEBUG
        value: false
      - key: CORS_ORIGINS
        value: "*"
```

### Step 2: Push to GitHub

```bash
# Add all changes
git add .

# Commit with message
git commit -m "Updated frontend with 3D car viewer and cleaned storage services"

# Push to GitHub
git push origin main
```

### Step 3: Deploy on Render

1. **Go to:** https://render.com
2. **Sign in** with GitHub
3. **Click:** "New +" → "Web Service"
4. **Connect** your repository: `EXcel_Invoice_Automation`
5. **Configure:**
   - Name: `hilldrive-invoice`
   - Runtime: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main_new:app --host 0.0.0.0 --port $PORT`
6. **Add Environment Variables:**
   - `OCR_SPACE_API_KEY` = `K88999613688957`
   - `OPENROUTER_API_KEY` = `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`
   - `OPENROUTER_MODEL` = `google/gemini-2.5-flash`
   - `USE_OPENROUTER` = `true`
7. **Click:** "Create Web Service"

### Step 4: Wait for Deployment (3-5 minutes)

Watch the logs. You'll see:
```
==> Building...
==> Installing dependencies...
==> Starting server...
✅ Your service is live!
```

### Step 5: Access Your App

Your URL will be:
```
https://hilldrive-invoice.onrender.com
```

Test these URLs:
- **Frontend:** https://hilldrive-invoice.onrender.com
- **3D Viewer:** https://hilldrive-invoice.onrender.com/static/car-viewer.html
- **API Docs:** https://hilldrive-invoice.onrender.com/docs
- **Health:** https://hilldrive-invoice.onrender.com/health

---

## 🚂 Alternative: Deploy to Railway.app

### Step 1: Push to GitHub (same as above)

### Step 2: Deploy on Railway

1. **Go to:** https://railway.app
2. **Sign in** with GitHub
3. **Click:** "New Project" → "Deploy from GitHub repo"
4. **Select:** `EXcel_Invoice_Automation`
5. **Add Variables:**
   - Same environment variables as Render
6. **Deploy!**

Your URL: `https://hilldrive-invoice.up.railway.app`

---

## 🐍 Alternative: Deploy to PythonAnywhere

### Step 1: Create Account

1. Go to: https://www.pythonanywhere.com
2. Sign up (free account)
3. Verify email

### Step 2: Upload Code

**Option A: Git Clone**
```bash
# In PythonAnywhere Bash console
git clone https://github.com/Shubhamm5515/EXcel_Invoice_Automation.git
cd EXcel_Invoice_Automation
```

**Option B: Upload Files**
- Use "Files" tab
- Upload zip of your project
- Extract

### Step 3: Setup Virtual Environment

```bash
# In Bash console
cd EXcel_Invoice_Automation
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 4: Configure Web App

1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Python 3.10
5. Set source code: `/home/yourusername/EXcel_Invoice_Automation`
6. Set virtualenv: `/home/yourusername/EXcel_Invoice_Automation/venv`

### Step 5: Configure WSGI File

Edit `/var/www/yourusername_pythonanywhere_com_wsgi.py`:

```python
import sys
import os

# Add your project directory
project_home = '/home/yourusername/EXcel_Invoice_Automation'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Load environment variables
from dotenv import load_dotenv
load_dotenv(os.path.join(project_home, '.env'))

# Import FastAPI app
from main_new import app as application
```

### Step 6: Setup Static Files

In Web tab, add static files mapping:
- URL: `/static/`
- Directory: `/home/yourusername/EXcel_Invoice_Automation/static/`

### Step 7: Reload & Test

Click "Reload" button

Your URL: `https://yourusername.pythonanywhere.com`

---

## ⚠️ Important: 3D Model File Size

Your `car.glb` is **57.8 MB** - this is large!

### For Render/Railway:
- ✅ Will work, but slow initial load
- Consider optimizing the model

### For PythonAnywhere Free:
- ⚠️ 512 MB disk limit total
- May need to optimize or upgrade

### Optimize Your 3D Model:

**Option 1: Use Online Tools**
- https://gltf.report/ - Analyze model
- https://products.aspose.app/3d/compress - Compress GLB
- Target: < 10 MB

**Option 2: Reduce Quality**
- Lower polygon count
- Compress textures
- Remove unnecessary details

**Option 3: Use CDN**
- Upload to GitHub releases
- Use direct URL in viewer
- Free and fast

---

## 📦 Files to Deploy

Make sure these are in your repo:

### Essential Files
- ✅ `main_new.py` - New entry point
- ✅ `config.py` - Configuration
- ✅ `requirements.txt` - Dependencies
- ✅ `.env.example` - Example environment
- ✅ `Dockerfile` - Docker config
- ✅ `render.yaml` - Render config

### App Structure
- ✅ `app/` folder - Modular code
  - `app/models/` - Data models
  - `app/services/` - Business logic
  - `app/routers/` - API endpoints

### Frontend
- ✅ `static/index.html` - Main page
- ✅ `static/style.css` - Styles
- ✅ `static/script.js` - JavaScript
- ✅ `static/car-3d.css` - CSS 3D car
- ✅ `static/car-viewer.html` - 3D viewer
- ✅ `static/models/car.glb` - 3D model

### Templates & Data
- ✅ `inn sample.xlsx` - Invoice template
- ✅ `invoice_counter.json` - Counter

---

## 🔒 Security: Environment Variables

**Never commit these to GitHub:**
- ❌ `.env` file
- ❌ API keys
- ❌ Credentials

**Add to `.gitignore`:**
```
.env
*.pyc
__pycache__/
venv/
generated_invoices/*.xlsx
!generated_invoices/.gitkeep
```

**Set on deployment platform:**
- Render: Environment Variables section
- Railway: Variables tab
- PythonAnywhere: .env file on server

---

## ✅ Post-Deployment Checklist

After deploying, test:

- [ ] Homepage loads
- [ ] 3D car in header animates
- [ ] "View 3D Car Showroom" button works
- [ ] 3D viewer loads model
- [ ] Can rotate/zoom 3D car
- [ ] Color change works
- [ ] OCR upload works
- [ ] Manual entry works
- [ ] Invoice generation works
- [ ] Download invoice works
- [ ] API docs accessible
- [ ] Health endpoint responds

---

## 🐛 Troubleshooting

### 3D Model Not Loading

**Check:**
1. File exists at `static/models/car.glb`
2. File size < 100 MB
3. Browser console for errors (F12)
4. Network tab shows 200 status

**Fix:**
- Optimize model size
- Check file permissions
- Verify static files serving

### Server Errors

**Check logs:**
- Render: Logs tab
- Railway: Deployments → Logs
- PythonAnywhere: Error log

**Common issues:**
- Missing dependencies → Update requirements.txt
- Import errors → Check file paths
- Port issues → Use $PORT variable

### Slow Loading

**Optimize:**
1. Compress 3D model
2. Enable gzip compression
3. Use CDN for large files
4. Add loading indicators

---

## 🎨 Customize After Deployment

### Change 3D Model
1. Upload new `car.glb` to `static/models/`
2. Push to GitHub
3. Auto-redeploys

### Update Colors
Edit `static/car-viewer.html`:
```javascript
scene.background = new THREE.Color(0x1a1a1a); // Dark theme
```

### Add Custom Domain
- Render: Settings → Custom Domain
- Railway: Settings → Domains
- PythonAnywhere: Web tab → Custom domain (paid)

---

## 💰 Cost Comparison

| Platform | Free Tier | Limits | Best For |
|----------|-----------|--------|----------|
| **Render** | ✅ Yes | 750 hrs/mo | Production |
| **Railway** | ✅ $5 credit | 500 hrs/mo | Development |
| **PythonAnywhere** | ✅ Yes | 512 MB disk | Small projects |

**Recommendation:** Start with Render, it's the easiest!

---

## 🚀 Quick Commands

### Push to GitHub
```bash
git add .
git commit -m "Deploy updated frontend with 3D viewer"
git push origin main
```

### Check Git Status
```bash
git status
git log --oneline -5
```

### Create .gitignore
```bash
echo ".env" >> .gitignore
echo "*.pyc" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "venv/" >> .gitignore
```

---

## 📞 Need Help?

### Platform Support
- **Render:** https://render.com/docs
- **Railway:** https://docs.railway.app
- **PythonAnywhere:** https://help.pythonanywhere.com

### Your Documentation
- `DEPLOYMENT_READY.md` - General deployment
- `PYTHONANYWHERE_COMPLETE_GUIDE.md` - PythonAnywhere details
- `YOUR_3D_CAR_IS_READY.md` - 3D viewer info

---

## 🎉 You're Ready!

Your updated frontend with the 3D car viewer is ready to deploy!

**Recommended path:**
1. Update Dockerfile (see Step 1)
2. Push to GitHub
3. Deploy on Render.com
4. Test 3D viewer
5. Share your live URL!

**Estimated time:** 10-15 minutes

Good luck! 🚀
