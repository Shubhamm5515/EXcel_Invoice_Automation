# 🔧 QUICK FIX - Render Deployment Error

## ❌ Error You're Seeing

```
ERROR: Error loading ASGI app. Could not import module "main".
```

## 🎯 The Problem

Render is trying to run `uvicorn main:app` but we renamed the file to `main_new.py`.

---

## ✅ Solution (2 Minutes)

### Option 1: Update Start Command in Render Dashboard (Fastest)

1. **Go to your Render service** (the one that's failing)
2. **Click "Settings"** (left sidebar)
3. **Scroll to "Start Command"**
4. **Change from:**
   ```
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
5. **Change to:**
   ```
   uvicorn main_new:app --host 0.0.0.0 --port $PORT
   ```
6. **Click "Save Changes"**
7. **Render will auto-redeploy** (wait 2-3 minutes)

### Option 2: Create main.py Symlink (Alternative)

If you want to keep using `main:app`, create a simple redirect file:

**Create `main.py`:**
```python
"""
Redirect to main_new.py for backward compatibility
"""
from main_new import app

__all__ = ['app']
```

Then push to GitHub:
```bash
git add main.py
git commit -m "Add main.py redirect for Render"
git push origin master
```

Render will auto-redeploy.

---

## 🚀 Recommended: Option 1 (Update Start Command)

This is cleaner and doesn't require code changes.

### Step-by-Step with Screenshots

1. **In Render Dashboard:**
   - Click on your service name
   - Left sidebar → "Settings"
   
2. **Find "Build & Deploy" section:**
   - Look for "Start Command"
   - Current value: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   
3. **Update to:**
   ```
   uvicorn main_new:app --host 0.0.0.0 --port $PORT
   ```
   
4. **Scroll down and click "Save Changes"**

5. **Wait for auto-redeploy** (2-3 minutes)

---

## ✅ After Fix

You should see in logs:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:10000
```

Then test:
```
✅ https://your-app.onrender.com
✅ https://your-app.onrender.com/health
✅ https://your-app.onrender.com/static/car-viewer.html
```

---

## 🐛 If Still Failing

### Check These:

1. **Environment Variables Set?**
   - Settings → Environment
   - Must have: `OCR_SPACE_API_KEY`, `OPENROUTER_API_KEY`

2. **Build Succeeded?**
   - Check "Logs" tab
   - Should see: "Build successful 🎉"

3. **Files Pushed to GitHub?**
   - Check your repo has `main_new.py`
   - Verify `app/` folder exists

4. **Python Version?**
   - Render uses Python 3.11 by default
   - Should work fine

---

## 💡 Why This Happened

We refactored the code and renamed `main.py` to `main_new.py` for the modular architecture. The `render.yaml` file has the correct command, but if you manually set the start command in the Render dashboard earlier, it overrides the yaml file.

---

## 🎯 Quick Commands

### If Using Option 2 (Create main.py):

```bash
# Create redirect file
echo 'from main_new import app' > main.py

# Push to GitHub
git add main.py
git commit -m "Add main.py redirect"
git push origin master
```

### Check Deployment Status:

Go to Render dashboard → Logs tab → Watch for:
```
✅ Build successful
✅ Deploy live
✅ Uvicorn running
```

---

## 📞 Still Stuck?

### Check Render Logs

In Render dashboard:
1. Click "Logs" tab
2. Look for error messages
3. Common issues:
   - Missing environment variables
   - Import errors
   - Port binding issues

### Test Locally First

```bash
# Make sure it works locally
python main_new.py

# Should see:
# INFO: Uvicorn running on http://0.0.0.0:8000
```

---

## ✅ Success Checklist

After fixing:

- [ ] Start command updated to `main_new:app`
- [ ] Deployment succeeded
- [ ] Logs show "Uvicorn running"
- [ ] Homepage loads
- [ ] /health endpoint works
- [ ] 3D viewer loads
- [ ] No errors in logs

---

## 🚀 You're Almost There!

Just update the start command and you'll be live in 2 minutes!

**Go to Render → Settings → Start Command → Change to `main_new:app`**

Good luck! 🎉
