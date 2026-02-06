# 🚀 Deployment Options for Invoice Automation System

Your FastAPI app can be deployed on multiple platforms. Here are the best options:

---

## 1. ⭐ Render.com (RECOMMENDED - Easiest)

**Why Choose Render:**
- ✅ Free tier available
- ✅ Zero configuration needed
- ✅ Auto-deploys from GitHub
- ✅ Always-on (no cold start on paid tier)
- ✅ Built-in HTTPS
- ✅ Easy to use

**Free Tier:**
- 750 hours/month free
- Spins down after 15 min inactivity (cold start ~30 seconds)
- 512 MB RAM

**Paid Tier ($7/month):**
- Always-on (no cold start)
- 512 MB RAM
- Worth it for production use

### Deployment Steps:

1. **Go to:** https://render.com
2. **Sign up** with GitHub
3. Click **"New +"** → **"Web Service"**
4. **Connect your GitHub repo:** `EXcel_Invoice_Automation`
5. **Configure:**
   - Name: `hilldrive-invoice`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. **Add Environment Variables** (click "Advanced"):
   ```
   OCR_SPACE_API_KEY=your_ocr_api_key_here
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   USE_OPENROUTER=true
   USE_GEMINI=false
   ```
7. Click **"Create Web Service"**
8. Wait 5 minutes for deployment
9. Your app will be live at: `https://hilldrive-invoice.onrender.com`

**Pros:**
- Easiest deployment
- Auto-updates from GitHub
- Free SSL certificate
- Good performance

**Cons:**
- Free tier has cold start (15 min inactivity)
- Need paid tier for always-on

---

## 2. 🐳 Railway.app (Great Alternative)

**Why Choose Railway:**
- ✅ $5 free credit/month
- ✅ No cold start
- ✅ Deploy from GitHub
- ✅ Very fast
- ✅ Simple interface

**Free Tier:**
- $5 credit/month (enough for ~500 hours)
- No cold start
- 512 MB RAM

### Deployment Steps:

1. **Go to:** https://railway.app
2. **Sign up** with GitHub
3. Click **"New Project"** → **"Deploy from GitHub repo"**
4. Select: `EXcel_Invoice_Automation`
5. Railway auto-detects Python
6. **Add Environment Variables:**
   - Go to Variables tab
   - Add all variables from `.env` file
7. **Generate Domain:**
   - Go to Settings → Generate Domain
8. Your app will be live at: `https://your-app.railway.app`

**Pros:**
- No cold start on free tier
- Very fast deployment
- Good free credit
- Easy to use

**Cons:**
- Free credit runs out (~500 hours/month)
- Need to add payment method after trial

---

## 3. 💻 Your Own Windows PC (24/7 Server)

**Why Choose This:**
- ✅ Completely free
- ✅ Full control
- ✅ No cold start
- ✅ Unlimited resources

**Requirements:**
- Windows PC that stays on 24/7
- Internet connection
- Port forwarding on router

### Deployment Steps:

#### Step 1: Install ngrok (for public URL)

1. **Download ngrok:** https://ngrok.com/download
2. **Sign up** for free account
3. **Extract** ngrok.exe to your project folder
4. **Get auth token** from ngrok dashboard
5. **Run in CMD:**
   ```cmd
   ngrok config add-authtoken YOUR_TOKEN
   ```

#### Step 2: Start Your App

1. **Open CMD** in your project folder
2. **Run:**
   ```cmd
   py -m uvicorn main:app --host 0.0.0.0 --port 8001
   ```

#### Step 3: Expose to Internet

1. **Open another CMD**
2. **Run:**
   ```cmd
   ngrok http 8001
   ```
3. **Copy the public URL** (e.g., `https://abc123.ngrok.io`)
4. Share this URL with your team

#### Step 4: Auto-Start on Windows Boot (Optional)

Create `start_server.bat`:
```batch
@echo off
cd C:\Users\ASUS\Desktop\Invoice
start "Invoice API" py -m uvicorn main:app --host 0.0.0.0 --port 8001
start "Ngrok Tunnel" ngrok http 8001
```

Add to Windows Startup folder:
- Press `Win + R`
- Type: `shell:startup`
- Copy `start_server.bat` there

**Pros:**
- Completely free
- Full control
- No limitations
- Fast (local network)

**Cons:**
- PC must stay on 24/7
- Uses electricity
- ngrok free tier has random URLs (changes on restart)
- Need to manage yourself

---

## 4. ☁️ Google Cloud Run (Scalable)

**Why Choose Google Cloud:**
- ✅ Free tier: 2 million requests/month
- ✅ Auto-scales
- ✅ Pay only for usage
- ✅ No cold start on paid tier

**Free Tier:**
- 2 million requests/month
- 180,000 vCPU-seconds/month
- 360,000 GiB-seconds/month

