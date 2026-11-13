# KARTIKA TRIAGE SENTINEL
**Tactical Air-Gapped Cyber Incident & Forensics Triage Kit**
*Kategori 03: Dukungan Teknologi (Core Infra) — Kartika Cyber Hackathon 2026 (PUSSIBERAD)*

---

## 📌 Latar Belakang & Urgensi Militer
Di lingkungan satuan jajaran TNI AD (Kodam, Korem, Kodim, hingga pos perbatasan/Satgas Pamtas), insiden siber pada komputer workstation seringkali tidak dapat ditangani cepat karena:
1. Satuan daerah tidak memiliki personel bersertifikasi Digital Forensik.
2. Jaringan bersifat *air-gapped* atau ber-bandwidth rendah, sehingga artefak tidak boleh diunggah ke cloud publik luar negeri.
3. Keterlambatan respon berisiko menghilangkan artefak volatil di RAM dan merusak rantai komando.

**KARTIKA TRIAGE SENTINEL** adalah perangkat triage forensik portabel berstandar operasional militer. Alat ini mengekstrak artefak sistem dalam hitungan detik, lalu mengaktifkan **Local AI Engine** yang bekerja 100% *air-gapped* untuk menyajikan laporan intelijen berbahasa Indonesia, pemetaan **MITRE ATT&CK**, dan instruksi penanganan taktis segera kepada komandan satuan.

---

## ⚙️ Fitur Utama
- **Air-Gapped Artifact Extractor:** Mengumpulkan proses aktif, socket jaringan C2, registri persistensi, dan pemakaian memori secara volatil.
- **Sovereign Local AI Intelligence:** Terintegrasi dengan model LLM lokal (Ollama / Llama / Qwen) dengan fallback otomatis ke *Expert Heuristic Rule Engine*.
- **Tactical Command HUD:** Antarmuka web militer dengan indikator radar status ancaman real-time.
- **Instant Official Incident Report:** Format laporan intelijen standar PUSSIBERAD yang siap dicetak (*Print/PDF ready*).
- **One-Click Demo Simulator:** Tombol bawaan untuk mensimulasikan insiden APT (masquerading svchost, C2 beaconing, dan registry persistence) untuk keperluan demonstrasi ke dewan juri.

---

## 🚀 Panduan Menjalankan Sistem

### 1. Prasyarat:
Pastikan Python 3.10+ sudah terpasang.
```bash
pip install flask psutil requests
```

### 2. Menjalankan Dashboard:
```bash
cd 01_triage_sentinel
python app.py
```
Buka browser di: **http://127.0.0.1:5000**

### 3. Skenario Demonstrasi di Depan Juri:
1. Buka dashboard. Awalnya sistem membaca komputer Anda dalam status normal / baseline.
2. Klik tombol **"Simulasi Infeksi Demo"** (atau biarkan sistem memindai anomali sistem asli).
3. Klik **"JALANKAN TRIAGE SEKARANG"**.
4. Dalam beberapa detik, dashboard berubah menjadi **MERAH (SIAGA 1)**:
   - Terdeteksi proses anomali `svchost_update.exe`.
   - Terdeteksi koneksi keluar C2 port 4444.
   - Terdeteksi malicious run key registry.
5. Tunjukkan tab **"Laporan Analisis Taktis AI"** yang langsung menyusun analisis MITRE ATT&CK dan 4 langkah mitigasi lapangan.
6. Klik **"Cetak Laporan"** untuk menunjukkan kesiapan dokumen komando.
