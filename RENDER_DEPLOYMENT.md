# 🚀 Deploy to Render.com - Step by Step

**Time:** 5 minutes  
**Cost:** Free (with cold start) or $7/month (always-on)  
**Difficulty:** ⭐ Very Easy

---

## Step 1: Sign Up (1 minute)

1. Go to: **https://render.com**
2. Click **"Get Started"**
3. Sign up with **GitHub** (easiest)
4. Authorize Render to access your GitHub

---

## Step 2: Create Web Service (2 minutes)

1. Click **"New +"** button (top right)
2. Select **"Web Service"**
3. Click **"Connect account"** if needed
4. Find your repo: **"EXcel_Invoice_Automation"**
5. Click **"Connect"**

---

## Step 3: Configure Service (2 minutes)

### Basic Settings:

- **Name:** `hilldrive-invoice` (or any name you want)
- **Region:** Choose closest to you (e.g., Singapore, Oregon)
- **Branch:** `master` or `main`
- **Root Directory:** Leave blank
- **Runtime:** `Python 3`

### Build & Deploy:

- **Build Command:**
  ```bash
  pip install -r requirements.txt
  ```

- **Start Command:**
  ```bash
  uvicorn main:app --host 0.0.0.0 --port $PORT
  ```

### Instance Type:

- **Free:** Select "Free" (has cold start after 15 min inactivity)
- **Paid:** Select "Starter" $7/month (always-on, no cold start)

---

## Step 4: Add Environment Variables (1 minute)

Scroll down to **"Environment Variables"** section.

Click **"Add Environment Variable"** and add these:

```
OCR_SPACE_API_KEY = K88999613688957
OCR_SPACE_API_URL = https://api.ocr.space/parse/image

GEMINI_API_KEY = AIzaSyCqib0TlPBYcH3qoqlQvkgWJXkXu7t0jOk
GEMINI_MODEL = gemini-1.5-flash
USE_GEMINI = false

OPENROUTER_API_KEY = your_openrouter_api_key_here
OPENROUTER_MODEL = google/gemini-2.5-flash
USE_OPENROUTER = true

API_HOST = 0.0.0.0
API_PORT = 8000
DEBUG = false

MAX_FILE_SIZE_MB = 5
ALLOWED_EXTENSIONS = jpg,jpeg,png,pdf

TEMPLATE_PATH = inn sample.xlsx
OUTPUT_DIR = generated_invoices
USE_MASTER_FILE = false
MASTER_FILE_PATH = generated_invoices/all_invoices.xlsx

CORS_ORIGINS = *
```

**Note:** Set `DEBUG = false` for production!

---

## Step 5: Deploy! (1 minute)

1. Click **"Create Web Service"** button at bottom
2. Wait for deployment (3-5 minutes)
3. Watch the logs - you'll see:
   - Installing dependencies
   - Starting server
   - "Live" status

---

## Step 6: Test Your App (1 minute)

Your app will be live at:
```
https://hilldrive-invoice.onrender.com
```

(Replace `hilldrive-invoice` with your chosen name)

### Test URLs:

1. **Homepage:**
   ```
   https://hilldrive-invoice.onrender.com
   ```

2. **Health Check:**
   ```
   https://hilldrive-invoice.onrender.com/health
   ```

3. **API Docs:**
   ```
   https://hilldrive-invoice.onrender.com/docs
   ```

---

## ✅ You're Live!

Your invoice system is now:
- ✅ Deployed on Render
- ✅ Accessible from anywhere
- ✅ Auto-updates from GitHub
- ✅ Free SSL certificate (HTTPS)
- ✅ Professional URL

---

## 🔄 Auto-Deploy from GitHub

Every time you push to GitHub, Render automatically deploys!

```bash
# On your local computer
git add .
git commit -m "Update invoice system"
git push

# Render automatically deploys the changes!
```

---

## 📊 Monitor Your App

### View Logs:

1. Go to Render dashboard
2. Click your service
3. Click **"Logs"** tab
4. See real-time logs

### View Metrics:

1. Click **"Metrics"** tab
2. See:
   - CPU usage
   - Memory usage
   - Request count
   - Response times

---

## 🔧 Common Issues & Fixes

### Issue 1: Build Failed

**Error:** `ModuleNotFoundError`

**Fix:** Check `requirements.txt` has all packages:
```bash
fastapi
uvicorn
python-dotenv
pydantic
pydantic-settings
openpyxl
pillow
requests
python-multipart
google-generativeai
asgiref
```

### Issue 2: App Not Starting

**Error:** `Application startup failed`

**Fix:** Check environment variables are set correctly

### Issue 3: 502 Bad Gateway

**Fix:** 
- Check Start Command is correct
- Check PORT is `$PORT` (not hardcoded)
- View logs for errors

---

## 💰 Pricing

### Free Tier:
- ✅ 750 hours/month
- ✅ 512 MB RAM
- ✅ 100 GB bandwidth
- ⚠️ Spins down after 15 min inactivity (cold start ~30 sec)

### Starter ($7/month):
- ✅ Always-on (no cold start)
- ✅ 512 MB RAM
- ✅ Unlimited bandwidth
- ✅ Worth it for production!

### Pro ($25/month):
- ✅ 2 GB RAM
- ✅ Priority support
- ✅ More resources

---

## 🎯 Upgrade to Always-On (No Cold Start)

1. Go to your service dashboard
2. Click **"Settings"**
3. Scroll to **"Instance Type"**
4. Select **"Starter"** ($7/month)
5. Click **"Save Changes"**

Your app will now be always-on with no cold start!

---

## 🌐 Custom Domain (Optional)

Want your own domain like `invoice.yourdomain.com`?

1. Buy domain from Namecheap, GoDaddy, etc.
2. In Render dashboard, go to **"Settings"**
3. Click **"Custom Domain"**
4. Add your domain
5. Update DNS records (Render shows you how)
6. Done! Free SSL included

---

## 🔐 Security Best Practices

1. **Never commit `.env` to GitHub** (already in `.gitignore`)
2. **Use environment variables** for all secrets
3. **Set DEBUG=false** in production
4. **Enable CORS** only for your domains
5. **Monitor logs** regularly

---

## 📱 Share with Your Team

Share this URL with your team:
```
https://hilldrive-invoice.onrender.com
```

They can:
- Upload images for OCR
- Create invoices manually
- Download generated invoices
- View all invoices

---

## 🆘 Need Help?

- **Render Docs:** https://render.com/docs
- **Render Community:** https://community.render.com
- **Support:** support@render.com

---

## 🎉 Success!

Your invoice automation system is now live on Render!

**Next Steps:**
1. Test invoice creation
2. Setup Google Drive (optional)
3. Share URL with team
4. Monitor usage
5. Upgrade to Starter when ready

---

**Your app is live and ready to use! 🚀**
