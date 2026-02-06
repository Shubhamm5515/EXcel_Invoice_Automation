# 🚂 Deploy to Railway.app - Step by Step

**Time:** 5 minutes  
**Cost:** $5 free credit/month (~500 hours)  
**Difficulty:** ⭐ Very Easy  
**No Cold Start!** ✅

---

## Step 1: Sign Up (1 minute)

1. Go to: **https://railway.app**
2. Click **"Login"**
3. Sign in with **GitHub**
4. Authorize Railway to access your repos

---

## Step 2: Create New Project (1 minute)

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Find: **"EXcel_Invoice_Automation"**
4. Click on it

Railway will automatically:
- ✅ Detect it's a Python project
- ✅ Install dependencies from `requirements.txt`
- ✅ Start your app

---

## Step 3: Configure Start Command (1 minute)

Railway might not detect the correct start command.

1. Click on your service
2. Go to **"Settings"** tab
3. Scroll to **"Deploy"** section
4. Set **"Start Command":**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
5. Click **"Save"**

---

## Step 4: Add Environment Variables (2 minutes)

1. Click **"Variables"** tab
2. Click **"New Variable"**
3. Add these one by one:

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

**Tip:** You can also use "Raw Editor" to paste all at once!

---

## Step 5: Generate Public URL (1 minute)

1. Go to **"Settings"** tab
2. Scroll to **"Networking"** section
3. Click **"Generate Domain"**
4. Railway creates a public URL like:
   ```
   https://your-app.up.railway.app
   ```

---

## Step 6: Deploy! (Automatic)

Railway automatically deploys when you:
- Add environment variables
- Change settings
- Push to GitHub

Watch the **"Deployments"** tab to see progress.

---

## Step 7: Test Your App (1 minute)

Your app is live at:
```
https://your-app.up.railway.app
```

### Test URLs:

1. **Homepage:**
   ```
   https://your-app.up.railway.app
   ```

2. **Health Check:**
   ```
   https://your-app.up.railway.app/health
   ```

3. **API Docs:**
   ```
   https://your-app.up.railway.app/docs
   ```

---

## ✅ You're Live!

Your invoice system is now:
- ✅ Deployed on Railway
- ✅ **No cold start** (even on free tier!)
- ✅ Auto-updates from GitHub
- ✅ Free SSL certificate
- ✅ Fast performance

---

## 🔄 Auto-Deploy from GitHub

Every push to GitHub triggers automatic deployment:

```bash
# On your local computer
git add .
git commit -m "Update invoice system"
git push

# Railway automatically deploys!
```

---

## 📊 Monitor Your App

### View Logs:

1. Click **"Deployments"** tab
2. Click on latest deployment
3. Click **"View Logs"**
4. See real-time logs

### View Metrics:

1. Click **"Metrics"** tab
2. See:
   - CPU usage
   - Memory usage
   - Network traffic
   - Deployment history

---

## 💰 Pricing & Credits

### Free Trial:
- ✅ $5 credit/month
- ✅ ~500 hours of runtime
- ✅ No cold start
- ✅ 512 MB RAM
- ✅ 1 GB disk

### Usage Calculation:
```
$5 credit = 500 hours/month
= ~16 hours/day
= Perfect for small business!
```

### After Free Credit:
- Pay only for what you use
- ~$0.01/hour
- ~$7-10/month for 24/7 operation

### Add Payment Method:
1. Click your profile (top right)
2. Go to **"Account Settings"**
3. Click **"Billing"**
4. Add credit card (required after trial)

---

## 🔧 Common Issues & Fixes

### Issue 1: Build Failed

**Error:** `ModuleNotFoundError`

**Fix:** 
1. Check `requirements.txt` exists
2. Make sure all packages are listed
3. Redeploy

### Issue 2: App Crashes on Start

**Error:** `Application startup failed`

**Fix:**
1. Check environment variables
2. View logs for specific error
3. Make sure start command is correct

### Issue 3: Port Binding Error

**Error:** `Port already in use`

**Fix:** Use `$PORT` environment variable:
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

## 🎯 Custom Domain (Optional)

Want `invoice.yourdomain.com`?

1. Go to **"Settings"** tab
2. Scroll to **"Networking"**
3. Click **"Custom Domain"**
4. Enter your domain
5. Update DNS records (Railway shows you how)
6. Free SSL included!

---

## 📱 Share with Team

Share your Railway URL:
```
https://your-app.up.railway.app
```

Your team can:
- Create invoices
- Upload OCR images
- Download invoices
- View invoice list

---

## 🔐 Security Tips

1. **Never commit secrets** to GitHub
2. **Use environment variables** for all API keys
3. **Set DEBUG=false** in production
4. **Monitor logs** regularly
5. **Limit CORS** to your domains only

---

## 📈 Scaling

Railway automatically scales based on usage:
- More traffic = More resources
- Less traffic = Less cost
- No configuration needed!

---

## 🆘 Need Help?

- **Railway Docs:** https://docs.railway.app
- **Discord Community:** https://discord.gg/railway
- **Support:** help@railway.app

---

## 🎉 Success!

Your invoice system is live on Railway with:
- ✅ No cold start
- ✅ Fast performance
- ✅ Auto-deploys
- ✅ $5 free credit/month

**Next Steps:**
1. Test invoice creation
2. Monitor usage in dashboard
3. Add payment method before credit runs out
4. Setup Google Drive (optional)
5. Share URL with team

---

**Your app is live and blazing fast! 🚂💨**
