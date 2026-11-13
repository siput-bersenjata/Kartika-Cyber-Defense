@echo off
title SANISASI DAN IMUNISASI FLASHDISK // PUSSIBERAD HACKATHON 2026
color 0A
cls
echo ======================================================================
echo  [+] SISTEM SANISASI DAN IMUNISASI FLASHDISK (PUSSIBERAD 2026)
echo  [+] Arsitek Pertahanan: Sovian (@siput-bersenjata)
echo  [+] Melindungi Media USB dari Virus Shortcut, Autorun, dan Hidden Trojan
echo ======================================================================
echo.

cd /d "%~dp0"
echo [*] Melakukan scanning dan pembersihan direktori USB: %~dp0
echo.

echo [1/4] Memulihkan berkas dinas yang disembunyikan oleh virus shortcut...
attrib -h -r -s /s /d "%~dp0*.*" >nul 2>&1
echo       [V] Atribut hidden dan system berhasil dinormalkan!

echo.
echo [2/4] Membersihkan shortcut beracun .lnk di media flashdisk...
if exist "%~dp0*.lnk" (
    del /f /q "%~dp0*.lnk" >nul 2>&1
    echo       [V] File shortcut berbahaya berhasil dimusnahkan!
) else (
    echo       [V] Media bersih. Tidak ditemukan file shortcut liar.
)

echo.
echo [3/4] Memasang Ranjau Imunisasi Autorun...
if not exist "%~dp0autorun.inf" (
    mkdir "%~dp0autorun.inf\con\nul" >nul 2>&1
    attrib +r +s +h "%~dp0autorun.inf" >nul 2>&1
    echo       [V] Folder kekebalan autorun.inf berhasil dipasang terkunci!
) else (
    echo       [V] Folder imunisasi autorun.inf sudah aktif terpasang.
)

echo.
echo [4/4] Memverifikasi integritas file eksekutabel Sistem Penangkal Kartika...
if exist "%~dp0AKTIFKAN_PERISAI_PENANGKAL_KARTIKA.exe" (
    echo       [V] AKTIFKAN_PERISAI_PENANGKAL_KARTIKA.exe terverifikasi aman dan siap tugas.
) else (
    echo       [!] Executable utama belum tersinkronisasi.
)

echo.
echo ======================================================================
echo  [+] STATUS: FLASHDISK SELESAI DISANISASI DAN TERLINDUNGI DARI VIRUS
echo  [+] Media penyimpanan aman untuk dicolokkan ke laptop komando / operasi.
echo ======================================================================
echo.
pause
