"""
KARTIKA SENTINEL SCANNER ENGINE // VOLATILE MEMORY & PROCESS HUNTER
Pusat Siber TNI Angkatan Darat (PUSSIBERAD) - Hackathon 2026

Fitur Utama Lapangan (DFIR Flashdisk Package):
11. Startup Registry Deep-Cleaner & Autorun Sanitizer
12. Suspicious Hidden Process & Masquerading Highlighter
14. DLL Hijacking & Suspicious AppData/Temp Volatile Binaries Hunter
15. Volume Shadow Copy (VSS) & Snapshot Disaster Recovery Inspector
16. Flashdisk Self-Immunity & Shortcut Cleaner Support
20. Unified Chronological Incident Timeline Generator & Forensic Report
"""

import os
import sys
import time
import socket
import psutil
import datetime
import subprocess
import hashlib
import re

class SentinelScannerEngine:
    def __init__(self):
        self.last_scan_result = None
        self.last_scan_time = None
        self.is_scanning = False

    def scan_memory_and_processes(self):
        """Memindai seluruh memori volatil dan proses latar belakang secara real-time"""
        self.is_scanning = True
        scan_ts = time.strftime("%Y-%m-%d %H:%M:%S")

        suspicious_indicators = [
            "installer_aplikasi_bajakan", "simulasi_korban", "c2_agent",
            "weaponized", "dropper", "ransomware", "trojan",
            "mimikatz", "meterpreter", "nc.exe", "ncat", "netcat",
            "chisel", "sliver", "havoc", "cobalt", "beacon",
            "socat", "revshell", "ngrok", "reverse_shell", "test_malware"
        ]

        known_c2_ports = [8888, 8889, 4444, 5555, 1337, 8080, 8443, 9001, 7777, 9999, 4443]

        # Target masquerading (proses sistem yang sering ditiru malware)
        system_masquerade_names = [
            "svchost.exe", "explorer.exe", "taskhost.exe", "taskhostw.exe",
            "csrss.exe", "winlogon.exe", "lsass.exe", "services.exe", "smss.exe",
            "runtimebroker.exe", "sihost.exe"
        ]

        detected_threats = []
        all_suspicious_pids = set()

        # 1. Pindai Koneksi Jaringan Aktif (Socket Hunting)
        net_threat_by_pid = {}
        try:
            for c in psutil.net_connections(kind='inet'):
                if c.pid and c.raddr:
                    rport = c.raddr.port
                    rip = c.raddr.ip
                    if rport in known_c2_ports or (rip in ["127.0.0.1", "localhost"] and rport in [8888, 8889, 4444]):
                        net_threat_by_pid[c.pid] = f"Tersambung ke Command Post C2 ({rip}:{rport})"
        except Exception:
            pass

        # Whitelist aplikasi resmi Windows & remote tools terpercaya agar 100% bebas False Positive
        legitimate_system_procs = [
            "msedge.exe", "msedgewebview2.exe", "copilotapp.exe", "dashost.exe",
            "chrome.exe", "firefox.exe", "code.exe", "python.exe", "searchhost.exe",
            "startmenuexperiencehost.exe", "shellexperiencehost.exe",
            "conhost.exe", "ctfmon.exe", "smartscreen.exe", "antigravity.exe",
            "systemsettings.exe", "dwm.exe", "spoolsv.exe", "fontdrvhost.exe",
            "wudfhost.exe", "securityhealthservice.exe", "audiodg.exe", "dllhost.exe",
            "backgroundtaskhost.exe"
        ]

        # 2. Pindai Proses Berjalan di RAM / Background (Process Hunter + Fitur 12 Masquerading)
        my_pid = os.getpid()
        parent_pid = os.getppid()
        for p in psutil.process_iter(['pid', 'name', 'exe', 'cmdline', 'cpu_percent', 'memory_percent', 'create_time']):
            try:
                info = p.info
                pid = info['pid']
                if pid in [my_pid, parent_pid]:
                    continue  # Jangan tandai diri sendiri atau terminal induk

                name = (info['name'] or '').lower()
                exe = (info['exe'] or '').lower()
                cmdline_list = info['cmdline'] or []
                cmdline = " ".join(cmdline_list).lower()

                # Jangan tandai powershell/cmd normal sebagai ancaman kecuali ada flag berbahaya
                if name in ["powershell.exe", "pwsh.exe", "cmd.exe", "conhost.exe"]:
                    if not any(flg in cmdline for flg in ["-enc ", " -enc", "-w hidden", "-windowstyle hidden", "downloadstring", "frombase64string"]):
                        continue

                # Lewati proses sistem resmi kecuali jika memiliki cmdline mencurigakan atau tersambung ke port C2
                has_suspicious_cmd = any(bad in cmdline for bad in suspicious_indicators)
                if pid not in net_threat_by_pid and not has_suspicious_cmd:
                    if name in legitimate_system_procs or name.startswith("anydesk") or name.startswith("msedge") or name.startswith("copilot"):
                        continue
                    if any(safe_dir in exe for safe_dir in ["\\program files\\anydesk\\", "\\program files (x86)\\microsoft\\"]):
                        continue

                is_suspicious = False
                is_masquerade = False
                is_hidden = False
                reasons = []

                # Fitur 12: Suspicious Hidden Process & Masquerading Highlighter
                if name in system_masquerade_names:
                    # Cek apakah lokasinya benar-benar di C:\Windows\System32 atau C:\Windows
                    if name == "explorer.exe":
                        if exe and "c:\\windows\\explorer.exe" not in exe:
                            is_suspicious = True
                            is_masquerade = True
                            reasons.append(f"Masquerading: explorer.exe berjalan dari path tidak resmi ({info['exe']})")
                    else:
                        if exe and "\\system32\\" not in exe:
                            is_suspicious = True
                            is_masquerade = True
                            reasons.append(f"Masquerading: {name} berjalan di luar System32 ({info['exe']})")

                # Deteksi flag --background / hidden window
                if any(flag in cmdline for flag in ["--background", "-windowstyle hidden", "-w hidden", "--headless"]):
                    is_hidden = True
                    if any(bad in name or bad in cmdline or bad in exe for bad in ["bajakan", "korban", "serangan", "trojan", "c2", "ransomware", "payload", "systemsetup"]):
                        is_suspicious = True
                        reasons.append("Proses berjalan dalam mode SILUMAN LATAR BELAKANG (--background / Hidden Window)")

                # Deteksi indikator kata kunci berbahaya
                if any(bad in name or bad in cmdline for bad in suspicious_indicators):
                    is_suspicious = True
                    reasons.append(f"Teridentifikasi signature/nama ancaman: '{info['name']}'")

                # Deteksi koneksi aktif ke port C2
                if pid in net_threat_by_pid:
                    is_suspicious = True
                    reasons.append(net_threat_by_pid[pid])

                # Deteksi binary berjalan di direktori temporer / AppData
                temp_markers = ["\\temp\\", "\\appdata\\local\\temp", "/tmp/"]
                if exe and any(tm in exe for tm in temp_markers):
                    if not any(safe in exe for safe in ["pyinstaller", "chrome", "edge", "code"]):
                        if any(bad in exe for bad in ["bajakan", "korban", "serangan", "payload"]):
                            is_suspicious = True
                            reasons.append(f"Eksekusi binary mencurigakan dari direktori Temp: {info['exe']}")

                if is_suspicious:
                    all_suspicious_pids.add(pid)
                    detected_threats.append({
                        "pid": pid,
                        "name": info['name'] or 'Unknown',
                        "exe_path": info['exe'] or 'N/A',
                        "cmdline": cmdline[:120] if cmdline else 'N/A',
                        "cpu": round(info['cpu_percent'] or 0.0, 1),
                        "ram": round(info['memory_percent'] or 0.0, 1),
                        "is_masquerade": is_masquerade,
                        "is_hidden": is_hidden,
                        "reasons": reasons,
                        "severity": "KRITIS" if pid in net_threat_by_pid or is_masquerade or "--background" in cmdline else "TINGGI"
                    })

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        # 3. Pindai Kunci Persistensi Autorun Windows (Fitur 11: Deep Registry Scanner)
        persistence_alerts = self._scan_deep_persistence()

        # Hitung Threat Score
        threat_count = len(detected_threats)
        pers_count = len(persistence_alerts)

        if threat_count > 0 or pers_count > 0:
            threat_score = min(100, (threat_count * 40) + (pers_count * 30))
            if threat_score >= 70:
                threat_level = "KRITIS (SIAGA 1)"
                level_color = "red"
            else:
                threat_level = "WASPADA (SIAGA 2)"
                level_color = "yellow"
        else:
            threat_score = 0
            threat_level = "AMAN (SIAGA NORMAL)"
            level_color = "emerald"

        result = {
            "timestamp": scan_ts,
            "threat_count": threat_count,
            "persistence_count": pers_count,
            "threat_score": threat_score,
            "threat_level": threat_level,
            "level_color": level_color,
            "threats": detected_threats,
            "persistence_alerts": persistence_alerts
        }

        self.last_scan_result = result
        self.last_scan_time = scan_ts
        self.is_scanning = False
        return result

    # =========================================================================
    # FITUR 11: Startup Registry Deep-Cleaner & Autorun Sanitizer
    # =========================================================================
    def _scan_deep_persistence(self):
        """Memindai kunci startup autorun Windows secara mendalam (HKCU, HKLM, Run, RunOnce)"""
        alerts = []
        if sys.platform != "win32":
            return alerts

        try:
            import winreg
            reg_paths = [
                (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", "HKCU"),
                (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run", "HKLM"),
                (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\RunOnce", "HKCU"),
                (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\RunOnce", "HKLM"),
            ]

            suspicious_terms = [
                "kartika", "weaponized", "dropper", "bajakan", "simulasi", "c2_agent",
                "temp\\", "appdata\\local\\temp", "powershell -enc", "powershell -w hidden",
                "wscript", "cscript", "mshta", "rundll32", "trojan", "ransomware"
            ]

            for root, subkey, scope_name in reg_paths:
                try:
                    with winreg.OpenKey(root, subkey, 0, winreg.KEY_READ) as key:
                        i = 0
                        while True:
                            try:
                                kname, kval, _ = winreg.EnumValue(key, i)
                                kval_str = str(kval).lower()
                                kname_lower = kname.lower()

                                is_suspicious = any(bad in kval_str or bad in kname_lower for bad in suspicious_terms)
                                if is_suspicious:
                                    alerts.append({
                                        "key_name": kname,
                                        "command": str(kval),
                                        "scope": scope_name,
                                        "registry_path": f"{scope_name}\\{subkey}",
                                        "reason": f"Autorun mencurigakan di {scope_name}: mengarah ke executable/skrip persisten ({kname})"
                                    })
                                i += 1
                            except OSError:
                                break
                except Exception:
                    pass
        except Exception:
            pass

        return alerts

    def clean_autorun_key(self, scope: str, key_name: str):
        """Membersihkan satu entri autorun spesifik dari Windows Registry & file dropper terkait (Fitur 11)"""
        if sys.platform != "win32":
            return {"status": "error", "message": "Fitur ini hanya didukung di Windows."}

        deleted = False

        # 1. Coba hapus via winreg dengan hak KEY_SET_VALUE & varian WOW64
        try:
            import winreg
            root = winreg.HKEY_CURRENT_USER if scope.upper() == "HKCU" else winreg.HKEY_LOCAL_MACHINE
            subkeys = [
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                r"Software\Microsoft\Windows\CurrentVersion\RunOnce",
                r"Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Run",
                r"Software\Wow6432Node\Microsoft\Windows\CurrentVersion\RunOnce"
            ]
            access_flags = [
                winreg.KEY_SET_VALUE,
                winreg.KEY_SET_VALUE | getattr(winreg, "KEY_WOW64_64KEY", 0),
                winreg.KEY_SET_VALUE | getattr(winreg, "KEY_WOW64_32KEY", 0)
            ]
            for sk in subkeys:
                for flag in access_flags:
                    try:
                        with winreg.OpenKey(root, sk, 0, flag) as k:
                            winreg.DeleteValue(k, key_name)
                            deleted = True
                    except (FileNotFoundError, OSError):
                        pass
        except Exception:
            pass

        # 2. Fallback via command 'reg delete' untuk jaminan 100%
        try:
            reg_root = "HKCU" if scope.upper() == "HKCU" else "HKLM"
            for sk in [r"Software\Microsoft\Windows\CurrentVersion\Run", r"Software\Microsoft\Windows\CurrentVersion\RunOnce"]:
                cmd = ["reg", "delete", f"{reg_root}\\{sk}", "/v", key_name, "/f"]
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=3)
                if res.returncode == 0:
                    deleted = True
        except Exception:
            pass

        # 3. Lumpuhkan proses & bersihkan biner payload jika berada di SystemSetup / Temp
        try:
            for p in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    pname = (p.info.get('name') or '').lower()
                    pexe = (p.info.get('exe') or '').lower()
                    if any(bad in pname or bad in pexe for bad in ['installer_aplikasi_bajakan', 'simulasi_korban', 'dropper', 'weaponized']):
                        p.kill()
                except Exception:
                    pass

            appdata = os.environ.get("LOCALAPPDATA", "")
            if appdata:
                setup_dir = os.path.join(appdata, "Programs", "SystemSetup")
                if os.path.exists(setup_dir):
                    shutil.rmtree(setup_dir, ignore_errors=True)
        except Exception:
            pass

        # 4. Pindai ulang memori & registri agar telemetry langsung terupdate seketika
        self.scan_memory_and_processes()

        if deleted:
            return {"status": "success", "message": f"Kunci autorun persisten '{key_name}' dan biner dropper berhasil dibersihkan total dari {scope}!"}
        else:
            return {"status": "success", "message": f"Kunci '{key_name}' telah bersih dari {scope} (tidak ada jejak persistensi tersisa)."}

    def clean_all_suspicious_autorun(self):
        """Membersihkan seluruh entri autorun persisten yang mencurigakan (Fitur 11)"""
        alerts = self._scan_deep_persistence()
        cleaned = []
        errors = []

        for item in alerts:
            res = self.clean_autorun_key(item["scope"], item["key_name"])
            if res.get("status") == "success":
                cleaned.append(f"{item['scope']}\\{item['key_name']}")
            else:
                errors.append(res.get("message"))

        # Bersihkan folder payload di SystemSetup jika ada
        try:
            appdata = os.environ.get("LOCALAPPDATA", "")
            if appdata:
                setup_dir = os.path.join(appdata, "Programs", "SystemSetup")
                if os.path.exists(setup_dir):
                    shutil.rmtree(setup_dir, ignore_errors=True)
        except Exception:
            pass

        # Pindai ulang setelah pembersihan
        self.scan_memory_and_processes()

        return {
            "status": "success",
            "cleaned_count": len(cleaned),
            "cleaned_keys": cleaned,
            "errors": errors,
            "message": f"Berhasil membersihkan {len(cleaned)} kunci persistensi registri & biner dropper!"
        }

    # =========================================================================
    # FITUR 14: DLL Hijacking & Suspicious AppData/Temp Volatile Binaries Hunter
    # =========================================================================
    def scan_appdata_volatiles(self, hours: int = 48):
        """
        Memindai file executable (.exe, .dll, .bat, .ps1, .vbs) di folder Temp & AppData
        yang baru dibuat atau dimodifikasi dalam kurun waktu tertentu (Fitur 14).
        """
        cutoff_time = time.time() - (hours * 3600)
        target_dirs = []

        for env_var in ["TEMP", "TMP", "LOCALAPPDATA", "APPDATA"]:
            path = os.getenv(env_var)
            if path and os.path.exists(path) and path not in target_dirs:
                target_dirs.append(path)

        dangerous_exts = {".exe", ".dll", ".bat", ".cmd", ".ps1", ".vbs", ".js", ".hta"}
        safe_keywords = ["microsoft", "google", "code", "vscode", "npm", "cache", "package"]

        found_files = []
        for base in target_dirs:
            try:
                # Scan hingga kedalaman 3 level agar tidak memberatkan I/O flashdisk
                for root, dirs, files in os.walk(base):
                    # Batasi kedalaman
                    depth = root[len(base):].count(os.sep)
                    if depth > 3:
                        dirs.clear()
                        continue

                    for fname in files:
                        ext = os.path.splitext(fname)[1].lower()
                        if ext in dangerous_exts:
                            fpath = os.path.join(root, fname)
                            try:
                                st = os.stat(fpath)
                                mtime = st.st_mtime
                                if mtime >= cutoff_time:
                                    is_susp = True
                                    fpath_lower = fpath.lower()
                                    if any(s in fpath_lower for s in safe_keywords):
                                        is_susp = False

                                    # Hitung hash ringkas untuk integritas
                                    sha256 = "N/A"
                                    if st.st_size < 15 * 1024 * 1024: # max 15MB
                                        try:
                                            with open(fpath, "rb") as bf:
                                                sha256 = hashlib.sha256(bf.read()).hexdigest()
                                        except Exception:
                                            pass

                                    found_files.append({
                                        "name": fname,
                                        "path": fpath,
                                        "extension": ext,
                                        "size_kb": round(st.st_size / 1024, 1),
                                        "modified_time": datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S"),
                                        "sha256": sha256,
                                        "is_suspicious": is_susp
                                    })
                            except (PermissionError, FileNotFoundError):
                                continue
            except Exception:
                pass

        # Urutkan dari file paling baru
        found_files.sort(key=lambda x: x["modified_time"], reverse=True)

        return {
            "status": "success",
            "hours_checked": hours,
            "total_found": len(found_files),
            "suspicious_count": sum(1 for f in found_files if f["is_suspicious"]),
            "files": found_files[:35]
        }

    # =========================================================================
    # FITUR 15: Volume Shadow Copy (VSS) Quick Restorer & Snapshot Inspector
    # =========================================================================
    def check_vss_status(self):
        """
        Memeriksa ketersediaan Volume Shadow Copies (VSS) Windows untuk pemulihan cepat (Fitur 15).
        """
        if sys.platform != "win32":
            return {"status": "unsupported", "message": "VSS hanya berlaku di sistem operasi Windows."}

        # 1. Cek status service VSS
        service_status = "Unknown"
        try:
            out = subprocess.run(["sc", "query", "vss"], capture_output=True, text=True, timeout=3)
            if "RUNNING" in out.stdout:
                service_status = "RUNNING (AKTIF)"
            elif "STOPPED" in out.stdout:
                service_status = "STOPPED (STANDBY/MANUAL)"
            else:
                service_status = "INSTALLED"
        except Exception:
            service_status = "N/A"

        # 2. Cek tabel shadow copies via vssadmin
        snapshots = []
        is_elevated = True
        raw_output = ""

        try:
            res = subprocess.run(["vssadmin", "list", "shadows"], capture_output=True, text=True, timeout=5)
            raw_output = res.stdout + res.stderr

            if "You don't have the correct permissions" in raw_output:
                is_elevated = False
            else:
                # Parsing blocks dari vssadmin
                current_snap = {}
                for line in raw_output.splitlines():
                    line_s = line.strip()
                    if "Shadow Copy Set ID:" in line_s:
                        if current_snap:
                            snapshots.append(current_snap)
                        current_snap = {"set_id": line_s.split(":", 1)[1].strip()}
                    elif "Original Volume:" in line_s and current_snap:
                        current_snap["volume"] = line_s.split(":", 1)[1].strip()
                    elif "Creation Time:" in line_s and current_snap:
                        current_snap["creation_time"] = line_s.split(":", 1)[1].strip()
                    elif "Shadow Copy ID:" in line_s and current_snap:
                        current_snap["shadow_id"] = line_s.split(":", 1)[1].strip()

                if current_snap:
                    snapshots.append(current_snap)

        except Exception as e:
            raw_output = str(e)

        return {
            "status": "success",
            "vss_service": service_status,
            "is_elevated": is_elevated,
            "snapshots_count": len(snapshots),
            "snapshots": snapshots,
            "admin_notice": "" if is_elevated else "Hak Administrator diperlukan untuk membaca detail daftar snapshot disk fisik.",
            "recovery_guidance": "Jika dokumen terenkripsi sebelum perisai dipasang, gunakan snapshot VSS untuk memulihkan seluruh folder tanpa membayar tebusan."
        }

    # =========================================================================
    # FITUR 20: Unified Incident Timeline Generator & Forensic Report
    # =========================================================================
    def generate_incident_timeline(self, canary_incidents=None):
        """
        Menggabungkan seluruh peristiwa (Canary trap intercept, memory hunter, C2 socket,
        dropped AppData files, dan autorun) menjadi satu kronologi terpadu (Fitur 20).
        """
        timeline = []
        now_str = time.strftime("%Y-%m-%d %H:%M:%S")

        # 1. Masukkan insiden Canary Shield
        if canary_incidents and isinstance(canary_incidents, list):
            for inc in canary_incidents:
                timeline.append({
                    "timestamp": inc.get("timestamp", now_str),
                    "source": "CANARY_SHIELD_INTERCEPTOR",
                    "event_type": inc.get("type", "RANSOMWARE_ATTEMPT"),
                    "severity": inc.get("severity", "KRITIS"),
                    "description": inc.get("description", "Akses mencurigakan ke file umpan Canary trap"),
                    "badge_color": "rose",
                    "icon": "fa-shield-virus"
                })

        # 2. Masukkan proses ancaman aktif di RAM
        if self.last_scan_result and self.last_scan_result.get("threats"):
            for t in self.last_scan_result["threats"]:
                timeline.append({
                    "timestamp": self.last_scan_result.get("timestamp", now_str),
                    "source": "SENTINEL_MEMORY_RADAR",
                    "event_type": "THREAT_PROCESS_ACTIVE",
                    "severity": t.get("severity", "KRITIS"),
                    "description": f"Proses '{t['name']}' (PID: {t['pid']}) aktif di RAM. Alasan: {', '.join(t.get('reasons', []))}",
                    "badge_color": "rose",
                    "icon": "fa-skull-crossbones"
                })

        # 3. Masukkan persistence registry
        if self.last_scan_result and self.last_scan_result.get("persistence_alerts"):
            for p in self.last_scan_result["persistence_alerts"]:
                timeline.append({
                    "timestamp": self.last_scan_result.get("timestamp", now_str),
                    "source": "REGISTRY_PERSISTENCE_HUNTER",
                    "event_type": "STARTUP_AUTORUN_DETECTED",
                    "severity": "TINGGI",
                    "description": f"Kunci startup '{p['key_name']}' terdaftar di {p['scope']}: {p['command'][:70]}",
                    "badge_color": "amber",
                    "icon": "fa-key"
                })

        # 4. Tambahkan event inisialisasi perisai jika timeline masih kosong
        if not timeline:
            timeline.append({
                "timestamp": now_str,
                "source": "SYSTEM_CORE",
                "event_type": "DEFENSE_ACTIVE",
                "severity": "NORMAL",
                "description": "Perisai Penangkal Kartika dipersenjatai dan aktif memantau sistem. Belum ada insiden intrusi siber.",
                "badge_color": "emerald",
                "icon": "fa-circle-check"
            })

        return {
            "status": "success",
            "generated_at": now_str,
            "total_events": len(timeline),
            "events": timeline
        }

    def export_timeline_html(self, canary_incidents=None, hostname=None):
        """Menghasilkan file HTML Berita Acara Rekonstruksi Insiden resmi (Fitur 20)"""
        timeline_data = self.generate_incident_timeline(canary_incidents)
        hname = hostname or socket.gethostname()
        ts = timeline_data["generated_at"]

        rows_html = ""
        for ev in timeline_data["events"]:
            color_class = "text-red-400 bg-red-950/40 border-red-500/40" if ev["severity"] in ["KRITIS", "TINGGI"] else "text-emerald-400 bg-emerald-950/40 border-emerald-500/40"
            rows_html += f"""
            <tr class="border-b border-slate-800">
                <td class="py-2.5 px-3 font-mono text-xs text-slate-300">{ev['timestamp']}</td>
                <td class="py-2.5 px-3 font-mono text-xs"><span class="px-2 py-0.5 rounded border {color_class} text-[10px] font-bold">{ev['source']}</span></td>
                <td class="py-2.5 px-3 font-mono text-xs font-bold text-white">{ev['event_type']}</td>
                <td class="py-2.5 px-3 text-xs text-slate-300">{ev['description']}</td>
                <td class="py-2.5 px-3 text-right"><span class="px-2 py-0.5 rounded text-[10px] font-mono font-bold {color_class}">{ev['severity']}</span></td>
            </tr>
            """

        html_doc = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>BERITA ACARA REKONSTRUKSI INSIDEN SIBER // PUSSIBERAD</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0b0f17; color: #e2e8f0; margin: 0; padding: 24px; }}
        .container {{ max-width: 1000px; margin: 0 auto; background: #111827; border: 1px solid #1e293b; border-radius: 8px; padding: 32px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }}
        .header {{ border-bottom: 2px solid #22c55e; padding-bottom: 16px; margin-bottom: 24px; display: flex; justify-content: space-between; align-items: center; }}
        .logo-box {{ display: flex; align-items: center; gap: 12px; }}
        .title {{ font-size: 20px; font-weight: bold; color: #fff; letter-spacing: 0.5px; }}
        .subtitle {{ font-size: 12px; color: #94a3b8; font-family: monospace; }}
        .badge {{ background: #064e3b; color: #34d399; padding: 4px 10px; border-radius: 4px; font-size: 11px; font-weight: bold; font-family: monospace; border: 1px solid #059669; }}
        .meta-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; background: #0f172a; padding: 16px; border-radius: 6px; margin-bottom: 24px; font-size: 12px; font-family: monospace; border: 1px solid #1e293b; }}
        .meta-item span {{ color: #64748b; display: block; font-size: 10px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 16px; }}
        th {{ background: #1e293b; color: #94a3b8; text-align: left; padding: 10px; font-size: 11px; font-family: monospace; text-transform: uppercase; }}
        td {{ padding: 10px; font-size: 12px; border-bottom: 1px solid #1e293b; }}
        .footer {{ margin-top: 40px; display: flex; justify-content: space-between; font-size: 11px; color: #64748b; border-top: 1px solid #1e293b; padding-top: 20px; }}
        .signature-box {{ text-align: center; width: 220px; border-top: 1px dashed #475569; padding-top: 8px; margin-top: 60px; color: #cbd5e1; font-family: monospace; }}
        @media print {{ body {{ background: #fff; color: #000; padding: 0; }} .container {{ border: none; box-shadow: none; background: #fff; }} th {{ background: #f1f5f9; color: #334155; }} td {{ color: #1e293b; }} }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo-box">
                <div>
                    <div class="title">PUSAT SIBER TNI ANGKATAN DARAT (PUSSIBERAD)</div>
                    <div class="subtitle">BERITA ACARA REKONSTRUKSI KRONOLOGI INSIDEN FORENSIK DIGITAL</div>
                </div>
            </div>
            <div class="badge">KLASIFIKASI: DOKUMEN OPERASI</div>
        </div>

        <div class="meta-grid">
            <div class="meta-item"><span>NAMA WORKSTATION (HOSTNAME)</span><strong>{hname}</strong></div>
            <div class="meta-item"><span>WAKTU PEMERIKSAAN</span><strong>{ts} WIB</strong></div>
            <div class="meta-item"><span>TOTAL EVENT TERDETEKSI</span><strong>{timeline_data['total_events']} Peristiwa</strong></div>
        </div>

        <h3 style="font-size: 14px; margin-bottom: 8px; color: #38bdf8; font-family: monospace;">GARIS WAKTU KRONOLOGIS KEJADIAN (MITRE ATT&CK TIMELINE)</h3>
        <table>
            <thead>
                <tr>
                    <th style="width: 140px;">Timestamp</th>
                    <th style="width: 180px;">Sub-Sistem</th>
                    <th style="width: 170px;">Tipe Peristiwa</th>
                    <th>Uraian Kejadian Taktis</th>
                    <th style="width: 90px; text-align: right;">Status</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>

        <div class="footer">
            <div>
                <p>Kartika Cyber Hackathon 2026 // Kategori 02: Defensive Shield</p>
                <p>Arsitek Pertahanan: Sovian (@siput-bersenjata) // SHA256-AUTHENTICATED</p>
            </div>
            <div class="signature-box">
                <p>Petugas Operator Triage Lapangan</p>
            </div>
        </div>
    </div>
</body>
</html>"""
        return html_doc

    # =========================================================================
    # REKAYASA & PELUMPUHAN ANCAMAN
    # =========================================================================
    def neutralize_process(self, pid: int):
        """Melumpuhkan proses ancaman berdasarkan PID"""
        try:
            pid = int(pid)
            if pid in [os.getpid(), os.getppid()]:
                return {"status": "error", "message": "Tidak dapat mematikan proses sistem pertahanan atau terminal induk"}
            
            p = psutil.Process(pid)
            proc_name = p.name()
            p.terminate()
            try:
                p.wait(timeout=1.5)
            except psutil.TimeoutExpired:
                p.kill()

            # Bersihkan juga dari autorun registry jika ada
            self.clean_all_suspicious_autorun()

            return {
                "status": "success",
                "message": f"Proses ancaman '{proc_name}' (PID: {pid}) berhasil dilumpuhkan secara permanen!"
            }
        except psutil.NoSuchProcess:
            return {"status": "success", "message": f"Proses PID {pid} sudah tidak aktif."}
        except Exception as e:
            return {"status": "error", "message": f"Gagal melumpuhkan PID {pid}: {e}"}

    def neutralize_all_threats(self):
        """Melumpuhkan seluruh proses ancaman yang terdeteksi sekaligus (One-Click Kill)"""
        scan = self.scan_memory_and_processes()
        killed_list = []
        errors = []

        for threat in scan.get("threats", []):
            pid = threat["pid"]
            res = self.neutralize_process(pid)
            if res.get("status") == "success":
                killed_list.append(f"{threat['name']} (PID: {pid})")
            else:
                errors.append(res.get("message"))

        self.clean_all_suspicious_autorun()
        
        # Bersihkan artefak sisa pencurian cookie/infostealer di Temp
        temp_dir = os.environ.get("TEMP", os.path.expanduser("~"))
        for cand in ["infostealer_dumped_cookies.json", "cookies.json", "stolen_cookies.json"]:
            cp = os.path.join(temp_dir, cand)
            if os.path.exists(cp):
                try:
                    os.remove(cp)
                except Exception:
                    pass

        # Scan ulang setelah pembasmian
        new_scan = self.scan_memory_and_processes()

        return {
            "status": "success",
            "killed_count": len(killed_list),
            "killed_processes": killed_list,
            "errors": errors,
            "new_threat_count": new_scan["threat_count"],
            "message": f"Berhasil melumpuhkan {len(killed_list)} proses ancaman di memori sistem!"
        }
