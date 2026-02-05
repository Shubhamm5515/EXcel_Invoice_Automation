@echo off
echo ========================================
echo GitHub Upload Script
echo ========================================
echo.

echo Step 1: Initializing Git...
git init
echo.

echo Step 2: Adding files...
git add .
echo.

echo Step 3: Creating commit...
git commit -m "Initial commit - Hill Drive Invoice System"
echo.

echo Step 4: Adding remote repository...
echo Please enter your GitHub repository URL:
echo Example: https://github.com/YOUR_USERNAME/hilldrive-invoice.git
set /p REPO_URL="Repository URL: "
git remote add origin %REPO_URL%
echo.

echo Step 5: Pushing to GitHub...
git push -u origin main
echo.

echo ========================================
echo Done! Check your GitHub repository.
echo ========================================
pause
