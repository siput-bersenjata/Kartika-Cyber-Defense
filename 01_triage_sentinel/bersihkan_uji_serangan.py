"""
KARTIKA TRIAGE SENTINEL - Cleanup Utility
Membersihkan proses uji nyata dan menghapus entri registri uji coba.
"""

import sys
import os
import psutil

REG_KEYS = ["Kartika_Test_Malware_C2", "Kartika_Tactical_C2_Persistence", "Kartika_Weaponized_Doc_Dropper"]

def cleanup_registry():
    if sys.platform == "win32":
        import winreg
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        for key_name in REG_KEYS:
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
                    winreg.DeleteValue(key, key_name)
                    print(f"[+] Registri Run Key '{key_name}' berhasil DIHAPUS.")
            except FileNotFoundError:
                pass
            except Exception as e:
                print(f"[-] Gagal menghapus registri '{key_name}': {e}")

def kill_test_processes():
    killed = 0
    current_pid = os.getpid()
    for p in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if p.info['pid'] == current_pid:
                continue
            cmd = " ".join(p.info['cmdline'] or [])
            # Matikan skrip uji nyata, child powershell, atau agen ransomware
            test_targets = [
                "uji_serangan_nyata.py", "cwB0AGEAcgB0AC", "Kartika_Tactical",
                "ransomware_agent.py", "dropper_dokumen_palsu.py", "c2_server.py"
            ]
            if any(t in cmd for t in test_targets):
                p.terminate()
                p.kill()
                killed += 1
                print(f"[+] Mematikan proses uji nyata (PID: {p.info['pid']})")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    print(f"[*] Total {killed} proses uji coba dinonaktifkan.")

if __name__ == "__main__":
    print("=" * 55)
    print(" [+] MEMBERSIHKAN PROSES DAN REGISTRI UJI SERANGAN")
    print("=" * 55)
    kill_test_processes()
    cleanup_registry()
    
    # Pulihkan file sandbox militer asli jika perlu
    try:
        import subprocess
        gen_script = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "skenario_serangan", "generate_dokumen_militer_asli.py"))
        if os.path.exists(gen_script):
            subprocess.run([sys.executable, gen_script], check=False)
            print("[+] Berkas dokumen sandbox militer (Excel, Word, KML) telah dipulihkan ke versi asli.")
    except Exception:
        pass

    # Hapus file artefak dump cookie uji coba
    try:
        temp_dir = os.environ.get("TEMP", os.path.expanduser("~"))
        for cand in ["infostealer_dumped_cookies.json", "cookies.json", "stolen_cookies.json"]:
            cp = os.path.join(temp_dir, cand)
            if os.path.exists(cp):
                os.remove(cp)
                print(f"[+] Artefak uji cookie '{cand}' berhasil dibersihkan dari Temp.")
    except Exception as e:
        pass

    print("[+] Sistem telah kembali ke kondisi normal sepenuhnya.")
