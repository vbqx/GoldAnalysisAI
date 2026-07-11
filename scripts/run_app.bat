@echo off
cd /d "%~dp0\.."
python run_app.py %*
exit /b %ERRORLEVEL%
