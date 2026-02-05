# 📤 Upload Code to GitHub - Step by Step

## Prerequisites

- Git installed on your computer
- GitHub account

## Step 1: Install Git (if not installed)

### Windows
Download from: https://git-scm.com/download/win

### Check if Git is installed
```bash
git --version
```

Should show: `git version 2.x.x`

---

## Step 2: Configure Git (First Time Only)

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

## Step 3: Create GitHub Repository

1. Go to: https://github.com
2. Click **"+"** (top right) → **"New repository"**
3. Fill in:
   - **Repository name:** `hilldrive-invoice`
   - **Description:** `Invoice automation system for Hill Drive`
   - **Visibility:** Private (recommended) or Public
   - **DON'T** initialize with README (we have one)
4. Click **"Create repository"**

**Copy the repository URL** (looks like):
```
https://github.com/YOUR_USERNAME/hilldrive-invoice.git
```

---

## Step 4: Initialize Git in Your Project

Open terminal/command prompt in your project folder:

```bash
# Navigate to project folder
cd C:\Users\ASUS\Desktop\Invoice

# Initialize Git
git init
```

Should show: `Initialized empty Git repository`

---

## Step 5: Add Files to Git

```bash
# Add all files (respects .gitignore)
git add .

# Check what will be committed
git status
```

You should see files in green (ready to commit).

**Important:** `.env` and `google_credentials.json` should NOT appear (they're in .gitignore)

---

## Step 6: Create First Commit

```bash
git commit -m "Initial commit - Hill Drive Invoice System"
```

Should show: `X files changed, Y insertions(+)`

---

## Step 7: Connect to GitHub

```bash
# Add remote repository (use YOUR URL from Step 3)
git remote add origin https://github.com/YOUR_USERNAME/hilldrive-invoice.git

# Verify remote
git remote -v
```

Should show:
```
origin  https://github.com/YOUR_USERNAME/hilldrive-invoice.git (fetch)
origin  https://github.com/YOUR_USERNAME/hilldrive-invoice.git (push)
```

---

## Step 8: Push to GitHub

```bash
# Push code to GitHub
git push -u origin main
```

**If it asks for credentials:**
- Username: Your GitHub username
- Password: Use **Personal Access Token** (not your password)

### Create Personal Access Token:
1. GitHub → Settings → Developer settings
2. Personal access tokens → Tokens (classic)
3. Generate new token
4. Select scopes: `repo` (full control)
5. Copy token (save it somewhere safe!)
6. Use token as password

---

## Step 9: Verify Upload

1. Go to: `https://github.com/YOUR_USERNAME/hilldrive-invoice`
2. You should see all your files!
3. Check that `.env` is NOT there (good!)

---

## ✅ Success!

Your code is now on GitHub!

**Repository URL:**
```
https://github.com/YOUR_USERNAME/hilldrive-invoice
```

---

## Future Updates

When you make changes:

```bash
# Add changed files
git add .

# Commit with message
git commit -m "Description of changes"

# Push to GitHub
git push
```

---

## Common Issues & Solutions

### Issue: "fatal: not a git repository"
**Solution:**
```bash
git init
```

### Issue: "remote origin already exists"
**Solution:**
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/hilldrive-invoice.git
```

### Issue: "failed to push some refs"
**Solution:**
```bash
git pull origin main --rebase
git push origin main
```

### Issue: "Permission denied"
**Solution:**
- Use Personal Access Token instead of password
- Or setup SSH keys

---

## Verify .gitignore is Working

Check that these files are NOT in GitHub:
- ❌ `.env`
- ❌ `google_credentials.json`
- ❌ `generated_invoices/*.xlsx` (except .gitkeep)
- ❌ `__pycache__/`
- ❌ `venv/`

If they appear, they were committed before .gitignore. To remove:

```bash
git rm --cached .env
git rm --cached google_credentials.json
git commit -m "Remove sensitive files"
git push
```

---

## Clone Repository (On Another Computer)

```bash
git clone https://github.com/YOUR_USERNAME/hilldrive-invoice.git
cd hilldrive-invoice

# Install dependencies
pip install -r requirements.txt

# Create .env file (manually)
# Add your API keys

# Run
uvicorn main:app --host 0.0.0.0 --port 8001
```

---

## Branch Strategy (Optional)

For team collaboration:

```bash
# Create development branch
git checkout -b development

# Make changes
git add .
git commit -m "New feature"

# Push branch
git push origin development

# Create Pull Request on GitHub
# Merge to main after review
```

---

## GitHub Features to Use

### 1. Releases
Tag versions:
```bash
git tag -a v1.0.0 -m "First release"
git push origin v1.0.0
```

### 2. Issues
Track bugs and features on GitHub Issues tab

### 3. Wiki
Document your project in GitHub Wiki

### 4. Actions
Setup CI/CD (auto-deploy on push)

---

## Security Checklist

Before pushing:

- [x] `.env` in `.gitignore`
- [x] `google_credentials.json` in `.gitignore`
- [x] No API keys in code
- [x] No passwords in code
- [x] Repository is Private (if needed)

---

## Next Steps

1. ✅ Code is on GitHub
2. ✅ Ready to deploy to PythonAnywhere
3. ✅ Can clone on any computer
4. ✅ Team can collaborate

**Now follow:** `PYTHONANYWHERE_COMPLETE_GUIDE.md` to deploy!

---

## Quick Reference

```bash
# Status
git status

# Add files
git add .

# Commit
git commit -m "Message"

# Push
git push

# Pull latest
git pull

# View history
git log

# Undo last commit (keep changes)
git reset --soft HEAD~1
```

---

**Your code is now safely backed up on GitHub!** 🎉
