@echo off
title Bundling NHS CQ Portal

echo ==========================================
echo Packaging Hermetic NHS Portal
echo ==========================================

cd /d "%~dp0"

echo Compressing files into NHS_SBS_Portal.zip...
echo This might take a moment depending on the size of the local AI models.

:: Using Windows native tar to create a zip
tar.exe -a -c -f "NHS_SBS_Portal.zip" backend data frontend models scripts venv start.bat

echo.
echo Packaging Complete! 
echo You can now distribute the NHS_SBS_Portal.zip file.
pause
