"""
Build Script: Mengompilasi Kartika Canary-Shield menjadi Aplikasi Portable (.exe)
Tanpa perlu instalasi Python di komputer tujuan/komputer panitia.
"""

import os
import sys
import subprocess

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

def build():
    print("=" * 65)
    print(" [+] MEMULAI BUILD PORTABLE EXE (KARTIKA CANARY-SHIELD)")
    print("=" * 65)

    templates_dir = os.path.join(CURRENT_DIR, "templates")
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onedir",
        "--name", "Kartika_Canary_Shield",
        "--add-data", f"{templates_dir};templates",
        os.path.join(CURRENT_DIR, "app.py")
    ]
    
    print("[*] Menjalankan PyInstaller...")
    res = subprocess.run(cmd, cwd=CURRENT_DIR)
    if res.returncode == 0:
        print("\n[+] BUILD BERHASIL!")
        dist_dir = os.path.join(CURRENT_DIR, "dist", "Kartika_Canary_Shield")
        exe_path = os.path.join(dist_dir, "Kartika_Canary_Shield.exe")
        print(f"[+] Lokasi Executable Portable: {exe_path}")

        # Sinkronisasi otomatis ke paket flashdisk
        flashdisk_dest = os.path.join(CURRENT_DIR, "..", "PAKET_FLASHDISK_SISTEM_PENANGKAL", "02_Canary_Shield_Portable")
        if os.path.exists(flashdisk_dest):
            import shutil
            print(f"[*] Menyalin biner portable ke paket flashdisk: {flashdisk_dest}")
            shutil.copytree(dist_dir, flashdisk_dest, dirs_exist_ok=True)
            print("[+] Berhasil disinkronkan ke PAKET_FLASHDISK_SISTEM_PENANGKAL/02_Canary_Shield_Portable!")
    else:
        print(f"\n[-] Build gagal dengan kode error: {res.returncode}")

if __name__ == "__main__":
    build()
