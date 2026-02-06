# 🚀 Deployment Quick Start Guide

Choose your deployment method and get started in minutes!

---

## 🎯 Which Option is Best for You?

### ⭐ **Render.com** - RECOMMENDED
**Best for:** Production use, professional setup  
**Cost:** Free (with cold start) or $7/month (always-on)  
**Time:** 5 minutes  
**Difficulty:** ⭐ Very Easy

👉 **[Full Guide: RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)**

**Quick Start:**
1. Go to https://render.com
2. Sign up with GitHub
3. New → Web Service → Select your repo
4. Build: `pip install -r requirements.txt`
5. Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables from `.env`
7. Deploy!

---

### 🚂 **Railway.app** - GREAT FREE OPTION
**Best for:** Starting out, no cold start needed  
**Cost:** $5 credit/month (~500 hours)  
**Time:** 5 minutes  
**Difficulty:** ⭐ Very Easy

👉 **[Full Guide: RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md)**

**Quick Start:**
1. Go to https://railway.app
2. Sign in with GitHub
3. New Project → Deploy from GitHub
4. Select your repo
5. Add environment variables
6. Generate domain
7. Done!

---

### 💻 **Your Windows PC** - COMPLETELY FREE
**Best for:** Testing, budget constraints, full control  
**Cost:** $0 (just electricity)  
**Time:** 10 minutes  
**Difficulty:** ⭐⭐ Medium

👉 **[Full Guide: LOCAL_PC_DEPLOYMENT.md](LOCAL_PC_DEPLOYMENT.md)**

**Quick Start:**
1. Install ngrok from https://ngrok.com
2. Run: `py -m uvicorn main:app --host 0.0.0.0 --port 8001`
3. Run: `ngrok http 8001`
4. Share the ngrok URL!

---

## 📊 Comparison Table

| Feature | Render | Railway | Your PC |
|---------|--------|---------|---------|
| **Cost** | Free/$7 | $5 credit | $0 |
| **Cold Start** | Yes (free) | No | No |
| **Setup Time** | 5 min | 5 min | 10 min |
| **Difficulty** | ⭐ Easy | ⭐ Easy | ⭐⭐ Medium |
| **Auto-Deploy** | ✅ Yes | ✅ Yes | ❌ No |
| **Custom Domain** | ✅ Yes | ✅ Yes | ⚠️ Complex |
| **SSL/HTTPS** | ✅ Free | ✅ Free | ⚠️ Via ngrok |
| **Uptime** | 99.9% | 99.9% | Depends on PC |
| **Scalability** | ✅ Auto | ✅ Auto | ❌ Limited |
| **Best For** | Production | Starting | Testing |

---

## 🎯 My Recommendation

### For Production (Business Use):
**Choose Render.com ($7/month)**
- Always-on, no cold start
- Professional URL
- Auto-deploys from GitHub
- Best value for money

### For Testing/Starting:
**Choose Railway.app (Free)**
- $5 credit/month
- No cold start
- Easy to upgrade later

### For Development:
**Choose Your PC (Free)**
- Test locally first
- Then deploy to cloud

---

## 🚀 Fastest Path to Production

### Step 1: Test Locally (10 minutes)
```cmd
py -m uvicorn main:app --host 0.0.0.0 --port 8001
```
Open: http://localhost:8001

### Step 2: Deploy to Railway (5 minutes)
- Free $5 credit
- No cold start
- Test with real users

### Step 3: Upgrade to Render (5 minutes)
- When ready for production
- $7/month for always-on
- Professional setup

---

## 📋 Pre-Deployment Checklist

Before deploying, make sure:

- [ ] App works locally
- [ ] All files committed to GitHub
- [ ] `.env` file NOT in GitHub (check `.gitignore`)
- [ ] `requirements.txt` is complete
- [ ] Environment variables ready to copy
- [ ] Template file (`inn sample.xlsx`) in repo
- [ ] `generated_invoices` folder exists (or created in code)

---

## 🔑 Environment Variables to Add

Copy these to your deployment platform:

