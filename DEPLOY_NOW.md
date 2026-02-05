# 🚀 Deploy to PythonAnywhere - Quick Guide

You're already logged in! Follow these steps:

---

## Step 1: Upload Your Code (5 min)

### Option A: Using Git (Easiest)

1. Click **"Consoles"** tab at the top
2. Click **"$ Bash"** to open a terminal
3. Run these commands:

```bash
git clone https://github.com/Shubhamm5515/EXcel_Invoice_Automation.git
cd EXcel_Invoice_Automation
```

### Option B: Upload Files Manually

1. Click **"Files"** tab
2. Click **"Upload a file"**
3. Upload all your project files

---

## Step 2: Install Dependencies (3 min)

In the Bash console (from Step 1):

```bash
cd EXcel_Invoice_Automation

# Create virtual environment
python3.10 -m venv venv

# Activate it
source venv/bin/activate

# Install all packages
pip install -r requirements.txt
```

Wait for installation (~2 minutes)

---

## Step 3: Create Folders (1 min)

Still in Bash console:

```bash
mkdir -p generated_invoices
mkdir -p static
```

---

## Step 4: Setup Web App (5 min)

1. Click **"Web"** tab at the top
2. Click **"Add a new web app"** button
3. Click **"Next"**
4. Choose **"Manual configuration"**
5. Select **"Python 3.10"**
6. Click **"Next"**

---

## Step 5: Configure WSGI File (2 min)

1. On the Web tab, find **"Code"** section
2. Click on the **WSGI configuration file** link (blue text)
3. **DELETE ALL** the existing content
4. **PASTE THIS** (replace `Sarthak1` with your actual username):

```python
import sys
import os

# IMPORTANT: Replace 'Sarthak1' with YOUR PythonAnywhere username
project_home = '/home/Sarthak1/EXcel_Invoice_Automation'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Activate virtual environment
activate_this = os.path.join(project_home, 'venv/bin/activate_this.py')
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Load environment variables
from dotenv import load_dotenv
load_dotenv(os.path.join(project_home, '.env'))

# Import FastAPI app
from main import app as application
```

5. Click **"Save"** (top right)

---

## Step 6: Set Virtual Environment Path (1 min)

1. Go back to **"Web"** tab
2. Find **"Virtualenv"** section
3. Enter this path (replace `Sarthak1` with your username):
   ```
   /home/Sarthak1/EXcel_Invoice_Automation/venv
   ```
4. Click the checkmark ✓

---

## Step 7: Set Working Directory (1 min)

1. Still on **"Web"** tab
2. Find **"Code"** section
3. Set **"Source code"** to (replace username):
   ```
   /home/Sarthak1/EXcel_Invoice_Automation
   ```
4. Set **"Working directory"** to (replace username):
   ```
   /home/Sarthak1/EXcel_Invoice_Automation
   ```

---

## Step 8: Reload Web App (1 min)

1. Scroll to top of **"Web"** tab
2. Click the big green **"Reload"** button
3. Wait for "Reload complete" message

---

## Step 9: Test Your App! (1 min)

Open your app URL (replace with your username):
```
https://sarthak1.pythonanywhere.com
```

You should see your invoice web interface!

Test the API:
```
https://sarthak1.pythonanywhere.com/health
```

Should show:
```json
{"status":"healthy","version":"1.0.0",...}
```

---

## ✅ You're Live!

Your invoice system is now:
- ✅ **Online 24/7** (no cold start)
- ✅ **Free forever** (PythonAnywhere free tier)
- ✅ **Accessible anywhere**

**Your URL:** `https://sarthak1.pythonanywhere.com`

---

## Common Issues & Fixes

### Issue: "Import Error" or "Module not found"

**Fix:**
```bash
# In Bash console
cd EXcel_Invoice_Automation
source venv/bin/activate
pip install -r requirements.txt
```
Then reload web app.

### Issue: "404 Not Found"

**Fix:**
- Check WSGI file has correct username
- Check virtual environment path is correct
- Check working directory is correct
- Reload web app

### Issue: "Static files not loading"

**Fix:**
```bash
# In Bash console
cd EXcel_Invoice_Automation
ls static/
# Should show: index.html, style.css, script.js
```

If missing, upload them to the `static` folder.

---

## View Logs

If something goes wrong:

1. Go to **"Web"** tab
2. Scroll down to **"Log files"**
3. Click **"Error log"** to see errors
4. Click **"Server log"** to see requests

---

## Update Your Code Later

When you make changes:

```bash
# In Bash console
cd EXcel_Invoice_Automation
git pull  # If using Git

# Or upload new files via Files tab

# Then reload
# Go to Web tab → Click Reload button
```

---

## Next: Setup Google Drive (Optional)

After deployment works, you can setup Google Drive to auto-upload invoices.

See: `GOOGLE_DRIVE_SETUP.md`

---

**Need help? Check the error log or ask me!**
