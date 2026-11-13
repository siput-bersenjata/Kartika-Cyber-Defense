@echo off
title KARTIKA CANARY-SHIELD ^& MILITARY CRYPTO-VAULT // PUSSIBERAD
cd /d "%~dp0"
cls
echo =====================================================================
echo   [+] KARTIKA CANARY-SHIELD ^& MILITARY CRYPTO-VAULT
echo   [+] Kategori 02: DEFENSIVE SHIELD // PUSSIBERAD HACKATHON 2026
echo   [+] Sub-50ms Zero-Day Ransomware Interceptor ^& AES-256-GCM Vault
echo =====================================================================
echo.
echo [*] Membuka Dashboard Komando Taktis di http://127.0.0.1:5001 ...
echo [*] Browser default akan otomatis terbuka dalam 2 detik...
echo.

start "" cmd /c "timeout /t 2 /nobreak >nul && start http://127.0.0.1:5001"
python app.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [-] Terjadi kesalahan saat menjalankan aplikasi!
    pause
)