```env
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

**Important:** Set `DEBUG=false` for production!

---

## 🧪 Testing Your Deployment

After deployment, test these URLs:

### 1. Health Check
```
https://your-app-url.com/health
```
Should return:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "ocr_service": "OCR.space (Free Tier)",
  "ai_service": "OpenRouter AI"
}
```

### 2. Homepage
```
https://your-app-url.com
```
Should show your web interface

### 3. API Documentation
```
https://your-app-url.com/docs
```
Should show FastAPI Swagger UI

### 4. Create Test Invoice
Use the web interface to:
1. Upload an OCR image
2. Fill in booking details
3. Generate invoice
4. Download and verify

---

## 🔧 Common Deployment Issues

### Issue 1: Build Failed
**Error:** `ModuleNotFoundError`

**Fix:** Check `requirements.txt` has all packages

### Issue 2: App Won't Start
**Error:** `Application startup failed`

**Fix:** Check environment variables are set

### Issue 3: 502 Bad Gateway
**Fix:** 
- Check start command uses `$PORT`
- View logs for errors

### Issue 4: Template Not Found
**Error:** `FileNotFoundError: inn sample.xlsx`

**Fix:** Make sure template file is in GitHub repo

---

## 📱 After Deployment

### Share with Your Team

Send them:
```
Invoice System: https://your-app-url.com

Features:
- Upload images for OCR
- Create invoices manually
- Download invoices
- View all invoices

Login: (if you added authentication)
Username: admin
Password: your_password
```

### Monitor Usage

Check your deployment platform dashboard for:
- Request count
- Error rate
- Response times
- Resource usage

### Setup Google Drive (Optional)

Follow `GOOGLE_DRIVE_SETUP.md` to:
- Auto-upload invoices to Google Drive
- Organize by month
- Download entire month at once

---

## 💰 Cost Breakdown

### Option 1: Render (Recommended)
- **Free tier:** $0/month (with cold start)
- **Starter:** $7/month (always-on)
- **Pro:** $25/month (more resources)

### Option 2: Railway
- **Free:** $5 credit/month (~500 hours)
- **After credit:** ~$0.01/hour (~$7-10/month for 24/7)

### Option 3: Your PC
- **Electricity:** ~$5-10/month
- **ngrok (optional):** $8/month for permanent URL
- **Total:** $5-18/month

### Recommendation:
Start with Railway (free), then upgrade to Render Starter ($7/month) for production.

---

## 🎓 Learning Path

### Week 1: Local Development
- Run locally
- Test all features
- Fix any bugs

### Week 2: Test Deployment
- Deploy to Railway (free)
- Share with 2-3 users
- Gather feedback

### Week 3: Production
- Deploy to Render ($7/month)
- Share with all users
- Monitor usage

### Week 4: Optimize
- Setup Google Drive
- Add custom domain
- Improve features

---

## 🆘 Need Help?

### Documentation:
- **Render:** https://render.com/docs
- **Railway:** https://docs.railway.app
- **FastAPI:** https://fastapi.tiangolo.com

### Community:
- **Render Community:** https://community.render.com
- **Railway Discord:** https://discord.gg/railway
- **FastAPI Discord:** https://discord.gg/fastapi

### Support:
- **Render:** support@render.com
- **Railway:** help@railway.app

---

## 🎉 Ready to Deploy?

Choose your platform and follow the detailed guide:

1. **[Render Deployment Guide](RENDER_DEPLOYMENT.md)** ⭐ Recommended
2. **[Railway Deployment Guide](RAILWAY_DEPLOYMENT.md)** 🚂 Great free option
3. **[Local PC Deployment Guide](LOCAL_PC_DEPLOYMENT.md)** 💻 Completely free

---

## 📞 What's Next?

After successful deployment:

1. ✅ Test all features
2. ✅ Share URL with team
3. ✅ Setup Google Drive (optional)
4. ✅ Add custom domain (optional)
5. ✅ Monitor usage
6. ✅ Gather feedback
7. ✅ Improve features

---

**Your invoice automation system is ready to go live! 🚀**

Pick a platform and start deploying now!
