@echo off
REM GoldAnalysisAI launcher (Windows) -> cross-platform run_app.py
setlocal
cd /d "%~dp0"
python run_app.py %*
exit /b %ERRORLEVEL%
