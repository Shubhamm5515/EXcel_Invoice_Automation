# 🚀 Deploy to Render.com - Step by Step

## Why Render.com?

✅ **Free tier** - 750 hours/month  
✅ **Easy setup** - Deploy in 5 minutes  
✅ **Auto-deploy** - Push to GitHub = Auto deploy  
✅ **HTTPS** - Free SSL certificate  
✅ **Reliable** - Good uptime  

---

## Prerequisites

1. GitHub account
2. Your code pushed to GitHub
3. Render.com account (free)

---

## Step 1: Push Code to GitHub (5 minutes)

```bash
# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Hill Drive Invoice System"

# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/hilldrive-invoice.git
git push -u origin main
```

**Important:** Add to `.gitignore`:
```
.env
google_credentials.json
__pycache__/
*.pyc
venv/
generated_invoices/*.xlsx
invoice_counter.json
```

---

## Step 2: Create Render Account (2 minutes)

1. Go to: https://render.com
2. Click "Get Started"
3. Sign up with GitHub (easiest)
4. Authorize Render to access your repos

---

## Step 3: Create New Web Service (3 minutes)

1. **Click** "New +" → "Web Service"
2. **Connect** your GitHub repository
3. **Configure:**
   - **Name:** `hilldrive-invoice-api`
   - **Region:** Singapore (or closest to you)
   - **Branch:** `main`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free

4. **Click** "Create Web Service"

---

## Step 4: Add Environment Variables (3 minutes)

In Render dashboard:

1. Go to **Environment** tab
2. Add these variables:

```
OCR_SPACE_API_KEY = K88999613688957
OPENROUTER_API_KEY = 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
OPENROUTER_MODEL = google/gemini-2.5-flash
USE_OPENROUTER = true
USE_MASTER_FILE = false
TEMPLATE_PATH = inn sample.xlsx
OUTPUT_DIR = generated_invoices
API_PORT = $PORT
```

3. **Click** "Save Changes"

---

## Step 5: Deploy! (2 minutes)

Render will automatically:
1. Clone your repo
2. Install dependencies
3. Start the server
4. Give you a URL

**Your URL:** `https://hilldrive-invoice-api.onrender.com`

---

## Step 6: Test Deployment (1 minute)

```bash
# Test health endpoint
curl https://hilldrive-invoice-api.onrender.com/health

# Should return:
# {"status":"healthy","timestamp":"...","version":"1.0.0",...}
```

Open in browser:
```
https://hilldrive-invoice-api.onrender.com
```

You should see your web interface!

---

## Step 7: Setup Google Drive (Optional)

For cloud storage:

1. Upload `google_credentials.json` as secret file in Render
2. Or use Render's disk storage (paid feature)
3. Or keep local storage only

---

## Auto-Deploy Setup

Every time you push to GitHub:
1. Render detects the push
2. Automatically rebuilds
3. Deploys new version
4. Zero downtime

```bash
# Make changes
git add .
git commit -m "Updated feature"
git push

# Render auto-deploys!
```

---

## Free Tier Limitations

⚠️ **Important:**

1. **Sleeps after 15 min** of inactivity
2. **Wakes in ~30 seconds** on first request
3. **750 hours/month** (enough for 24/7 if always active)

**Solution:** Use a free uptime monitor (like UptimeRobot) to ping every 14 minutes.

---

## Upgrade Options

If you need always-on:

**Starter Plan:** $7/month
- No sleep
- 512 MB RAM
- Always available

---

## Custom Domain (Optional)

1. Buy domain (e.g., from Namecheap)
2. In Render: Settings → Custom Domain
3. Add your domain
4. Update DNS records
5. Done! Free HTTPS included

---

## Monitoring

Render provides:
- ✅ Logs (real-time)
- ✅ Metrics (CPU, RAM)
- ✅ Deploy history
- ✅ Health checks

Access from dashboard.

---

## Troubleshooting

### Build Failed
- Check `requirements.txt` is correct
- Check Python version compatibility
- View build logs in Render

### App Not Starting
- Check start command is correct
- Check port is `$PORT` (Render provides this)
- View logs in Render

### Environment Variables Not Working
- Check spelling
- Check they're saved
- Redeploy after adding variables

---

## Alternative: Railway.app

If Render doesn't work:

1. Go to railway.app
2. Connect GitHub
3. Deploy (similar process)
4. Get $5 free credit/month

---

## Files Needed

✅ `requirements.txt` - Dependencies  
✅ `main.py` - Your app  
✅ `render.yaml` - Render config (optional)  
✅ `.gitignore` - Exclude sensitive files  

---

## Security Checklist

Before deploying:

- [ ] `.env` in `.gitignore`
- [ ] `google_credentials.json` in `.gitignore`
- [ ] API keys as environment variables
- [ ] No sensitive data in code
- [ ] CORS configured correctly

---

## Cost Summary

**Free Forever:**
- Render.com free tier
- Google Drive 15 GB
- GitHub (public repo)

**Total:** $0/month

**If you need always-on:**
- Render Starter: $7/month
- Still very affordable!

---

## Next Steps

1. ✅ Push code to GitHub
2. ✅ Create Render account
3. ✅ Deploy web service
4. ✅ Add environment variables
5. ✅ Test your live URL
6. ✅ Share with team!

**Deployment time: ~15 minutes total**

Your invoice system will be live at:
`https://hilldrive-invoice-api.onrender.com`
