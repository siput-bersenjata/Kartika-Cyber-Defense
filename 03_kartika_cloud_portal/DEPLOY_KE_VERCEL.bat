@echo off
TITLE [PUSSIBERAD 2026] DEPLOY KARTIKA CLOUD COMMAND PORTAL KE VERCEL
COLOR 0A
chcp 65001 >nul

echo ===============================================================================
echo     PUSSIBERAD - KARTIKA CYBER HACKATHON 2026
echo     DEPLOY SISTEM PENANGKAL BERBASIS WEB CLOUD KE VERCEL
echo ===============================================================================
echo.
echo [INFO] Direktori Web Portal: 04_kartika_cloud_portal_vercel
echo [INFO] Deployment ini membuat website demo juri aktif 24/7 di Vercel Cloud
echo        sehingga juri/panitia dapat membuka dan menguji simulator tanpa perlu
echo        menyalakan laptop atau server lokal.
echo.
echo -------------------------------------------------------------------------------
echo Menjalankan Vercel CLI (npx vercel)...
echo Jika diminta login, pilih Continue with GitHub / Email pada browser Anda.
echo Ikuti petunjuk di terminal (tekan Enter untuk opsi default).
echo -------------------------------------------------------------------------------
echo.

cd /d "%~dp0"
call npx vercel --prod

echo.
echo ===============================================================================
echo [SELESAI] Deployment ke Vercel selesai!
echo Salin tautan URL Vercel (contoh: https://kartika-cyber-defense-portal.vercel.app)
echo dan masukkan ke form submisi atau kirimkan ke juri/panitia hackathon.
echo ===============================================================================
pause
