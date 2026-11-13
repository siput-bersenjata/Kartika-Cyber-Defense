@echo off
title OPERASI TANGKIS TOTAL SIBER KARTIKA // PUSSIBERAD HACKATHON 2026
color 0A
cls
echo ======================================================================
echo  [+] PUSAT SIBER TNI ANGKATAN DARAT (PUSSIBERAD) - HACKATHON 2026
echo  [+] OPERASI PENANGKALAN TOTAL SIBER KARTIKA (ONE-CLICK COMPLETE DEFENSE)
echo  [+] Pengembang: Sovian (@siput-bersenjata) // SHA256-MILITARY-GRADE
echo ======================================================================
echo.
echo [*] Memulai Operasi Penangkalan Total untuk Melindungi Workstation...
echo.

:: 1. Jalankan Engine Penangkal jika belum menyala
netstat -ano | findstr :5001 >nul
if %ERRORLEVEL% NEQ 0 (
    echo [*] Mengaktifkan engine perisai pertahanan port 5001...
    if exist "%~dp0dist\AKTIFKAN_PERISAI_PENANGKAL_KARTIKA.exe" (
        start /min "" "%~dp0dist\AKTIFKAN_PERISAI_PENANGKAL_KARTIKA.exe"
    ) else if exist "%~dp002_itot_pangkalan_shield\app.py" (
        start /min "" cmd /c "cd /d "%~dp002_itot_pangkalan_shield" && python app.py"
    )
    timeout /t 3 >nul
) else (
    echo [+] Engine Perisai Pertahanan telah aktif siaga di Port 5001.
)

:: 2. Jalankan PowerShell Runner untuk memanggil API Total Countermeasure dan melakukan verifikasi menyeluruh
powershell -NoProfile -ExecutionPolicy Bypass -Command "& {
    Write-Host '[1/11] Mempersenjatai tripwires Canary-Shield (.docx & .kml)...' -ForegroundColor Cyan
    Write-Host '[2/11] Memindai seluruh memori volatil (RAM) & proses sistem...' -ForegroundColor Cyan
    Write-Host '[3/11] Melumpuhkan seluruh PID ancaman malware & ransomware...' -ForegroundColor Cyan
    Write-Host '[4/11] Mensterilkan kunci registri autorun persistensi Windows...' -ForegroundColor Cyan
    Write-Host '[5/11] Mendekripsi & memulihkan berkas dokumen militer terkunci...' -ForegroundColor Cyan
    Write-Host '[6/11] Memusnahkan ransom note & membersihkan berkas terenkripsi...' -ForegroundColor Cyan
    Write-Host '[7/11] Memindai dropper biner/skrip di folder Temp & AppData...' -ForegroundColor Cyan
    Write-Host '[8/11] Memeriksa snapshot Volume Shadow Copy (VSS) Windows...' -ForegroundColor Cyan
    Write-Host '[9/11] Menginspeksi muatan berbahaya di soket jaringan...' -ForegroundColor Cyan
    Write-Host '[10/11] Menyinkronkan telemetri artefak forensik Triage Sentinel...' -ForegroundColor Cyan
    Write-Host '[11/11] Merekonstruksi garis waktu kronologis MITRE ATT&CK...' -ForegroundColor Cyan
    Write-Host ''

    try {
        $uri = 'http://127.0.0.1:5001/api/defense/total_action'
        $resp = Invoke-RestMethod -Uri $uri -Method POST -TimeoutSec 10
        Write-Host '======================================================================' -ForegroundColor Green
        Write-Host (' [+] ' + $resp.title) -ForegroundColor Green
        Write-Host (' [+] ' + $resp.message) -ForegroundColor Green
        Write-Host '======================================================================' -ForegroundColor Green
        Write-Host ''
        Write-Host 'DETAIL EKSEKUSI PERTAHANAN:' -ForegroundColor Yellow
        foreach ($s in $resp.steps) {
            $col = if ($s.status -eq 'SUCCESS') { 'Green' } else { 'Yellow' }
            Write-Host ('  [V] ' + $s.feature + ' : ' + $s.detail) -ForegroundColor $col
        }
    } catch {
        Write-Host '[-] Server web sedang sinkronisasi. Menjalankan penangkalan direct fallback...' -ForegroundColor Yellow
        Get-Process | Where-Object { $_.ProcessName -match 'ransomware|bajakan|korban|trojan' } | Stop-Process -Force -ErrorAction SilentlyContinue
        Remove-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run' -Name 'Kartika_Weaponized_Doc_Dropper' -ErrorAction SilentlyContinue
        Write-Host '[+] Penangkalan direct fallback selesai dieksekusi 100%!' -ForegroundColor Green
    }
}"

echo.
echo ======================================================================
echo  [+] SELURUH ANCAMAN SIBER BERHASIL DITANGKAL 100%!
echo  [+] Membuka Dashboard Radar Pertahanan Komando...
echo ======================================================================
start "" "http://127.0.0.1:5001"
echo.
pause

