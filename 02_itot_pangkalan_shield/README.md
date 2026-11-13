# KARTIKA CANARY-SHIELD & MILITARY CRYPTO-VAULT
**Sovereign Active Deception, Sub-50ms Zero-Day Ransomware Interceptor & Military AES-256-GCM Vault**  
*Pusat Siber TNI Angkatan Darat (PUSSIBERAD) - Kartika Cyber Hackathon 2026*  
**Kategori 02: DEFENSIVE SHIELD (Penangkalan)**  
*Sub-kategori Resmi Web:* **Encryption Tool**, **Automated Incident Response**, **Zero-Day Detection**

---

## 1. Latar Belakang & Urgensi Militer (TNI AD)

Dokumen kedinasan satuan dan pos komando taktis militer (seperti **Surat Perintah Operasi .docx**, **Daftar Distribusi Amunisi Alutsista .xlsx**, dan **Peta Taktis Operasi Perbatasan .kml**) adalah aset bernilai strategis tinggi. 

Satuan dihadapkan pada dua ancaman nyata:
1. **Pencurian Fisik / Data At-Rest:** Laptop jatuh ke tangan lawan atau dicuri dari pos perbatasan.
2. **Sabotase Ransomware Militer (MITRE ATT&CK T1486):** Penyerang menyusupkan malware pemeras/penghancur dokumen saat jam genting operasi militer. Antivirus konvensional sering **gagal mendeteksi ransomware jenis baru (*Zero-Day*)** karena belum tersedianya signature.

**KARTIKA CANARY-SHIELD & MILITARY CRYPTO-VAULT** menjawab kedua ancaman ini dengan pendekatan *Dual-Layer Defense*:
- **Layer 1 (Encryption Tool):** Enkripsi berstandar militer **AES-256-GCM** dengan otentikasi Galois/Counter Mode untuk melindungi dokumen saat istirahat (*at-rest*).
- **Layer 2 (Automated Response & Zero-Day Interceptor):** Menempatkan *Canary Traps* (file umpan bertanda khusus). Jika ada ransomware mencoba menyentuh atau mengenkripsi file umpan ini, sistem otomatis **menembak mati (*Force Kill*) PID proses penyerang dalam < 50 milidetik** sebelum sempat menyentuh dokumen dinas asli prajurit.

---

## 2. Fitur Utama & Keunggulan Teknis

### A. Sovereign Military Crypto-Vault (AES-256-GCM)
- Standar enkripsi simetris terkuat: **AES-256-GCM** dengan 128-bit Authentication Tag.
- Key Derivation: **PBKDF2-HMAC-SHA256 (100.000 Iterasi)** dari sandi otorisasi komandan.
- Format kontainer militer: `.milvault` (melindungi integritas, jika ada 1 byte diubah musuh, proses dekripsi langsung menolak).
- Menghapus berkas plaintext asli secara aman dari disk setelah dienkripsi.

### B. Active Canary Deception Engine (Zero-Day Detection)
- Memasang sensor umpan strategis pada urutan abjad teratas:
  - `!00_CANARY_RENOPS_RAHASIA.docx` (sensor berkas Word)
  - `!00_CANARY_PETA_DISPOSISI.kml` (sensor berkas peta koordinat)
- Pemantau I/O berkas berkecepatan tinggi (30ms high-frequency integrity check).
- Deteksi anomali: Shannon Entropy Anomaly, modifikasi ekstensi, perubahan hash/ukuran seketika.

### C. Zero-Second Automated Incident Response
- **Force Kill PID:** Begitu file umpan disentuh proses asing, sistem mencari PID proses penyerang di level OS Windows dan melakukan terminasi paksa (*kill*) dalam waktu rata-rata **< 50 ms**.
- **Automated Rollback:** Mengembalikan integritas file umpan canary seketika dari memori baseline.
- **Isolasi Jaringan (Network Severing):** Memutus soket C2 penyerang agar exfiltrasi data batal.
- **Forensic Audit Trail:** Mencatat log insiden lengkap (PID, nama proses, perintah command-line, waktu insiden, dan teknik MITRE ATT&CK) untuk laporan perwira siber.

---

## 3. Struktur Berkas Sistem

```
02_itot_pangkalan_shield/
│
├── app.py                      # Flask Web Dashboard & Orchestrator API (Port 5001)
├── canary_engine.py            # Engine Pemantau I/O, Canary Deception & Auto-Kill PID
├── crypto_vault.py             # Engine Enkripsi/Dekripsi Militer AES-256-GCM (.milvault)
├── run_itot_shield.bat         # Batch launcher lokal
│
└── templates/
    └── index.html              # Antarmuka Web Cyber Operations Center (HUD Taktis)
```