### Deployment Steps:

1. **Install Google Cloud SDK**
2. **Create Dockerfile** (already exists in your project)
3. **Deploy:**
   ```bash
   gcloud run deploy hilldrive-invoice \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```
4. Add environment variables in Cloud Run console

**Pros:**
- Generous free tier
- Auto-scales
- Google infrastructure

**Cons:**
- More complex setup
- Cold start on free tier
- Need credit card

---

## 5. 🔷 Azure App Service (Enterprise)

**Why Choose Azure:**
- ✅ Free tier available
- ✅ Microsoft infrastructure
- ✅ Good for enterprise
- ✅ Integrates with Microsoft services

**Free Tier:**
- 10 apps
- 1 GB storage
- 60 CPU minutes/day

### Deployment Steps:

1. **Install Azure CLI**
2. **Login:** `az login`
3. **Create app:**
   ```bash
   az webapp up --name hilldrive-invoice --runtime "PYTHON:3.10"
   ```
4. Configure environment variables in Azure Portal

**Pros:**
- Microsoft ecosystem
- Good for enterprise
- Free tier available

**Cons:**
- 60 min CPU limit/day on free tier
- More complex than Render

---

## 6. 🟢 Vercel (Serverless)

**Why Choose Vercel:**
- ✅ Free tier
- ✅ Deploy from GitHub
- ✅ Very fast CDN
- ✅ Zero config

**Free Tier:**
- Unlimited deployments
- 100 GB bandwidth/month
- Serverless functions

### Deployment Steps:

1. **Go to:** https://vercel.com
2. **Import** your GitHub repo
3. Vercel auto-detects Python
4. Add environment variables
5. Deploy

**Note:** Need to add `vercel.json`:
```json
{
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ]
}
```

**Pros:**
- Very fast
- Free tier generous
- Auto-deploys

**Cons:**
- Serverless (cold start)
- 10 second timeout on free tier

---

## 7. 🟠 Heroku (Classic)

**Why Choose Heroku:**
- ✅ Easy to use
- ✅ Lots of documentation
- ✅ Add-ons available

**Pricing:**
- No free tier anymore
- $5/month minimum (Eco Dynos)
- $7/month for always-on

### Deployment Steps:

1. **Install Heroku CLI**
2. **Login:** `heroku login`
3. **Create app:**
   ```bash
   heroku create hilldrive-invoice
   ```
4. **Add Procfile:**
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
5. **Deploy:**
   ```bash
   git push heroku master
   ```

**Pros:**
- Very easy
- Lots of add-ons
- Good documentation

**Cons:**
- No free tier
- More expensive than alternatives

---

## 📊 Comparison Table

| Platform | Free Tier | Cold Start | Setup Difficulty | Best For |
|----------|-----------|------------|------------------|----------|
| **Render** | ✅ 750h/mo | Yes (free) | ⭐ Easy | **Recommended** |
| **Railway** | ✅ $5 credit | No | ⭐ Easy | Small projects |
| **Your PC** | ✅ Free | No | ⭐⭐ Medium | Testing/Dev |
| **Google Cloud** | ✅ 2M req/mo | Yes (free) | ⭐⭐⭐ Hard | Scalable apps |
| **Azure** | ✅ Limited | Yes | ⭐⭐⭐ Hard | Enterprise |
| **Vercel** | ✅ 100GB/mo | Yes | ⭐ Easy | Serverless |
| **Heroku** | ❌ $5/mo | No | ⭐ Easy | Classic choice |

---

## 🎯 My Recommendation

### For You (Small Business):

**Option 1: Render.com ($7/month)**
- Always-on, no cold start
- Easy to manage
- Auto-deploys from GitHub
- Best value for money

**Option 2: Railway.app (Free)**
- $5 credit/month (enough for ~500 hours)
- No cold start
- Very fast
- Good for starting

**Option 3: Your Windows PC (Free)**
- If you have a PC that stays on 24/7
- Completely free
- Use ngrok for public URL
- Good for testing before paid deployment

---

## 🚀 Quick Start: Deploy to Render (5 Minutes)

1. Go to https://render.com
2. Sign up with GitHub
3. New → Web Service
4. Connect `EXcel_Invoice_Automation` repo
5. Settings:
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables from `.env`
7. Create Web Service
8. Done! Your app is live

---

## 💡 Tips

1. **Start with Render free tier** to test
2. **Upgrade to $7/month** when ready for production
3. **Use Google Drive API** for invoice storage (already implemented)
4. **Monitor usage** to avoid unexpected costs
5. **Keep GitHub repo updated** for auto-deploys

---

## 🆘 Need Help?

- **Render:** https://render.com/docs
- **Railway:** https://docs.railway.app
- **Google Cloud:** https://cloud.google.com/run/docs

---

**Which platform would you like to try? I can help you deploy!**
