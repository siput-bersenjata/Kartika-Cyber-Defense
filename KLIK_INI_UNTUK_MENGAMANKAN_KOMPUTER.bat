@echo off
title SISTEM PENANGKAL SIBER KARTIKA // PUSSIBERAD HACKATHON 2026
color 0A
cls
echo ======================================================================
echo  [+] PUSAT SIBER TNI ANGKATAN DARAT (PUSSIBERAD) - HACKATHON 2026
echo  [+] SISTEM PENANGKAL SIBER KARTIKA (PORTABLE USB EDITION)
echo  [+] Arsitek Pertahanan: Sovian (@siput-bersenjata)
echo  [+] Melindungi Workstation dari Serangan Ransomware ^& File Dropper
echo ======================================================================
echo.
echo [*] Melakukan pra-inspeksi ^& sterilisasi memori kilat...

:: 1. Bersihkan proses malware aktif jika ada di latar belakang
taskkill /F /FI "WINDOWTITLE eq *ransomware*" >nul 2>&1
taskkill /F /FI "IMAGENAME eq Simulasi_Korban_Dokumen_Palsu.exe" >nul 2>&1
taskkill /F /FI "IMAGENAME eq Installer_Aplikasi_Bajakan.exe" >nul 2>&1

:: 2. Bersihkan kunci registri autorun persistensi malware
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "Kartika_Weaponized_Doc_Dropper" /f >nul 2>&1
reg delete "HKLM\Software\Microsoft\Windows\CurrentVersion\Run" /v "Kartika_Weaponized_Doc_Dropper" /f >nul 2>&1

echo [+] Memori ^& registri awal berhasil disanitasi!
echo [*] Mengaktifkan Perisai Pertahanan Otomatis ^& Radar Taktis...
echo [*] Dashboard Radar akan otomatis terbuka di http://127.0.0.1:5001
echo.

cd /d "%~dp0"
start "" cmd /c "timeout /t 3 /nobreak >nul && start http://127.0.0.1:5001"

if exist "%~dp0AKTIFKAN_PERISAI_PENANGKAL_KARTIKA.exe" (
    start "" "%~dp0AKTIFKAN_PERISAI_PENANGKAL_KARTIKA.exe"
) else if exist "%~dp002_Canary_Shield_Portable\Kartika_Canary_Shield.exe" (
    cd /d "%~dp002_Canary_Shield_Portable"
    start "" "Kartika_Canary_Shield.exe"
) else (
    echo [!] File executable tidak ditemukan.
    pause
)

echo ======================================================================
echo  [+] PERISAI SIBER KARTIKA TELAH AKTIF MELINDUNGI KOMPUTER ANDA!
echo  [+] Di browser, tekan tombol: [TANGKIS TOTAL SEMUA ANCAMAN]
echo      untuk menjalankan seluruh 12 fitur pertahanan secara serentak.
echo ======================================================================
echo.
timeout /t 5
