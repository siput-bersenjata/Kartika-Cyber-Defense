@echo off
title KARTIKA TRIAGE SENTINEL // PUSSIBERAD TNI AD
cd /d "%~dp0"
cls
echo =====================================================================
echo   [+] KARTIKA TRIAGE SENTINEL - PUSSIBERAD HACKATHON 2026
echo   [+] Tactical Air-Gapped Cyber Incident ^& Forensics Triage Kit
echo =====================================================================
echo.
echo [*] Memulai server lokal di http://127.0.0.1:5000 ...
echo [*] Browser default akan otomatis terbuka dalam 2 detik...
echo.

:: Buka browser di latar belakang setelah jeda 2 detik
start "" cmd /c "timeout /t 2 /nobreak >nul && start http://127.0.0.1:5000"

:: Jalankan server Python di jendela ini
python app.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [-] Terjadi kesalahan saat menjalankan aplikasi!
    echo [-] Pastikan Python sudah terpasang dan jalankan: pip install flask psutil requests
    pause
)
