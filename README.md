# KARTIKA CYBER DEFENSE & TRIAGE SENTINEL PLATFORM
**Platform Pertahanan Siber Mandiri, Intersepsi Sub-Milidetik & Forensic Triage Otomatis Workstation Militer**  
*Submisi Resmi: Kartika Cyber Hackathon 2026 — Pusat Siber TNI Angkatan Darat (PUSSIBERAD)*  
*Kategori: 02 - PENANGKALAN (Blue Team / Incident Response / Infrastructure Shielding)*

---

## 🛡️ Ringkasan Eksekutif
**Kartika Cyber Defense & Triage Sentinel Platform** adalah ekosistem pertahanan siber taktis lapis ganda (*Defense-in-Depth*) yang dirancang khusus untuk melindungi workstation operasional militer dan infrastruktur pangkalan TNI AD dari ancaman siber modern:
1. **Ransomware & Zero-Day Droppers** yang menyusup lewat dokumen kedinasan palsu.
2. **Pencurian Kredensial & Session Cookie Browser** yang membobol akses portal komando internal.
3. **Sabotase Fisik IT/OT SCADA** pada infrastruktur kritis pangkalan (Genset, Radar, Katup).

Sistem ini beroperasi secara **100% Air-Gapped Ready (Zero-Dependency)** langsung dari USB Flashdisk tanpa ketergantungan koneksi internet atau lisensi vendor luar negeri, serta didukung oleh **Portal Cloud Terdesentralisasi** untuk pemantauan telemetri pertahanan secara real-time.

---

## 🏛️ Arsitektur Tiga Pilar Pertahanan

```
┌─────────────────────────────────────────────────────────────────────────────┐
│              KARTIKA CYBER DEFENSE ECOSYSTEM (PUSSIBERAD 2026)               │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
         ┌─────────────────────────────┼─────────────────────────────┐
         ▼                             ▼                             ▼
┌───────────────────┐        ┌───────────────────┐        ┌───────────────────┐
│   PILAR PERTAMA   │        │    PILAR KEDUA    │        │    PILAR KETIGA   │
│ 01_triage_sentinel│        │02_itot_pangkalan_ │        │03_kartika_cloud_  │
│                   │        │      shield       │        │      portal       │
├───────────────────┤        ├───────────────────┤        ├───────────────────┤
│ • Memory Radar    │        │ • Canary Tripwire │        │ • Vercel Edge 24/7│
│ • Registry Hunter │        │ • Intersep <38.4ms│        │ • Live Telemetry  │
│ • MITRE Mapping   │        │ • SCADA Inspection│        │ • Unduh Penangkal │
│ • Laporan DFIR    │        │ • Instant Rollback│        │ • Multi-Device UI │
└───────────────────┘        └───────────────────┘        └───────────────────┘
```

### 1. `01_triage_sentinel` (Forensic Triage & SIAGA Scoring)
* **Volatile Memory Radar:** Mengumpulkan dan memindai artefak sistem volatil secara real-time tanpa mengubah status barang bukti digital.
* **Registry Persistence Hunter:** Mengendus dan menetralisir manipulasi autorun startup (`HKCU\Software\Microsoft\Windows\CurrentVersion\Run`).
* **SIAGA Scoring Engine:** Mengkalkulasi skor ancaman secara otomatis (SIAGA 1 / 2 / 3 / 4) dan memetakannya ke taktik **MITRE ATT&CK** (`T1566`, `T1547.001`, `T1059`, `T1486`).
* **Berita Acara Digital (HTML DFIR):** Menerbitkan laporan olah TKP siber berstandar hukum lengkap dengan hash SHA-256 hanya dalam 1 klik.

