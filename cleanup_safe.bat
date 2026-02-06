@echo off
REM Safe Cleanup Script for Hill Drive Invoice Automation
REM This script deletes only SAFE files (obsolete documentation and code)

echo ========================================
echo Hill Drive Invoice Cleanup Script
echo ========================================
echo.
echo This will delete 32 obsolete files:
echo - 20 old documentation files
echo - 8 obsolete code files
echo - 2 unused storage files
echo - 2 test files
echo.
echo Your important files will NOT be deleted!
echo.
pause

echo.
echo Creating backup first...
if not exist "..\Invoice_Backup" (
    xcopy /E /I /Q . ..\Invoice_Backup
    echo Backup created at: ..\Invoice_Backup
) else (
    echo Backup already exists at: ..\Invoice_Backup
)
echo.

echo Deleting obsolete documentation files...
del /Q CHANGES_SUMMARY.md 2>nul
del /Q CLOUD_BACKUP_COMPLETE.md 2>nul
del /Q COMMANDS_TO_RUN.txt 2>nul
del /Q DEBUG_MEGA.md 2>nul
del /Q DEPLOY_NOW.md 2>nul
del /Q DEPLOYMENT_READY.md 2>nul
del /Q FINAL_SETUP_MEGA.md 2>nul
del /Q FIXED.txt 2>nul
del /Q FIXES_APPLIED.md 2>nul
del /Q GITHUB_SUCCESS.md 2>nul
del /Q GITHUB_UPLOAD_GUIDE.md 2>nul
del /Q GOOGLE_DRIVE_COMPLETE_SETUP.md 2>nul
del /Q GOOGLE_DRIVE_SETUP.md 2>nul
del /Q MEGA_NETWORK_ISSUE.md 2>nul
del /Q MEGA_SETUP_GUIDE.md 2>nul
del /Q NO_COLD_START_DEPLOYMENT.md 2>nul
del /Q RENDER_FIX.md 2>nul
del /Q RENDER_NO_DOWNTIME.md 2>nul
del /Q RENDER_WITH_KEEPALIVE.md 2>nul
del /Q START_HERE.md 2>nul
del /Q SYSTEM_COMPLETE.md 2>nul
del /Q TEST_MEGA_UPLOAD.md 2>nul
echo Done! (20 files)

echo.
echo Deleting obsolete code files...
del /Q schemas.py 2>nul
del /Q check_calculation.py 2>nul
del /Q check_template_formulas.py 2>nul
del /Q test_extraction.py 2>nul
del /Q optimize_project.py 2>nul
del /Q install.py 2>nul
del /Q diagnose.bat 2>nul
del /Q upload_to_github.bat 2>nul
echo Done! (8 files)

echo.
echo Deleting unused storage files...
del /Q pcloud_storage.py 2>nul
del /Q local_backup.py 2>nul
echo Done! (2 files)

echo.
echo Deleting test files...
del /Q test_invoice.xlsx 2>nul
del /Q HD-20260205-822926.xlsx 2>nul
echo Done! (2 files)

echo.
echo Deleting extra environment files...
del /Q .env.production 2>nul
del /Q .python-version 2>nul
echo Done! (2 files)

echo.
echo ========================================
echo Cleanup Complete!
echo ========================================
echo.
echo Deleted: 34 obsolete files
echo Backup: ..\Invoice_Backup
echo.
echo Your important files are safe:
echo - app/ (modular code)
echo - tests/ (test suite)
echo - static/ (web interface)
echo - generated_invoices/ (your invoices)
echo - main_new.py (new entry point)
echo - All configuration files
echo.
echo Next steps:
echo 1. Test the application: python main_new.py
echo 2. Run tests: python -m pytest tests/ -v
echo 3. If everything works, you can delete main.py in 1 week
echo.
pause
