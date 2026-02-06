@echo off
echo ========================================
echo Hill Drive Invoice - Deploy to GitHub
echo ========================================
echo.

echo Checking git status...
git status
echo.

echo Adding all changes...
git add .
echo.

echo Enter commit message (or press Enter for default):
set /p commit_msg="Commit message: "
if "%commit_msg%"=="" set commit_msg="Updated frontend with 3D car viewer"

echo.
echo Committing with message: %commit_msg%
git commit -m "%commit_msg%"
echo.

echo Pushing to GitHub...
git push origin main
echo.

echo ========================================
echo ✅ Deployment Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Go to Render.com or Railway.app
echo 2. Connect your GitHub repo
echo 3. Deploy automatically!
echo.
echo Your repo: https://github.com/Shubhamm5515/EXcel_Invoice_Automation
echo.
pause