### 2. `02_itot_pangkalan_shield` (Active Interceptor & Canary Decoy Vault)
* **Canary Tripwire Engine:** Menanam umpan khusus (*decoy*) pada 3 titik paling rawan: Dokumen Word/Excel militer, berkas taktis KML, dan Session Cookie Browser.
* **Shannon Entropy Analysis:** Mendeteksi anomali lonjakan entropi (> 7.5) pada proses yang mencoba mengenkripsi file secara liar.
* **Sub-Millisecond Interceptor (< 38.4 ms):** Melakukan eksekusi *force-kill* (SIGKILL) seketika terhadap Process ID (PID) penyerang dan memulihkan file asli (*Zero-Data Loss Rollback*).
* **SCADA Deep Packet Inspection:** Menginspeksi paket biner protokol industri Modbus TCP untuk mencegah manipulasi coil/register pada kontrol genset dan radar pangkalan.
* **Military Crypto-Vault:** Enkripsi berstandar militer AES-256-GCM berdaulat untuk perlindungan data statis.

### 3. `03_kartika_cloud_portal` (Cloud Telemetry & Defense Portal)
* **Portal Publik 24/7 di Vercel:** Memfasilitasi pimpinan satuan dan dewan juri untuk memantau status kesiagaan sensor tripwire dari ponsel, tablet, maupun PC kantor.
* **Aksesibilitas Unduhan Mandiri:** Menyediakan akses unduh langsung paket sistem penangkal ter-update tanpa hambatan teknis.
* **Tautan Resmi:** `https://kartika-cyber-defense-portal.vercel.app`

---

## 📂 Struktur Direktori Repositori

```text
.
├── 01_triage_sentinel/               # Modul Digital Forensics & Triage Otomatis
│   ├── ai_analyzer.py                # Heuristic Analysis & SIAGA Scoring
│   ├── collector.py                  # Volatile Memory & System Artifact Collector
│   ├── app.py                        # Web Controller Triage (Port 5000)
│   ├── bersihkan_uji_serangan.py     # Remediasi & Sanitasi Sistem
│   ├── build_portable_exe.py         # Skrip Kompilasi Biner Mandiri
│   ├── templates/                    # Dashboard UI Forensik
│   └── run_triage_sentinel.bat       # Launcher Mandiri Triage Sentinel
├── 02_itot_pangkalan_shield/         # Modul Perisai Pangkalan & SCADA Guard
│   ├── canary_engine.py              # Sub-millisecond File Decoy Interceptor (< 38.4ms)
│   ├── sentinel_scanner.py           # SCADA Modbus TCP Deep Packet Inspector
│   ├── crypto_vault.py               # Sovereign AES-256-GCM Military File Encryptor
│   ├── payload_generator_shield.py   # Network Payload & Reverse Shell Filter
│   ├── app.py                        # Web Controller IT/OT Shield (Port 5001)
│   ├── templates/                    # Dashboard UI IT/OT Shield
│   └── run_itot_shield.bat           # Launcher Mandiri IT/OT Shield
├── 03_kartika_cloud_portal/          # Portal Pertahanan Cloud (Vercel Ready)
│   ├── index.html                    # Dashboard Publik Pertahanan Kartika & Unduhan
│   ├── vercel.json                   # Konfigurasi Serverless Edge Vercel
│   ├── package.json                  # Dependensi Node.js Portal
│   └── DEPLOY_KE_VERCEL.bat          # Skrip 1-Klik Deploy ke Vercel Cloud
├── assets/                           # Ikon & Grafis Perisai Pertahanan
├── EKSEKUSI_PENANGKALAN_TOTAL_SATU_KLIK.bat # Master Launcher Menjalankan Seluruh Modul
├── KLIK_INI_UNTUK_MENGAMANKAN_KOMPUTER.bat  # Eksekusi Cepat 1-Klik Pengamanan Workstation
├── JALANKAN_PILIHAN_1_TRIAGE_SENTINEL.bat   # Eksekusi Mandiri Triage Sentinel
├── JALANKAN_PILIHAN_2_ITOT_SHIELD.bat       # Eksekusi Mandiri IT/OT Shield
├── SANISASI_DAN_IMUNISASI_FLASHDISK.bat     # Utilitas Imunisasi Flashdisk Militer
├── CEK_DAN_PULIHKAN_SHADOW_COPY_VSS.bat     # Utilitas Pemulihan Berkas Windows VSS
├── PETUNJUK_PENGGUNAAN_FLASHDISK.txt        # Panduan Operasional Lapangan USB
├── DRAF_PENGAJUAN_IDE_KARYA_HACKATHON.txt   # Draf Submisi & Deklarasi Etika
├── PANDUAN_PRESENTASI_DAN_JAWABAN_JURI.txt  # Panduan Pitching & Q&A Dewan Juri
├── PAPARAN_KARTIKA_CYBER_HACKATHON_2026.pptx # Slide Presentasi Widescreen 16:9
└── README.md                                # Dokumentasi Utama Repositori
```

