@echo off
title CEK ^& PULIHKAN SHADOW COPY (VSS) // PUSSIBERAD HACKATHON 2026
color 0B
cls
echo ======================================================================
echo  [+] SISTEM PEMULIHAN SNAPSHOT VSS MILITER (PUSSIBERAD 2026)
echo  [+] Arsitek Pertahanan: Sovian (@siput-bersenjata)
echo  [+] Disaster Recovery: Cek Snapshot Cadangan Windows Sebelum Serangan
echo ======================================================================
echo.

echo [*] Memeriksa status layanan Volume Shadow Copy (VSS)...
sc query vss | findstr /i "STATE"
echo.

echo [*] Memeriksa daftar snapshot cadangan di Drive C: ...
vssadmin list shadows /for=C:
if %errorlevel% neq 0 (
    echo.
    echo [!] PERINGATAN: Memerlukan hak Administrator untuk membaca daftar snapshot fisik.
    echo [*] SOP: Klik kanan file ini lalu pilih "Run as administrator" jika ingin melihat detail.
)

echo.
echo ======================================================================
echo  [+] PETUNJUK PEMULIHAN CEPAT:
echo  1. Jika ransomware sempat mengenkripsi berkas sebelum perisai aktif,
echo     snapshot di atas dapat dipakai untuk memulihkan seluruh folder.
echo  2. Anda juga dapat menggunakan dashboard web di: http://127.0.0.1:5001
echo ======================================================================
echo.
pause
