"""
KARTIKA CIPHER-VAULT // SOVEREIGN MILITARY ENCRYPTION ENGINE
PUSSIBERAD - Kartika Cyber Hackathon 2026
Sub-kategori: Encryption Tool (Kategori 02: DEFENSIVE SHIELD)

Standar Keamanan:
- AES-256-GCM (Galois/Counter Mode) dengan 128-bit Authentication Tag
- Key Derivation: PBKDF2-HMAC-SHA256 (100.000 Iterasi)
- Format Kontainer Militer: .milvault
"""

import os
import struct
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes

MAGIC_HEADER = b"MILVAULT1" # 9 bytes magic identifier
SALT_SIZE = 16              # 16 bytes salt
NONCE_SIZE = 16             # 16 bytes GCM nonce
TAG_SIZE = 16               # 16 bytes authentication tag
PBKDF2_ITERATIONS = 100000

class MilitaryCryptoVault:
    def __init__(self, default_key: str = "KARTIKA-PUSSIBERAD-DEFCON-2026"):
        self.default_key = default_key

    def _derive_key(self, passphrase: str, salt: bytes) -> bytes:
        return PBKDF2(passphrase, salt, dkLen=32, count=PBKDF2_ITERATIONS, hmac_hash_module=SHA256)

    def encrypt_file(self, file_path: str, passphrase: str = None) -> str:
        """
        Mengenkripsi berkas militer menjadi berkas .milvault terautentikasi AES-256-GCM.
        Menghapus berkas plaintext asli setelah enkripsi berhasil.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Berkas tidak ditemukan: {file_path}")
            
        passphrase = passphrase or self.default_key
        salt = get_random_bytes(SALT_SIZE)
        key = self._derive_key(passphrase, salt)
        
        with open(file_path, "rb") as f:
            plaintext = f.read()
            
        cipher = AES.new(key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)
        
        # Simpan nama berkas asli di header metadata
        orig_filename = os.path.basename(file_path).encode("utf-8")
        filename_len = len(orig_filename)
        
        vault_path = file_path + ".milvault"
        with open(vault_path, "wb") as f:
            f.write(MAGIC_HEADER)
            f.write(salt)
            f.write(cipher.nonce)
            f.write(tag)
            f.write(struct.pack(">H", filename_len))
            f.write(orig_filename)
            f.write(ciphertext)
            
        # Hapus berkas asli yang tidak terenkripsi
        try:
            os.remove(file_path)
        except Exception:
            pass
            
        return vault_path

    def decrypt_file(self, vault_path: str, passphrase: str = None) -> str:
        """
        Mendekripsi berkas .milvault kembali ke berkas dokumen asli.
        Memverifikasi tag otentikasi GCM (Mencegah manipulasi data).
        """
        if not os.path.exists(vault_path) or not vault_path.endswith(".milvault"):
            raise ValueError(f"Berkas bukan kontainer .milvault valid: {vault_path}")
            
        passphrase = passphrase or self.default_key
        
        with open(vault_path, "rb") as f:
            header = f.read(len(MAGIC_HEADER))
            if header != MAGIC_HEADER:
                raise ValueError("Header berkas tidak valid / rusak!")
                
            salt = f.read(SALT_SIZE)
            nonce = f.read(NONCE_SIZE)
            tag = f.read(TAG_SIZE)
            
            raw_len = f.read(2)
            if len(raw_len) < 2:
                raise ValueError("Format metadata berkas rusak!")
            filename_len = struct.unpack(">H", raw_len)[0]
            orig_filename = f.read(filename_len).decode("utf-8", errors="replace")
            ciphertext = f.read()
            
        key = self._derive_key(passphrase, salt)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        
        try:
            plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        except ValueError:
            raise ValueError("Kunci sandi salah atau berkas telah dimanipulasi pihak asing!")
            
        target_dir = os.path.dirname(vault_path)
        restored_path = os.path.join(target_dir, orig_filename)
        
        with open(restored_path, "wb") as f:
            f.write(plaintext)
            
        try:
            os.remove(vault_path)
        except Exception:
            pass
            
        return restored_path

    def encrypt_directory(self, dir_path: str, passphrase: str = None) -> dict:
        """Mengenkripsi seluruh dokumen rahasia di direktori"""
        encrypted = []
        errors = []
        if os.path.exists(dir_path):
            for fname in os.listdir(dir_path):
                if fname.startswith("~$") or fname.endswith(".milvault") or fname.startswith("!00_CANARY"):
                    continue
                fpath = os.path.join(dir_path, fname)
                if os.path.isfile(fpath):
                    try:
                        vpath = self.encrypt_file(fpath, passphrase)
                        encrypted.append(os.path.basename(vpath))
                    except Exception as e:
                        errors.append(f"{fname}: {str(e)}")
        return {"status": "success", "encrypted": encrypted, "errors": errors}

    def decrypt_directory(self, dir_path: str, passphrase: str = None) -> dict:
        """Mendekripsi seluruh kontainer .milvault di direktori"""
        decrypted = []
        errors = []
        if os.path.exists(dir_path):
            for fname in os.listdir(dir_path):
                if fname.endswith(".milvault"):
                    fpath = os.path.join(dir_path, fname)
                    try:
                        rpath = self.decrypt_file(fpath, passphrase)
                        decrypted.append(os.path.basename(rpath))
                    except Exception as e:
                        errors.append(f"{fname}: {str(e)}")
        return {"status": "success", "decrypted": decrypted, "errors": errors}

if __name__ == "__main__":
    vault = MilitaryCryptoVault()
    print("[+] MilitaryCryptoVault AES-256-GCM siap digunakan.")