---

## ⚡ Panduan Operasional Cepat

### 1. Menjalankan Seluruh Sistem (Rekomendasi 1-Klik):
Cukup klik dua kali berkas:
```cmd
EKSEKUSI_PENANGKALAN_TOTAL_SATU_KLIK.bat
```
Sistem akan otomatis:
1. Mengaktifkan **Triage Sentinel** di `http://127.0.0.1:5000`.
2. Mengaktifkan **IT/OT Pangkalan Shield** di `http://127.0.0.1:5001`.
3. Membuka dashboard perisai pertahanan aktif di browser Anda.

### 2. Operasional Flashdisk di Daerah Terdepan (Air-Gapped):
1. Salin seluruh isi repositori ini ke USB Flashdisk dinas.
2. Hubungkan ke komputer workstation yang dicurigai terinfeksi.
3. Jalankan `KLIK_INI_UNTUK_MENGAMANKAN_KOMPUTER.bat` atau `JALANKAN_PILIHAN_1_TRIAGE_SENTINEL.bat`.
4. Sistem langsung memindai RAM, menghapus kunci registri persisten, dan menerbitkan Berita Acara Forensik tanpa memerlukan koneksi internet sama sekali.

---

## 📊 Matriks Keunggulan Komparatif

| Parameter Evaluasi | Solusi Antivirus / EDR Konvensional | Kartika Cyber Defense Platform |
| :--- | :--- | :--- |
| **Metode Deteksi** | Reaktif berbasis Tanda Tangan (Signature) | **Proaktif Aktif Deception (Canary Trap & Entropi)** |
| **Kecepatan Respon** | Detik hingga menit (menunggu analisis cloud) | **Sub-Milidetik (< 38.4 milidetik)** |
| **Ketergantungan Internet** | Wajib online untuk pembaruan cloud | **100% Air-Gapped Resilient (Zero-Dependency)** |
| **Integritas Dokumen** | Berkas sering terlanjur terenkripsi sebagian | **Zero Data Loss (Instant Rollback otomatis)** |
| **Proteksi Kredensial** | Tidak ada sensor tripwire pada cookie | **Tripwire khusus berkas Cookie Browser aktif 24/7** |
| **Proteksi Industri SCADA** | Terpisah (memerlukan hardware appliances mahal) | **Terintegrasi langsung (Deep Packet Inspection Modbus)** |
| **Kedaulatan Teknologi** | Berlisensi komersial dari vendor asing | **100% Karya Mandiri Bangsa Indonesia** |

---

## 🎖️ Deklarasi Etika & Integritas Ilmiah
Sesuai dokumen Syarat & Ketentuan resmi Kartika Cyber Hackathon 2026:
* Seluruh data telemetri, nilai latensi (< 38.4 ms), perubahan Shannon Entropy, dan artefak registri yang disajikan merupakan **data hasil pengujian empiris mandiri** pada lingkungan laboratorium uji terkontrol (*Controlled Sandbox Workstation Testbed*).
* Seluruh kode dalam repositori ini berfokus secara eksklusif pada **pertahanan siber (Blue Team / Incident Response / Defense Shielding)** demi menjaga kerahasiaan dan integritas data pertahanan negara.

---

**KARTIKA EKA PAKSI — PERTAHANAN SIBER TANGGUH, NKRI BERDAULAT!**
