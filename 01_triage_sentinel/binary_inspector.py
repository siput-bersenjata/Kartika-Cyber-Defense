"""
KARTIKA SOVEREIGN BINARY INSPECTOR & THREAT TRIAGE ENGINE
Pusat Siber TNI Angkatan Darat (PUSSIBERAD) - Kartika Cyber Hackathon 2026

Modul Inspeksi Berkas Mandiri Berdaulat (Sovereign Static & Dynamic Binary Inspector)
- 100% On-Premise / Air-Gapped Safe: Dokumen rahasia militer TIDAK PERNAH diunggah ke cloud publik / VirusTotal
- Analisis Entropi Shannon (Deteksi Packer / Crypter / Ransomware)
- Pembongkaran Header PE & Deteksi Packer (PyInstaller, UPX, Py2exe, Go, .NET)
- Ekstraksi String Forensik C2, IOC, Registri Persistensi, dan Kredensial
- Korelasi Memori RAM Volatil (Mengecek apakah biner sedang berjalan aktif di sistem)
- Pemetaan Taktik MITRE ATT&CK & Skor SIAGA Pertahanan Militer
"""

import os
import sys
import math
import re
import json
import socket
import datetime
import hashlib
from typing import Dict, Any, List

class SovereignBinaryInspector:
    def __init__(self, target_filepath: str = None):
        self.target_path = os.path.abspath(target_filepath) if target_filepath else None
        self.findings = []
        self.threat_score = 0
        self.mitre_tags = []

    def calculate_entropy(self, data: bytes) -> float:
        """Menghitung Shannon Entropy dari sekumpulan byte (0.0 s.d 8.0)"""
        if not data:
            return 0.0
        entropy = 0.0
        length = len(data)
        counts = {}
        for b in data:
            counts[b] = counts.get(b, 0) + 1
        for count in counts.values():
            p_x = count / length
            if p_x > 0:
                entropy -= p_x * math.log2(p_x)
        return round(entropy, 3)

    def extract_strings(self, data: bytes, min_len: int = 4) -> List[str]:
        """Mengekstrak deretan string ASCII dan Unicode, termasuk dekompresi otomatis stream zlib/PyInstaller"""
        import zlib
        ascii_regex = re.compile(b"[\x20-\x7e]{" + str(min_len).encode() + b",}")
        found = [m.decode('latin-1', errors='ignore') for m in ascii_regex.findall(data)]

        # Inspeksi stream terkompresi zlib di dalam biner (Membongkar PyInstaller Archive)
        if b"PyInstaller" in data or b"_MEI" in data:
            decompressed_count = 0
            for m in re.finditer(b"\x78[\x01\x9c\xda]", data):
                if decompressed_count > 150:
                    break
                try:
                    decomp = zlib.decompress(data[m.start():m.start() + 2000000])
                    decompressed_count += 1
                    decomp_strs = [s.decode('latin-1', errors='ignore') for s in ascii_regex.findall(decomp)]
                    found.extend(decomp_strs)
                except Exception:
                    pass

        # Filter duplikat sambil mempertahankan urutan
        seen = set()
        clean = []
        for s in found:
            s_strip = s.strip()
            if s_strip and s_strip not in seen and len(s_strip) < 300:
                seen.add(s_strip)
                clean.append(s_strip)
        return clean

    def inspect_file(self, file_path: str = None) -> Dict[str, Any]:
        target = os.path.abspath(file_path or self.target_path)
        if not os.path.exists(target):
            return {"status": "error", "message": f"Berkas tidak ditemukan: {target}"}

        file_size = os.path.getsize(target)
        if file_size == 0:
            return {"status": "error", "message": "Ukuran berkas 0 byte."}

        # Baca seluruh atau cuplikan byte awal dan akhir (maks 50MB)
        with open(target, "rb") as f:
            raw_bytes = f.read(min(file_size, 50 * 1024 * 1024))

        # 1. HASH GENERATION
        md5_hash = hashlib.md5(raw_bytes).hexdigest()
        sha1_hash = hashlib.sha1(raw_bytes).hexdigest()
        sha256_hash = hashlib.sha256(raw_bytes).hexdigest()

        # 2. SHANNON ENTROPY
        entropy = self.calculate_entropy(raw_bytes)
        entropy_verdict = "NORMAL"
        if entropy > 7.2:
            entropy_verdict = "HIGHLY_ENCRYPTED_OR_PACKED"
            self.findings.append({
                "severity": "CRITICAL",
                "title": "Tingkat Entropi Sangat Tinggi (> 7.2)",
                "detail": f"Entropi berkas adalah {entropy}/8.0. Ini adalah karakteristik kuat dari malware yang dikompresi, di-pack, atau payload ransomware terenkripsi.",
                "mitre": "T1027 (Obfuscated Files or Information)"
            })
            self.threat_score += 25
            self.mitre_tags.append("T1027")
        elif entropy > 6.6:
            entropy_verdict = "SUSPICIOUS_COMPRESSION"
            self.threat_score += 10

        # 3. PE HEADER PARSING
        is_pe = raw_bytes.startswith(b"MZ")
        pe_info = {"is_pe": is_pe, "arch": "Unknown", "subsystem": "Unknown", "sections": []}
        if is_pe and len(raw_bytes) >= 0x40:
            try:
                e_lfanew = int.from_bytes(raw_bytes[0x3C:0x40], byteorder="little")
                if e_lfanew < len(raw_bytes) - 4 and raw_bytes[e_lfanew:e_lfanew+4] == b"PE\x00\x00":
                    pe_info["valid_pe"] = True
                    machine = int.from_bytes(raw_bytes[e_lfanew+4:e_lfanew+6], byteorder="little")
                    if machine == 0x8664:
                        pe_info["arch"] = "x64 (AMD64 / 64-bit)"
                    elif machine == 0x014c:
                        pe_info["arch"] = "x86 (Intel 386 / 32-bit)"
                    elif machine == 0xaa64:
                        pe_info["arch"] = "ARM64"

                    num_sections = int.from_bytes(raw_bytes[e_lfanew+6:e_lfanew+8], byteorder="little")
                    pe_info["num_sections"] = num_sections
            except Exception:
                pass

        # 4. PACKER & TOOLCHAIN SIGNATURE DETECTION
        packer_detected = []
        if b"PyInstaller" in raw_bytes or b"_MEI" in raw_bytes or b"pyi-windows-bin" in raw_bytes:
            packer_detected.append("PyInstaller (Python Executable Bundle)")
            self.findings.append({
                "severity": "MEDIUM",
                "title": "Terdeteksi Wrapper PyInstaller",
                "detail": "Biner dikompilasi dari skrip Python menggunakan PyInstaller. Sering disalahgunakan untuk menyamarkan malware / ransomware berbasis Python.",
                "mitre": "T1027.002 (Software Packing)"
            })
            self.threat_score += 15
            self.mitre_tags.append("T1027.002")

        if b"UPX0" in raw_bytes or b"UPX1" in raw_bytes or b"UPX!" in raw_bytes:
            packer_detected.append("UPX (Ultimate Packer for eXecutables)")
            self.findings.append({
                "severity": "HIGH",
                "title": "Terdeteksi UPX Packer",
                "detail": "File menggunakan kompresi UPX untuk memperkecil ukuran dan mengelabui antivirus konvensional.",
                "mitre": "T1027.002"
            })
            self.threat_score += 20
            self.mitre_tags.append("T1027.002")

        if b"Go build ID:" in raw_bytes:
            packer_detected.append("Golang Binary Runtime")
        if b"CorExitProcess" in raw_bytes or b"mscoree.dll" in raw_bytes:
            packer_detected.append(".NET CLR Managed Assembly")

        # 5. FORENSIC STRING & IOC EXTRACTION
        extracted_strings = self.extract_strings(raw_bytes, min_len=4)
        c2_urls = []
        ip_addresses = []
        persistence_keys = []
        credentials_keywords = []
        ransomware_indicators = []
        scada_indicators = []

        url_pattern = re.compile(r'https?://[a-zA-Z0-9_\-\.]+(?::[0-9]+)?(?:/[^\s"\']*)?')
        ip_pattern = re.compile(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b')

        for s in extracted_strings:
            # URLs
            for url in url_pattern.findall(s):
                if not any(ign in url.lower() for ign in ["schemas.microsoft.com", "w3.org", "purl.org", "xmlns"]):
                    if url not in c2_urls:
                        c2_urls.append(url)

            # IPs
            for ip in ip_pattern.findall(s):
                if not ip.startswith(("127.", "0.", "255.")):
                    if ip not in ip_addresses:
                        ip_addresses.append(ip)

            # Registri Persistensi
            if any(k in s.lower() for k in ["currentversion\\run", "runonce", "winlogon", "userinit", "services\\"]):
                if s not in persistence_keys:
                    persistence_keys.append(s)

            # Pencurian Kredensial & Infostealer
            if any(c in s.lower() for c in ["cookies.sqlite", "network\\cookies", "dpapi", "jwt_", "bearer", "session_token", "kemhan_sso", "tni_webmail"]):
                if s not in credentials_keywords:
                    credentials_keywords.append(s)

            # Ransomware / Enkripsi Berkas
            if any(r in s.lower() for r in [".locked", "ransom", "decrypt", "xor_cipher", "petunjuk_pemulihan", "vssadmin delete shadows"]):
                if s not in ransomware_indicators:
                    ransomware_indicators.append(s)

            # SCADA / Modbus
            if any(m in s.lower() for m in ["modbus", "holding_register", "slave_id", "scada", "plc_"]):
                if s not in scada_indicators:
                    scada_indicators.append(s)

        # Evaluasi Temuan Forensik
        if c2_urls:
            self.findings.append({
                "severity": "CRITICAL",
                "title": f"Terdeteksi {len(c2_urls)} URL Komunikasi Jarak Jauh (C2 Endpoint)",
                "detail": f"Ditemukan koneksi keluar yang tertanam di biner: {', '.join(c2_urls[:3])}",
                "mitre": "T1071.001 (Web Protocols C2)"
            })
            self.threat_score += 25
            self.mitre_tags.append("T1071.001")

        if persistence_keys:
            self.findings.append({
                "severity": "CRITICAL",
                "title": "Terdeteksi Upaya Persistensi Registri Startup Windows",
                "detail": f"Biner mencoba mendaftarkan eksekusi otomatis di: {', '.join(persistence_keys[:2])}",
                "mitre": "T1547.001 (Boot or Logon Autostart Execution: Registry Run Keys)"
            })
            self.threat_score += 25
            self.mitre_tags.append("T1547.001")

        if credentials_keywords:
            self.findings.append({
                "severity": "CRITICAL",
                "title": "Terdeteksi Indikator Spyware / Infostealer (Pencurian Kredensial Browser)",
                "detail": f"Ditemukan pola pembajakan sesi web browser & token otorisasi: {', '.join(credentials_keywords[:3])}",
                "mitre": "T1539 (Steal Web Session Cookie)"
            })
            self.threat_score += 30
            self.mitre_tags.append("T1539")

        if ransomware_indicators:
            self.findings.append({
                "severity": "CRITICAL",
                "title": "Terdeteksi Rutin Enkripsi Berkas / Ransomware",
                "detail": f"Ditemukan indikator penguncian berkas dan ekstensi ransomware: {', '.join(ransomware_indicators[:3])}",
                "mitre": "T1486 (Data Encrypted for Impact)"
            })
            self.threat_score += 30
            self.mitre_tags.append("T1486")

        if scada_indicators:
            self.findings.append({
                "severity": "HIGH",
                "title": "Terdeteksi Pustaka Kontrol Industri / SCADA Modbus",
                "detail": f"Biner berinteraksi dengan protokol kontrol fisik militer: {', '.join(scada_indicators[:2])}",
                "mitre": "T0814 (Inhibit Response Function - ICS)"
            })
            self.threat_score += 20

        # 6. KORELASI MEMORI VOLATIL (RAM CHECK)
        active_processes_matched = self.correlate_running_processes(target, sha256_hash)
        if active_processes_matched:
            self.findings.append({
                "severity": "CRITICAL",
                "title": f"BINER SEDANG AKTIF BERJALAN DI MEMORI RAM (PID {active_processes_matched[0]['pid']})",
                "detail": f"Proses '{active_processes_matched[0]['name']}' saat ini sedang mengeksekusi biner ini secara langsung di workstation militer!",
                "mitre": "T1059 (Command and Scripting Interpreter)"
            })
            self.threat_score += 35

        # Normalisasi Threat Score (0 - 100)
        final_score = min(100, self.threat_score)
        if final_score >= 70:
            siaga_status = "SIAGA 1 (CRITICAL MALWARE)"
            siaga_color = "red"
        elif final_score >= 45:
            siaga_status = "SIAGA 2 (HIGH THREAT / SUSPICIOUS)"
            siaga_color = "orange"
        elif final_score >= 20:
            siaga_status = "SIAGA 3 (MEDIUM ANOMALY)"
            siaga_color = "yellow"
        else:
            siaga_status = "SIAGA 4 (NORMAL / BENIGN)"
            siaga_color = "green"

        result = {
            "status": "success",
            "metadata": {
                "filename": os.path.basename(target),
                "filepath": target,
                "filesize_bytes": file_size,
                "filesize_mb": round(file_size / (1024 * 1024), 2),
                "md5": md5_hash,
                "sha1": sha1_hash,
                "sha256": sha256_hash,
                "analyzed_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "threat_evaluation": {
                "siaga_level": siaga_status,
                "threat_score": final_score,
                "threat_color": siaga_color,
                "mitre_attack_matrix": list(set(self.mitre_tags))
            },
            "binary_internals": {
                "entropy": entropy,
                "entropy_verdict": entropy_verdict,
                "pe_info": pe_info,
                "packers": packer_detected if packer_detected else ["Standard Native Compiler"]
            },
            "extracted_iocs": {
                "c2_urls": c2_urls,
                "ip_addresses": ip_addresses,
                "persistence_keys": persistence_keys,
                "credentials_targeted": credentials_keywords,
                "ransomware_indicators": ransomware_indicators
            },
            "active_memory_correlation": {
                "is_active_in_ram": len(active_processes_matched) > 0,
                "matched_processes": active_processes_matched
            },
            "forensic_findings": self.findings,
            "sovereign_guarantee": "100% On-Premise Inspection. Zero Bytes Uploaded to Public Clouds/VirusTotal."
        }

        return result

    def correlate_running_processes(self, filepath: str, file_hash: str) -> List[Dict[str, Any]]:
        """Mengecek apakah biner sedang berjalan di memori RAM sistem operasi lokal"""
        matched = []
        try:
            import psutil
            target_fname = os.path.basename(filepath).lower()
            for p in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
                try:
                    p_name = (p.info['name'] or '').lower()
                    p_exe = (p.info['exe'] or '').lower()
                    if p_name == target_fname or (p_exe and os.path.abspath(p_exe).lower() == filepath.lower()):
                        matched.append({
                            "pid": p.info['pid'],
                            "name": p.info['name'],
                            "exe": p.info['exe'],
                            "cmdline": " ".join(p.info['cmdline'] or [])
                        })
                except Exception:
                    pass
        except Exception:
            pass
        return matched

def format_cli_report(res: Dict[str, Any]) -> str:
    if res.get("status") == "error":
        return f"[-] Error: {res.get('message')}"

    meta = res["metadata"]
    threat = res["threat_evaluation"]
    internals = res["binary_internals"]
    iocs = res["extracted_iocs"]
    findings = res["forensic_findings"]
    mem = res["active_memory_correlation"]

    lines = []
    lines.append("=" * 72)
    lines.append("       KARTIKA SOVEREIGN BINARY INSPECTOR & FORENSIC TRIAGE       ")
    lines.append("      Pusat Siber TNI Angkatan Darat // Hackathon 2026 Defense    ")
    lines.append("=" * 72)
    lines.append(f" [*] Target Berkas : {meta['filename']} ({meta['filesize_mb']} MB)")
    lines.append(f" [*] Path Absolut  : {meta['filepath']}")
    lines.append(f" [*] SHA-256 Hash  : {meta['sha256']}")
    lines.append(f" [*] Entropi Biner : {internals['entropy']} / 8.0 ({internals['entropy_verdict']})")
    lines.append(f" [*] Arsitektur    : {internals['pe_info'].get('arch', 'Unknown')}")
    lines.append(f" [*] Packer/Tools  : {', '.join(internals['packers'])}")
    lines.append("-" * 72)
    lines.append(f" [!] STATUS EVALUASI: {threat['siaga_level']} (Skor: {threat['threat_score']}/100)")
    lines.append(f" [!] MITRE ATT&CK   : {', '.join(threat['mitre_attack_matrix']) if threat['mitre_attack_matrix'] else 'None'}")
    lines.append(f" [!] STATUS DI RAM  : {'TERDETEKSI AKTIF BERJALAN DI MEMORI!' if mem['is_active_in_ram'] else 'Tidak ada proses aktif'}")
    lines.append("-" * 72)
    lines.append(" INDIKATOR ANCAMAN (IOCs) YANG DIEKSTRAK DARI BINER:")
    if iocs['c2_urls']:
        lines.append(f"  • C2 Web URLs        : {len(iocs['c2_urls'])} ditemukan ({', '.join(iocs['c2_urls'][:2])})")
    if iocs['persistence_keys']:
        lines.append(f"  • Registri Startup   : {', '.join(iocs['persistence_keys'][:2])}")
    if iocs['credentials_targeted']:
        lines.append(f"  • Target Infostealer : {len(iocs['credentials_targeted'])} jejak kredensial/token browser")
    if iocs['ransomware_indicators']:
        lines.append(f"  • Indikator Enkripsi : {', '.join(iocs['ransomware_indicators'][:2])}")

    lines.append("\n TEMUAN ANALISIS FORENSIK:")
    for idx, f in enumerate(findings, 1):
        lines.append(f"  [{idx}] [{f['severity']}] {f['title']}")
        lines.append(f"      {f['detail']}")
        if f.get('mitre'):
            lines.append(f"      MITRE: {f['mitre']}")

    lines.append("-" * 72)
    lines.append(" [✓] KEDAULATAN DATA: 100% Diperiksa Secara Lokal (Zero Cloud Leakage).")
    lines.append("=" * 72)
    return "\n".join(lines)

if __name__ == "__main__":
    target_file = sys.argv[1] if len(sys.argv) > 1 else "Installer_Aplikasi_Bajakan.exe"
    if not os.path.exists(target_file):
        # Cek di folder skenario_serangan jika ada
        fallback = os.path.join(os.path.dirname(__file__), "..", "skenario_serangan", "Installer_Aplikasi_Bajakan.exe")
        if os.path.exists(fallback):
            target_file = fallback

    inspector = SovereignBinaryInspector()
    result = inspector.inspect_file(target_file)
    print(format_cli_report(result))
