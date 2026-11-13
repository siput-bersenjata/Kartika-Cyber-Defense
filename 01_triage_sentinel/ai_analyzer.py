"""
KARTIKA TRIAGE SENTINEL - Offline & Sovereign AI Incident Analyzer
Menghubungkan hasil triage dengan Local LLM (Ollama) secara offline, 
dengan fallback cerdas ke Expert Heuristic Engine berstandar doktrin militer TNI AD.
"""

import requests
import json

class TacticalAIAnalyzer:
    def __init__(self, ollama_url="http://localhost:11434", model="llama3.2"):
        self.ollama_url = ollama_url
        self.model = model

    def is_ollama_available(self):
        try:
            res = requests.get(f"{self.ollama_url}/api/tags", timeout=1.5)
            return res.status_code == 200
        except Exception:
            return False

    def generate_analysis(self, triage_data):
        """Menganalisis data artefak dan menghasilkan laporan intelijen taktis"""
        if self.is_ollama_available():
            try:
                return self._analyze_with_ollama(triage_data)
            except Exception as e:
                return self._expert_rule_fallback(triage_data, note=f"Ollama error: {str(e)}")
        else:
            return self._expert_rule_fallback(triage_data, note="Air-Gapped Sovereign Rule Engine (Ollama Standby)")

        cred_theft = triage_data.get("credential_theft", {})
        prompt = f"""
Anda adalah Perwira Ahli Forensik Siber PUSSIBERAD TNI AD.
Analisis data temuan triage artefak siber berikut:
Hostname: {triage_data['summary']['hostname']}
Skor Ancaman: {triage_data['threat_score']} / 100 ({triage_data['status_level']})
Proses Mencurigakan: {len(triage_data['processes']['suspicious_processes'])}
Koneksi Jaringan Mencurigakan: {len(triage_data['network']['suspicious_connections'])}
Titik Persistensi Mencurigakan: {triage_data['persistence']['suspicious_count']}
Artefak Ekstraksi Kredensial/Cookie (T1539): {len(cred_theft.get('artifacts', []))}

Daftar Temuan Kritis:
{json.dumps(triage_data['processes']['suspicious_processes'], indent=2)}
{json.dumps(triage_data['network']['suspicious_connections'], indent=2)}
{json.dumps(cred_theft.get('artifacts', []), indent=2)}

Berikan kesimpulan taktis militer dalam Bahasa Indonesia yang mencakup:
1. Ringkasan Eksekutif untuk Komandan Satuan (1 paragraf tegas).
2. Pemetaan Taktik MITRE ATT&CK (seperti Steal Web Session Cookie T1539, Persistence, Command and Control).
3. Langkah Tindakan Taktis Segera (Urgent Containment Actions) yang harus dilakukan prajurit di lokasi.
"""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        res = requests.post(f"{self.ollama_url}/api/generate", json=payload, timeout=25)
        if res.status_code == 200:
            result = res.json()
            return {
                "engine": f"Local LLM ({self.model})",
                "status": "Success",
                "analysis_text": result.get("response", "").strip()
            }
        else:
            return self._expert_rule_fallback(triage_data, note="Ollama response code error")

    def _expert_rule_fallback(self, triage_data, note=""):
        score = triage_data.get("threat_score", 0)
        susp_procs = triage_data['processes']['suspicious_processes']
        susp_conns = triage_data['network']['suspicious_connections']
        susp_persist = triage_data['persistence']['suspicious_count']
        cred_theft = triage_data.get("credential_theft", {})

        findings_summary = []
        mitre_tactics = []
        containment_steps = []

        # Deteksi spesifik jika insiden melibatkan Weaponized Document / Targeted Ransomware
        is_ransomware = any(
            any(w in str(p).lower() for w in ["ransomware", "dropper", "weaponized", "locked"])
            for p in susp_procs
        ) or any("weaponized" in str(it).lower() or "ransomware" in str(it).lower() for it in triage_data['persistence']['items'])

        # Deteksi spesifik jika insiden melibatkan Infostealer / Pencurian Cookie Sesi Browser
        has_cookie_theft = cred_theft.get("detected", False) or any(
            any(w in str(p).lower() for w in ["cookie", "infostealer", "stealer", "lumma", "redline"])
            for p in susp_procs
        )

        if score >= 70:
            if has_cookie_theft and is_ransomware:
                exec_summary = (
                    f"PERINGATAN KRITIS MAKSIMAL (SIAGA 1): Workstation {triage_data['summary']['hostname']} "
                    f"terkonfirmasi disusupi KOMBINASI SERANGAN DOKUMEN BERACUN, RANSOMWARE, DAN INFOSTEALER (T1539). "
                    f"Terdeteksi ekstraksi session token browser militer aktif (Kemhan SSO / TNI Webmail) bersamaan dengan "
                    f"upaya penyanderaan arsip kedinasan via C2 controller. Penyerang berpotensi mem-bypass MFA dan membajak akun komando!"
                )
                mitre_tactics = [
                    {"id": "T1539", "name": "Credential Access: Steal Web Session Cookie", "desc": "Pencurian cookie sesi web browser aktif prajurit untuk membypass autentikasi MFA (Session Hijacking)."},
                    {"id": "T1555.003", "name": "Credential Access: Credentials from Web Browsers", "desc": "Eksfiltrasi berkas database profil browser pengguna (Network\\Cookies / DPAPI Master Key)."},
                    {"id": "T1486", "name": "Impact: Data Encrypted for Impact", "desc": "Instruksi eksekusi penguncian/enkripsi file dokumen strategis dari jarak jauh."},
                    {"id": "T1571", "name": "Command and Control: Remote C2 Beaconing", "desc": "Agen terhubung ke server pengendali C2 untuk menerima instruksi eksfiltrasi data."},
                    {"id": "T1547.001", "name": "Persistence: Registry Run Keys", "desc": "Dropper memasang kunci autorun agar aktif kembali saat workstation dinyalakan."}
                ]
                containment_steps = [
                    "SEGERA lakukan REVOKE SESSION (cabut seluruh sesi dan token aktif) pada Identity Provider SSO Kemhan, TNI Webmail, dan Portal E-Office Kodam!",
                    "Putuskan kabel LAN dan matikan Wi-Fi (Physical Air-Gapping) untuk mencegah transmisi C2 lebih lanjut.",
                    "Lakukan force-logout identitas pengguna dari server pusat IdP militer.",
                    "JANGAN matikan daya listrik mendadak untuk mempertahankan memori volatil RAM.",
                    "Blokir IP/domain server C2 pengendali di gateway firewall perimeter pangkalan."
                ]
            elif has_cookie_theft:
                exec_summary = (
                    f"PERINGATAN KRITIS (SIAGA 1): Workstation {triage_data['summary']['hostname']} "
                    f"terdeteksi menjadi korban SERANGAN INFOSTEALER & PENCURIAN COOKIE SESI BROWSER (MITRE T1539). "
                    f"Artefak token autentikasi kedinasan telah diekstrak ke disk volatil dan berpotensi dieksfiltrasi ke C2. "
                    f"Sesi komando militer terancam dibajak tanpa perlu mengetahui password prajurit."
                )
                mitre_tactics = [
                    {"id": "T1539", "name": "Credential Access: Steal Web Session Cookie", "desc": "Pencurian token sesi web browser aktif untuk membypass proteksi MFA."},
                    {"id": "T1555.003", "name": "Credential Access: Credentials from Web Browsers", "desc": "Pembacaan direktori SQLite profil browser pengguna."},
                    {"id": "T1041", "name": "Exfiltration: Exfiltration Over C2 Channel", "desc": "Pengiriman paket kredensial curian ke server komando penyerang."}
                ]
                containment_steps = [
                    "SEGERA REVOKE token sesi pengguna di konsol IdP / SSO Kemhan dan Portal TNI.",
                    "Hapus cache dan cookie tersimpan di browser Google Chrome, Microsoft Edge, dan Mozilla Firefox.",
                    "Putuskan koneksi internet dan isolasi workstation dari jaringan dinas.",
                    "Ganti kredensial komando dari perangkat terpisah yang aman dan aktifkan FIDO2 Hardware Key."
                ]
            elif is_ransomware:
                exec_summary = (
                    f"PERINGATAN KRITIS (SIAGA 1): Workstation {triage_data['summary']['hostname']} "
                    f"terindikasi kuat terinfeksi SERANGAN DOKUMEN BERACUN & TARGETED RANSOMWARE (APT). "
                    f"Terdeteksi proses dropper yang mengeksekusi payload pengunci file dokumen kedinasan dan "
                    f"membuka jalur kontrol jarak jauh (C2 Remote Controller). Arsip dokumen strategis terancam disandera."
                )
                mitre_tactics = [
                    {"id": "T1566.001", "name": "Initial Access: Spearphishing Attachment", "desc": "Penyusupan melalui umpan berkas kedinasan palsu (PDF/Word/Image beracun)."},
                    {"id": "T1486", "name": "Impact: Data Encrypted for Impact", "desc": "Instruksi eksekusi penguncian/enkripsi file dokumen strategis dari jarak jauh."},
                    {"id": "T1571", "name": "Command and Control: Remote C2 Beaconing", "desc": "Agen terhubung ke server pengendali C2 untuk menerima perintah penguncian file."},
                    {"id": "T1547.001", "name": "Persistence: Registry Run Keys", "desc": "Dropper memasang kunci autorun agar aktif kembali saat workstation dinyalakan."}
                ]
                containment_steps = [
                    "SEGERA cabut kabel LAN dan putuskan koneksi Wi-Fi (Physical Air-Gapping) agar enkripsi tidak merembet ke Shared Drive / Server Komando Kodam.",
                    "Blokir segera IP/Port C2 pengendali di gateway firewall pangkalan militer.",
                    "JANGAN matikan daya listrik mendadak untuk mempertahankan kunci volatil di memori RAM.",
                    "Gunakan modul cadangan offline (air-gapped backup) untuk merestorasi dokumen yang terkunci."
                ]
            else:
                exec_summary = (
                    f"PERINGATAN TINGKAT TINGGI (SIAGA 1): Workstation {triage_data['summary']['hostname']} "
                    f"terindikasi kuat telah disusupi oleh malware spionase / Advanced Persistent Threat (APT). "
                    f"Ditemukan {len(susp_procs)} proses anomali yang berjalan secara tersembunyi dan koneksi keluar "
                    f"ke port kontrol tak berizin. Integritas data komando satuan terancam."
                )
                mitre_tactics = [
                    {"id": "T1036.005", "name": "Defense Evasion: Masquerading", "desc": "Proses berbahaya menyamar menggunakan nama proses sistem Windows resmi."},
                    {"id": "T1571", "name": "Command and Control: Non-Standard Port", "desc": "Koneksi jaringan keluar aktif ke port kontrol umum botnet (port 4444/5555/8888)."},
                    {"id": "T1547.001", "name": "Persistence: Registry Run Keys", "desc": "Payload disematkan pada registry autorun agar aktif kembali saat reboot."}
                ]
                containment_steps = [
                    "SEGERA cabut kabel LAN dan nonaktifkan adapter Wi-Fi/Bluetooth pada mesin ini (Physical Air-Gapping).",
                    "JANGAN matikan daya listrik secara mendadak agar bukti volatil di memori RAM tidak hilang.",
                    "Lakukan isolasi port pada switch pangkalan militer untuk IP node ini.",
                    "Ganti segera kredensial dinas (username & password akun komando) dari perangkat terpisah yang aman."
                ]
        elif score >= 35:
            exec_summary = (
                f"PERINGATAN MENENGAH (SIAGA 2): Terdeteksi beberapa indikasi perilaku anomali pada "
                f"workstation {triage_data['summary']['hostname']}. Belum ditemukan aktivitas C2 aktif secara masif, "
                f"namun terdapat proses atau berkas sementara yang mencurigakan memerlukan karantina."
            )
            mitre_tactics = [
                {"id": "T1059.001", "name": "Execution: Command and Scripting Interpreter", "desc": "Eksekusi skrip dari direktori volatil/temp pengguna."},
                {"id": "T1082", "name": "Discovery: System Information Discovery", "desc": "Pemeriksaan profil sistem dan koneksi jaringan."}
            ]
            containment_steps = [
                "Lakukan karantina proses yang mencurigakan ke dalam sandbox pengawasan.",
                "Periksa integritas berkas di direktori Temp dan AppData pengguna.",
                "Tingkatkan logging audit di firewall pangkalan untuk lalu lintas dari node ini."
            ]
        else:
            exec_summary = (
                f"KONDISI NORMAL (HIJAU): Workstation {triage_data['summary']['hostname']} berada dalam "
                f"kondisi aman. Tidak ditemukan proses berisiko tinggi, koneksi C2 ilegal, maupun manipulasi registry autorun. "
                f"Sistem siap digunakan untuk aktivitas operasional dinas."
            )
            mitre_tactics = [
                {"id": "N/A", "name": "Normal Operations Baseline", "desc": "Semua artefak berada dalam batas wajar sistem resmi."}
            ]
            containment_steps = [
                "Lanjutkan pemantauan berkala sesuai SOP pengamanan siber satuan.",
                "Pastikan media USB yang masuk tetap disanitasi di Kiosk sebelum digunakan."
            ]

        formatted_report = f"""
### 1. RINGKASAN EKSEKUTIF KOMANDAN SATUAN
{exec_summary}

---

### 2. PEMETAAN TAKTIK & TEKNIK MITRE ATT&CK
"""
        for t in mitre_tactics:
            formatted_report += f"- **[{t['id']}] {t['name']}**: {t['desc']}\n"

        formatted_report += """
---

### 3. TINDAKAN TAKTIS SEGERA DI LAPANGAN (IMMEDIATE MITIGATION)
"""
        for i, step in enumerate(containment_steps, 1):
            formatted_report += f"{i}. {step}\n"

        return {
            "engine": f"Sovereign Expert Engine ({note})",
            "status": "Success",
            "analysis_text": formatted_report.strip(),
            "mitre_tactics": mitre_tactics,
            "containment_steps": containment_steps
        }