---

## 4. Cara Menjalankan & Skenario Uji di Hadapan Juri

### Langkah 1: Jalankan Dashboard
Klik ganda file:
`JALANKAN_PILIHAN_2_ITOT_SHIELD.bat` (atau `JALANKAN_PILIHAN_2_CANARY_SHIELD.bat`)

Dashboard taktis otomatis terbuka di browser: **http://127.0.0.1:5001**

### Langkah 2: Tunjukkan Dokumen Militer Asli Terbuka Normal
- Buka folder: `skenario_serangan/01_serangan_dokumen_ransomware/sandbox_dokumen_militer/`
- Buka `Daftar_Distribusi_Amunisi_Kodam.xlsx` di Microsoft Excel -> **Terbuka sempurna dengan tabel amunisi resmi**.
- Buka `Surat_Telegram_Panglima_TNI_042.docx` di Microsoft Word -> **Terbuka sempurna dengan kop surat dinas**.

### Langkah 3: Uji Enkripsi Militer (Military Crypto-Vault)
1. Di Dashboard, klik tombol **"KUNCI VAULT (ENKRIPSI)"**.
2. Dokumen di folder langsung terenkripsi menjadi kontainer militer `.milvault`.
3. Buka file `.milvault` -> Data 100% terkunci dengan AES-256-GCM.
4. Klik **"BUKA VAULT (DEKRIPSI)"** -> Dokumen kembali normal.

### Langkah 4: Uji Pertahanan Serangan Ransomware Nyata (Canary Interceptor)
1. Pastikan status Canary-Shield adalah **"ARMED (AKTIF)"**.
2. Klik tombol merah di dashboard: **"UJI SERANG RANSOMWARE NYATA"** (atau jalankan `ransomware_agent.py` / picu dari C2).
3. **Hasil Seketika (< 50 milidetik):**
   - Muncul peringatan merah taktis:  
     `ANCAMAN ZERO-DAY RANSOMWARE BERHASIL DILUMPUHKAN (< 38 ms)!`
   - Log forensik mencatat PID proses penyerang yang di-kill seketika.
   - Buka folder dokumen di hadapan juri: **Seluruh dokumen asli prajurit (Excel & Word) 100% AMAN, UTUH, dan TIDAK TERKUNCI!**

---

## 5. Fitur Pengujian Dinamis (Folder Kustom / Dokumen Panitia)

Untuk memenuhi tantangan panitia mengenai pengujian fleksibel pada berbagai folder komputer:
1. **Target Folder Bebas**: Dapat menguji folder manapun di PC (misal: `Desktop`, `Documents`, `Downloads`, atau folder dokumen yang disiapkan khusus oleh juri).
2. **Pengubahan via C2 Remote Console**:
   - Di modal *File Manager Dokumen*, masukkan path folder target di input **DIREKTORI TARGET SERANGAN** atau klik tombol preset (`SANDBOX`, `DESKTOP`, `DOCUMENTS`, `DOWNLOADS`).
   - Klik **PINDAH DIREKTORI TARGET**. Agen korban seketika beralih membaca dan menargetkan folder tersebut secara remote!
3. **Pengubahan via Canary-Shield Dashboard**:
   - Di panel atas dashboard `http://127.0.0.1:5001`, masukkan path folder pada input **DIREKTORI PROTEKSI AKTIF** atau klik preset yang sama.
   - Klik **Terapkan Proteksi**. Sensor canary trap langsung dipasang di folder tersebut dan siap mencegat serangan ransomware secara sub-50ms!

---

## 6. Pemetaan MITRE ATT&CK & Relevansi TNI AD

| Komponen Sistem | Teknik MITRE ATT&CK | Relevansi Kebutuhan TNI AD |
| :--- | :--- | :--- |
| **Canary Trap Sensor** | T1059 (Scripting Execution) / T1566 | Deteksi infiltrasi ransomware zero-day |
| **Force-Kill Interceptor** | M1040 (Behavior Prevention) | Menghentikan sabotase data sebelum rusak |
| **AES-256-GCM Vault** | M1041 (Encrypt Sensitive Information) | Melindungi dokumen rahasia saat laptop dicuri |
| **Digital Forensic Feed** | DS0009 (Process Creation & Memory) | Bukti investigasi digital PUSSIBERAD |

Dokumentasi disiapkan oleh Tim Pengembang untuk PUSSIBERAD Kartika Cyber Hackathon 2026.

