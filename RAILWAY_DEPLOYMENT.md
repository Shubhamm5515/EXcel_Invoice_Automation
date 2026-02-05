# 🚀 Railway.app Deployment - NO Cold Start

## Why Railway?

✅ **NO COLD START** - Always active, instant response  
✅ **Easy setup** - 5 minutes total  
✅ **Auto-deploy** - Push to GitHub = Auto deploy  
✅ **$5/month** - Very affordable  
✅ **512 MB RAM** - Good performance  
✅ **Custom domains** - Free HTTPS  

---

## Step-by-Step Deployment

### Step 1: Push to GitHub (5 min)

```bash
# Initialize git
git init

# Add .gitignore
echo ".env
google_credentials.json
__pycache__/
*.pyc
venv/
generated_invoices/*.xlsx" > .gitignore

# Commit
git add .
git commit -m "Initial commit"

# Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/hilldrive-invoice.git
git push -u origin main
```

---

### Step 2: Create Railway Account (2 min)

1. Go to: **https://railway.app**
2. Click **"Login"**
3. Sign in with **GitHub** (easiest)
4. Authorize Railway

You get **$5 free credit** to start!

---

### Step 3: Create New Project (1 min)

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your **hilldrive-invoice** repository
4. Railway will auto-detect it's a Python app

---

### Step 4: Configure Environment Variables (2 min)

Click on your service → **Variables** tab

Add these:

```
OCR_SPACE_API_KEY=K88999613688957
OPENROUTER_API_KEY=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
OPENROUTER_MODEL=google/gemini-2.5-flash
USE_OPENROUTER=true
USE_MASTER_FILE=false
TEMPLATE_PATH=inn sample.xlsx
OUTPUT_DIR=generated_invoices
DEBUG=false
```

Click **"Add"** for each variable.

---

### Step 5: Deploy! (Automatic)

Railway automatically:
1. ✅ Detects Python
2. ✅ Installs dependencies from `requirements.txt`
3. ✅ Runs your app
4. ✅ Gives you a URL

**Your URL:** `https://hilldrive-invoice-production.up.railway.app`

---

### Step 6: Get Your URL (1 min)

1. Go to **Settings** tab
2. Click **"Generate Domain"**
3. Copy your URL
4. Test it!

```bash
curl https://your-app.up.railway.app/health
```

---

## ✅ You're Live!

Your invoice system is now:
- ✅ **Always on** - No cold start
- ✅ **Fast** - Instant response
- ✅ **Secure** - HTTPS included
- ✅ **Auto-deploy** - Push = Deploy

---

## Auto-Deploy Setup

Every time you push to GitHub:

```bash
# Make changes
git add .
git commit -m "Updated feature"
git push

# Railway automatically:
# 1. Detects push
# 2. Rebuilds app
# 3. Deploys new version
# 4. Zero downtime!
```

---

## Custom Domain (Optional)

1. Buy domain (e.g., Namecheap, $10/year)
2. In Railway: **Settings** → **Domains**
3. Click **"Custom Domain"**
4. Add your domain: `api.hilldrive.com`
5. Update DNS records (Railway shows you how)
6. Done! Free HTTPS included

---

## Monitoring

Railway provides:

**Metrics:**
- CPU usage
- Memory usage
- Network traffic
- Response times

**Logs:**
- Real-time logs
- Error tracking
- Request logs

Access from **Metrics** and **Logs** tabs.

---

## Cost Breakdown

**Free Credit:** $5/month

**Usage:**
- ~$5/month for always-on service
- 512 MB RAM
- Unlimited requests

**After free credit:**
- Add payment method
- Pay only $5/month
- Or add more credit

**Very affordable for always-on service!**

---

## Upgrade Options

**Hobby Plan:** $5/month
- What you're using
- 512 MB RAM
- Always on

**Pro Plan:** $20/month
- 8 GB RAM
- Priority support
- More resources

Start with Hobby, upgrade if needed.

---

## Files Needed

✅ `requirements.txt` - Already have  
✅ `main.py` - Already have  
✅ `railway.json` - Created (optional)  
✅ `.gitignore` - Important!  

---

## Troubleshooting

### Build Failed
**Check:**
- `requirements.txt` is correct
- Python version compatible
- View build logs in Railway

**Fix:**
- Update requirements
- Push again

### App Not Starting
**Check:**
- Start command is correct
- Port is `$PORT` (Railway provides)
- View logs in Railway

**Fix:**
- Check `railway.json` start command
- Redeploy

### Environment Variables Not Working
**Check:**
- Variables are saved
- Spelling is correct
- Redeploy after adding

---

## Security Checklist

Before deploying:

- [x] `.env` in `.gitignore`
- [x] `google_credentials.json` in `.gitignore`
- [x] API keys as environment variables
- [x] No sensitive data in code
- [x] `DEBUG=false` in production

---

## Comparison: Railway vs Others

| Feature | Railway | Render Free | PythonAnywhere |
|---------|---------|-------------|----------------|
| Cold Start | ❌ No | ✅ Yes | ❌ No |
| Cost | $5/mo | $0 | $0 |
| Setup | 5 min | 5 min | 10 min |
| Auto-deploy | ✅ Yes | ✅ Yes | ❌ No |
| Custom Domain | ✅ Yes | ✅ Yes | $5/mo |
| RAM | 512 MB | 512 MB | Limited |

**Railway = Best balance of features and cost**

---

## Alternative: Keep Render + UptimeRobot

If you want to stay with Render free tier:

1. Deploy to Render (free)
2. Use UptimeRobot (free) to ping every 5 min
3. No cold start!

**Cost:** $0/month

But Railway is more reliable and only $5/month.

---

## Next Steps

1. ✅ Push code to GitHub
2. ✅ Create Railway account
3. ✅ Deploy from GitHub
4. ✅ Add environment variables
5. ✅ Get your URL
6. ✅ Test it!

**Total time: 10 minutes**
**Cost: $5/month**
**Result: Always-on, no cold start!**

---

## Support

Railway has:
- 📚 Great documentation
- 💬 Discord community
- 📧 Email support
- 🎥 Video tutorials

Very beginner-friendly!

---

**Ready to deploy? Let me know if you need help with any step!**
