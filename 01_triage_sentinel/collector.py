"""
KARTIKA TRIAGE SENTINEL - Real Forensic Collector Engine
Mengumpulkan 100% data nyata dari sistem operasi Windows/Linux tanpa simulasi/dummy.
"""

import os
import sys
import psutil
import socket
import datetime
import hashlib
import platform

class ForensicCollector:
    def __init__(self):
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.hostname = socket.gethostname()
        self.os_info = f"{platform.system()} {platform.release()} ({platform.architecture()[0]})"

    def get_system_summary(self):
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        cpu_usage = psutil.cpu_percent(interval=0.3)
        memory = psutil.virtual_memory()
        
        return {
            "hostname": self.hostname,
            "os": self.os_info,
            "scan_time": self.timestamp,
            "uptime_since": boot_time,
            "cpu_usage_pct": cpu_usage,
            "ram_used_gb": round(memory.used / (1024**3), 2),
            "ram_total_gb": round(memory.total / (1024**3), 2),
            "ram_percent": memory.percent
        }

    def collect_processes(self):
        """Memindai seluruh proses yang benar-benar aktif di sistem operasi secara real-time"""
        process_list = []
        suspicious_processes = []

        # Daftar tanda bahaya nyata (Known Threat Signatures & Heuristics)
        suspicious_indicators = [
            "mimikatz", "meterpreter", "nc.exe", "ncat", "netcat", 
            "chisel", "payload", "trojan", "wiper", "backdoor", 
            "c2_agent", "reverse_shell", "test_malware", "svchost_update",
            "sliver", "havoc", "cobalt", "beacon", "socat", "rubeus", 
            "bloodhound", "sharphound", "seatbelt", "winpeas", "linpeas",
            "revshell", "impacket", "ligolo", "ngrok", "ransomware",
            "dropper", "weaponized", "infostealer", "stealer", "cookie",
            "lumma", "redline", "vidar"
        ]

        # Pola argumen command line credential dumping & lateral movement
        cred_dump_patterns = [
            "sekurlsa", "minidump", "comsvcs.dll", "lsass", "sam", "system.save",
            "ntds.dit", "procdump", "rundll32.exe comsvcs", "network\\cookies",
            "cookies.sqlite", "login data", "dpapi"
        ]

        for p in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'exe', 'cmdline', 'create_time']):
            try:
                info = p.info
                name = (info['name'] or '').lower()
                exe = (info['exe'] or '').lower()
                cmdline = " ".join(info['cmdline'] or []).lower()

                is_suspicious = False
                reasons = []

                # 1. Cek kecocokan nama proses atau perintah dengan pola ancaman
                if any(bad in name or bad in cmdline for bad in suspicious_indicators):
                    is_suspicious = True
                    reasons.append(f"Teridentifikasi pola nama/argumen ancaman siber: '{info['name']}'")

                # 2. Cek upaya Credential Harvesting / LSASS Dumping
                if any(patt in cmdline for patt in cred_dump_patterns):
                    is_suspicious = True
                    reasons.append("Terdeteksi upaya ekstraksi kredensial memori (Credential Harvesting / LSASS)")

                # 3. Cek Masquerading proses sistem palsu di luar direktori Windows resmi
                if any(m in name for m in ["svchost", "taskhost", "csrss", "winlogon", "lsass"]):
                    if exe and "system32" not in exe:
                        is_suspicious = True
                        reasons.append(f"Masquerading: {info['name']} berjalan di luar System32 ({info['exe']})")
                elif "explorer" in name and exe and "c:\\windows\\explorer.exe" not in exe:
                    is_suspicious = True
                    reasons.append(f"Masquerading: explorer.exe berjalan dari direktori tidak resmi ({info['exe']})")

                # 4. Cek eksekusi proses dari direktori Temp atau AppData pengguna
                temp_paths = ["\\temp\\", "\\appdata\\local\\temp", "/tmp/", "/var/tmp/", "\\public\\"]
                if exe and any(t in exe for t in temp_paths):
                    if not any(safe in exe for safe in ["installer", "setup", "update"]):
                        is_suspicious = True
                        reasons.append(f"Eksekusi binary dari direktori volatil/temp pengguna: {info['exe']}")

                # 5. Cek PowerShell/CMD dengan encoded command atau hidden window (LOLBAS)
                if "powershell" in name and any(flag in cmdline for flag in ["-enc", "-encodedcommand", "-w hidden", "-windowstyle hidden"]):
                    is_suspicious = True
                    reasons.append("PowerShell menjalankan perintah tersamar (Hidden/Encoded Command - LOLBAS)")

                item = {
                    "pid": info['pid'],
                    "name": info['name'] or 'Unknown',
                    "user": info['username'] or 'SYSTEM',
                    "cpu": round(info['cpu_percent'] or 0.0, 1),
                    "memory": round(info['memory_percent'] or 0.0, 1),
                    "path": info['exe'] or (cmdline[:80] if cmdline else 'N/A'),
                    "is_suspicious": is_suspicious,
                    "reasons": reasons
                }

                if is_suspicious:
                    suspicious_processes.append(item)
                process_list.append(item)

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        # Urutkan berdasarkan PID dan penggunaan CPU
        process_list.sort(key=lambda x: (not x['is_suspicious'], -x['cpu']))

        return {
            "total_processes": len(process_list),
            "suspicious_count": len(suspicious_processes),
            "suspicious_processes": suspicious_processes,
            "processes_sample": process_list[:50]
        }

    def collect_network_connections(self):
        """Memindai koneksi socket TCP/UDP yang benar-benar aktif di sistem operasi"""
        connections = []
        suspicious_conns = []

        # Port umum C2, Reverse Shell, dan backdoor yang sering digunakan aktor APT
        known_c2_ports = [4444, 5555, 1337, 8080, 8443, 8888, 6667, 31337, 9001, 8081, 7777, 9999, 4443]

        # Daftar proses interpreter skrip yang janggal jika membuka koneksi socket
        suspicious_net_procs = ["powershell.exe", "cmd.exe", "cscript.exe", "wscript.exe", "mshta.exe", "nc.exe", "ncat.exe", "netcat.exe"]

        try:
            for c in psutil.net_connections(kind='inet'):
                laddr = f"{c.laddr.ip}:{c.laddr.port}" if c.laddr else "N/A"
                raddr = f"{c.raddr.ip}:{c.raddr.port}" if c.raddr else "N/A"

                is_suspicious = False
                reasons = []

                remote_port = c.raddr.port if c.raddr else None
                local_port = c.laddr.port if c.laddr else None

                # Ambil info proses yang memiliki koneksi ini
                proc_name = "N/A"
                proc_exe = ""
                if c.pid:
                    try:
                        proc = psutil.Process(c.pid)
                        proc_name = proc.name()
                        proc_exe = (proc.exe() or "").lower()
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        proc_name = "System/Protected"

                # 1. Cek port C2 terkenal
                if remote_port and remote_port in known_c2_ports:
                    is_suspicious = True
                    reasons.append(f"Koneksi aktif keluar mengarah ke port kontrol C2 ({remote_port})")

                if local_port and local_port in known_c2_ports and c.status == psutil.CONN_LISTEN:
                    is_suspicious = True
                    reasons.append(f"Port C2/Reverse Shell lokal dalam status LISTEN terbuka ({local_port})")

                # 2. Cek jika proses skrip/interpreter membuka koneksi jaringan aktif
                if any(sp in proc_name.lower() for sp in suspicious_net_procs):
                    is_suspicious = True
                    reasons.append(f"Proses skrip/CLI '{proc_name}' membuka koneksi jaringan (Indikasi Reverse Shell)")

                # 3. Cek jika binary di direktori Temp/AppData membuka koneksi keluar
                if proc_exe and any(tp in proc_exe for tp in ["\\temp\\", "\\appdata\\local\\temp", "/tmp/"]):
                    is_suspicious = True
                    reasons.append(f"Binary volatil di Temp ({proc_name}) berkomunikasi di jaringan")

                conn_item = {
                    "fd": c.fd,
                    "family": "IPv4" if c.family == socket.AF_INET else "IPv6",
                    "type": "TCP" if c.type == socket.SOCK_STREAM else "UDP",
                    "local_address": laddr,
                    "remote_address": raddr,
                    "status": c.status,
                    "pid": c.pid or "-",
                    "proc_name": proc_name,
                    "is_suspicious": is_suspicious,
                    "reasons": reasons
                }

                if is_suspicious:
                    suspicious_conns.append(conn_item)
                connections.append(conn_item)

        except (psutil.AccessDenied, PermissionError):
            pass

        # Dahulukan koneksi yang mencurigakan di daftar
        connections.sort(key=lambda x: not x['is_suspicious'])

        return {
            "total_connections": len(connections),
            "suspicious_count": len(suspicious_conns),
            "suspicious_connections": suspicious_conns,
            "connections_sample": connections[:40]
        }

    def collect_persistence(self):
        """Memindai registri startup Windows nyata (HKCU & HKLM Run Keys)"""
        persistence_items = []

        if sys.platform == "win32":
            import winreg
            reg_paths = [
                (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
                (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run")
            ]
            for root, subkey in reg_paths:
                try:
                    with winreg.OpenKey(root, subkey, 0, winreg.KEY_READ) as key:
                        i = 0
                        while True:
                            try:
                                name, val, _ = winreg.EnumValue(key, i)
                                is_suspicious = False
                                val_lower = str(val).lower()

                                # Cek jika autorun mengarah ke direktori temp, powershell hidden, atau file anomali
                                if any(x in val_lower for x in ["temp\\", "appdata\\local\\temp", "powershell -enc", "powershell -w hidden", "test_malware", "c2_agent", "weaponized", "dropper", "ransomware"]):
                                    is_suspicious = True

                                persistence_items.append({
                                    "key_name": name,
                                    "command": str(val),
                                    "scope": "HKCU" if root == winreg.HKEY_CURRENT_USER else "HKLM",
                                    "is_suspicious": is_suspicious
                                })
                                i += 1
                            except OSError:
                                break
                except (PermissionError, FileNotFoundError):
                    pass

        suspicious_count = sum(1 for item in persistence_items if item.get("is_suspicious"))
        return {
            "total_persistence": len(persistence_items),
            "suspicious_count": suspicious_count,
            "items": persistence_items
        }

    def collect_credential_theft_artifacts(self):
        """Memindai jejak artefak pencurian credential, cookie browser & session hijacking (MITRE T1539/T1555)"""
        import json
        artifacts = []
        temp_dir = os.environ.get("TEMP", os.path.expanduser("~"))

        # 1. Cek artefak dump file cookie infostealer di Temp
        dump_candidates = [
            os.path.join(temp_dir, "infostealer_dumped_cookies.json"),
            os.path.join(temp_dir, "cookies.json"),
            os.path.join(temp_dir, "stolen_cookies.json"),
            os.path.join(temp_dir, "browser_cookies_loot.json")
        ]

        for cand in dump_candidates:
            if os.path.exists(cand):
                try:
                    with open(cand, "r", encoding="utf-8") as f:
                        cdata = json.load(f)
                    
                    cookie_count = len(cdata) if isinstance(cdata, list) else 0
                    domains = list(set([c.get("domain", "unknown") for c in cdata if isinstance(c, dict)]))
                    
                    artifacts.append({
                        "name": "Dump File Cookie Sesi Browser (Infostealer Loot)",
                        "path": cand,
                        "size_bytes": os.path.getsize(cand),
                        "cookie_count": cookie_count,
                        "target_domains": domains,
                        "mitre_technique": "T1539 (Steal Web Session Cookie)",
                        "severity": "CRITICAL",
                        "description": f"Ditemukan {cookie_count} token cookie sesi kedinasan aktif diekstrak ke disk ({', '.join(domains[:3])})"
                    })
                except Exception:
                    pass

        # 2. Cek apakah ada proses browser database lock / copy anomali di Temp
        return {
            "detected": len(artifacts) > 0,
            "suspicious_count": len(artifacts),
            "artifacts": artifacts
        }

    def run_full_triage(self):
        """Menjalankan seluruh tahapan triage forensik secara 100% nyata"""
        summary = self.get_system_summary()
        processes = self.collect_processes()
        network = self.collect_network_connections()
        persistence = self.collect_persistence()
        credential_theft = self.collect_credential_theft_artifacts()

        # Hitung skor ancaman riil berdasarkan anomali yang benar-benar ditemukan
        threat_score = 0
        threat_score += processes["suspicious_count"] * 35
        threat_score += network["suspicious_count"] * 30
        threat_score += persistence["suspicious_count"] * 25
        threat_score += credential_theft["suspicious_count"] * 40
        threat_score = min(threat_score, 100)

        if threat_score >= 70:
            status_level = "KRITIS (SIAGA 1)"
            status_color = "red"
        elif threat_score >= 30:
            status_level = "WASPADA (SIAGA 2)"
            status_color = "yellow"
        else:
            status_level = "AMAN (NORMAL)"
            status_color = "green"

        return {
            "summary": summary,
            "threat_score": threat_score,
            "status_level": status_level,
            "status_color": status_color,
            "processes": processes,
            "network": network,
            "persistence": persistence,
            "credential_theft": credential_theft
        }
