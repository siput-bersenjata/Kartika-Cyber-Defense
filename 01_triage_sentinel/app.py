"""
KARTIKA TRIAGE SENTINEL - Web Service & Real Forensic API Controller
Pusat Siber TNI Angkatan Darat (PUSSIBERAD) Hackathon 2026
100% Menggunakan Data Nyata Sistem Operasi (Tanpa Hardcoded Dummy Data)
"""

__AUTHOR__ = "Sovian (@siput-bersenjata)"
__GITHUB__ = "https://github.com/siput-bersenjata"
__COPYRIGHT__ = "Hak Cipta (c) 2026 Sovian. All rights reserved."
__SIGNATURE__ = "SHA256:4a8b79e19d70231cfb561d9a2884b2c1590e871e-SOVIAN-SIPUT-BERSENJATA-PUSSIBERAD-2026"

from flask import Flask, render_template, jsonify, request
from collector import ForensicCollector
from ai_analyzer import TacticalAIAnalyzer
import subprocess
import sys
import os
import signal

if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    app = Flask(__name__, template_folder=template_folder)
else:
    app = Flask(__name__)

collector = ForensicCollector()
analyzer = TacticalAIAnalyzer()

# Variabel pelacak proses pengujian serangan nyata
_payload_process = None

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With, Range"
    response.headers["Access-Control-Allow-Private-Network"] = "true"
    return response

@app.route('/', defaults={'path': ''}, methods=['OPTIONS'])
@app.route('/<path:path>', methods=['OPTIONS'])
def options_preflight(path):
    response = app.make_default_options_response()
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With, Range"
    response.headers["Access-Control-Allow-Private-Network"] = "true"
    return response

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/health")
def health():
    return jsonify({
        "status": "online",
        "system": "KARTIKA TRIAGE SENTINEL v1.0",
        "mode": "100% REAL TELEMETRY",
        "author": __AUTHOR__,
        "github": __GITHUB__,
        "digital_watermark": __SIGNATURE__,
        "ollama_available": analyzer.is_ollama_available(),
        "model": analyzer.model
    })

@app.route("/api/triage")
def run_triage_api():
    """Mengumpulkan 100% artefak nyata dari OS saat ini dan menganalisisnya"""
    data = collector.run_full_triage()
    ai_result = analyzer.generate_analysis(data)

    return jsonify({
        "triage": data,
        "ai_analysis": ai_result,
        "is_real_telemetry": True
    })

@app.route("/api/spawn-real-payload", methods=["POST"])
def spawn_real_payload():
    """Menjalankan proses uji coba nyata di background yang membuka port 4444 
    dan mendaftarkan key startup nyata agar diuji oleh collector secara autentik."""
    global _payload_process
    payload_script = os.path.join(os.path.dirname(__file__), "uji_serangan_nyata.py")
    
    if _payload_process is None or _payload_process.poll() is not None:
        try:
            _payload_process = subprocess.Popen([sys.executable, payload_script])
            return jsonify({
                "status": "active",
                "message": "Payload uji nyata AKTIF berjalan di background (PID terdaftar, port 4444 terbuka, registry Run terpasang)!"
            })
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    else:
        return jsonify({
            "status": "already_running",
            "message": "Payload uji nyata sudah berjalan di background."
        })

@app.route("/api/kill-real-payload", methods=["POST"])
def kill_real_payload():
    """Mematikan proses uji coba nyata dan membersihkan registri"""
    global _payload_process
    cleanup_script = os.path.join(os.path.dirname(__file__), "bersihkan_uji_serangan.py")
    
    try:
        subprocess.run([sys.executable, cleanup_script], timeout=5)
    except Exception:
        pass

    if _payload_process is not None:
        try:
            _payload_process.terminate()
            _payload_process.kill()
        except Exception:
            pass
        _payload_process = None

    return jsonify({
        "status": "terminated",
        "message": "Proses uji nyata dimatikan dan registri Windows telah dibersihkan normal."
    })

if __name__ == "__main__":
    print("=" * 70)
    print(" [+] KARTIKA TRIAGE SENTINEL SIAP BEROPERASI (100% REAL DATA)")
    print(" [+] PUSSIBERAD // PUSAT SIBER TNI ANGKATAN DARAT")
    print(f" [+] PENGEMBANG UTAMA : {__AUTHOR__}")
    print(f" [+] REPOSITORI RESMI : {__GITHUB__}")
    print(f" [+] WATERMARK DIGITAL: {__SIGNATURE__}")
    print(" [+] Memindai artefak sistem operasi secara real-time")
    print(" [+] Akses Dashboard di: http://127.0.0.1:5000")
    print("=" * 70)
    app.run(host="127.0.0.1", port=5000, debug=False)
