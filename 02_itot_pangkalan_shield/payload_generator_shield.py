"""
KARTIKA NETWORK PAYLOAD SHIELD
Pusat Siber TNI Angkatan Darat (PUSSIBERAD) - Hackathon 2026
Kategori 02: DEFENSIVE SHIELD (Penangkalan)

Modul Penangkal Serangan Jaringan & Payload Generator:
Mencegat dan memutus muatan berbahaya (shellcode, reverse shell, stager, 
NOP sleds, dan C2 beacons) yang di-generate oleh tool penindakan (Payload Generator)
sebelum sempat dieksekusi pada jaringan pangkalan militer.
"""

import socket
import threading
import time
import re
from datetime import datetime

PAYLOAD_INSPECTION_PORT = 8888

class PayloadGeneratorNetworkShield:
    def __init__(self, host="0.0.0.0", port=PAYLOAD_INSPECTION_PORT):
        self.host = host
        self.port = port
        self.running = False
        self.is_bound = False
        self.bind_error = None
        self.blocked_ips = set()
        self.incident_history = []
        self.total_packets_inspected = 0
        self.total_payloads_neutralized = 0

        # Signature pola khas yang dihasilkan oleh Payload Generator ofensif (Metasploit, msfvenom, custom stagers)
        self.malicious_payload_patterns = [
            (b"\x90\x90\x90\x90", "NOP_SLED_SHELLCODE", "Injeksi Shellcode Polimorfik (Buffer Overflow)"),
            (b"powershell", "POWERSHELL_PAYLOAD_CRADLE", "Eksekusi Dropper PowerShell dari Jaringan"),
            (b"-enc", "ENCODED_BASE64_STAGER", "Obfuscated Base64 Encoded Command Stager"),
            (b"FromBase64String", "BASE64_DOWNLOAD_CRADLE", "Memory Stager Download Cradle"),
            (b"cmd.exe", "REVERSE_SHELL_INVOCATION", "Permintaan Interaktif Reverse Shell Windows"),
            (b"/bin/sh", "UNIX_SHELL_SPAWN", "Permintaan Interaktif Reverse Shell Linux"),
            (b"\xfc\xe8", "MSF_WIN_STAGER_SHELLCODE", "Windows Metasploit Binary Stager Header"),
            (b"\x31\xc0", "X86_XOR_SHELLCODE", "X86 XOR EAX Shellcode Decryption Loop"),
        ]

    def start_network_guard(self):
        """Menjalankan daemon inspeksi paket soket jaringan real-time"""
        self.running = True
        self.server_thread = threading.Thread(target=self._socket_listener, daemon=True)
        self.server_thread.start()
        print(f"[+] [PAYLOAD-SHIELD] Network Payload Guard aktif pada port {self.port} (0.0.0.0)")

    def _socket_listener(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((self.host, self.port))
            sock.listen(10)
            self.is_bound = True
            self.bind_error = None
        except Exception as e:
            self.is_bound = False
            self.bind_error = str(e)
            print(f"[-] [PAYLOAD-SHIELD] Gagal binding port {self.port}: {e}")
            return

        while self.running:
            try:
                conn, addr = sock.accept()
                threading.Thread(target=self._inspect_client_stream, args=(conn, addr), daemon=True).start()
            except Exception:
                break

    def _inspect_client_stream(self, conn, addr):
        client_ip = addr[0]
        self.total_packets_inspected += 1

        if client_ip in self.blocked_ips:
            conn.close()
            return

        start_time = time.perf_counter()
        try:
            conn.settimeout(2.0)
            data = conn.recv(4096)
            if not data:
                conn.close()
                return

            threat_detected = None
            for pattern, threat_type, description in self.malicious_payload_patterns:
                if pattern in data or (b"powershell" in data.lower()) or (b"cmd.exe" in data.lower()):
                    threat_detected = (threat_type, description)
                    break

            latency_ms = (time.perf_counter() - start_time) * 1000

            if threat_detected:
                threat_type, description = threat_detected
                self.blocked_ips.add(client_ip)
                self.total_payloads_neutralized += 1

                # Putus koneksi secara instan (Socket Severing)
                conn.close()

                incident = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "source_ip": client_ip,
                    "target_port": self.port,
                    "threat_type": threat_type,
                    "description": description,
                    "latency_ms": round(latency_ms, 3),
                    "action": "FORCE_SEVER_SOCKET & IP_BLACKLISTED",
                    "status": "DITANGKAS_SEKETIKA",
                    "mitre": "T1059 / T1071 (Payload Generator Execution)"
                }
                self.incident_history.insert(0, incident)
                if len(self.incident_history) > 100:
                    self.incident_history.pop()

                print(f"[!] [ALERTA] PAYLOAD GENERATOR TERCEGAT DARI {client_ip}!")
                print(f"    Tipe   : {threat_type} - {description}")
                print(f"    Latensi: {latency_ms:.2f} ms -> KONEKSI SEGERA DIPUTUS!")
            else:
                conn.close()
        except Exception:
            try:
                conn.close()
            except Exception:
                pass

    def get_status(self):
        status_str = "ONLINE & GUARDING" if self.is_bound else f"STANDBY ({self.bind_error or 'PORT OCCUPIED'})"
        return {
            "status": status_str,
            "is_active": self.is_bound,
            "inspection_port": self.port,
            "packets_inspected": self.total_packets_inspected,
            "payloads_neutralized": self.total_payloads_neutralized,
            "blocked_ips_count": len(self.blocked_ips),
            "recent_incidents": self.incident_history[:10]
        }
