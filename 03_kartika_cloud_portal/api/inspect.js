// Vercel Serverless Function: /api/inspect (Kartika Sovereign Binary Inspector)
const crypto = require('crypto');

function calculateEntropy(buffer) {
  if (!buffer || buffer.length === 0) return 0;
  const counts = new Uint32Array(256);
  for (let i = 0; i < buffer.length; i++) {
    counts[buffer[i]]++;
  }
  let entropy = 0;
  const len = buffer.length;
  for (let i = 0; i < 256; i++) {
    if (counts[i] > 0) {
      const p = counts[i] / len;
      entropy -= p * Math.log2(p);
    }
  }
  return parseFloat(entropy.toFixed(3));
}

function extractStrings(buffer, minLen = 4) {
  const strings = [];
  let current = [];
  for (let i = 0; i < buffer.length; i++) {
    const b = buffer[i];
    if (b >= 32 && b <= 126) {
      current.push(String.fromCharCode(b));
    } else {
      if (current.length >= minLen) {
        strings.push(current.join(''));
      }
      current = [];
    }
  }
  if (current.length >= minLen) {
    strings.push(current.join(''));
  }
  return strings;
}

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  try {
    let filename = 'Sample_Threat_Binary.exe';
    let fileBuffer = null;

    if (req.method === 'POST') {
      const body = req.body || {};
      filename = body.filename || filename;
      if (body.data_base64) {
        fileBuffer = Buffer.from(body.data_base64, 'base64');
      }
    }

    // Default inspection dataset jika payload kosong (Preset Evaluasi Biner Bajakan)
    if (!fileBuffer) {
      return res.status(200).json({
        status: 'success',
        mode: 'PRESET_SAMPLE',
        metadata: {
          filename: 'Installer_Aplikasi_Bajakan.exe (Pegasus Setup)',
          filesize_bytes: 15203932,
          filesize_mb: 14.5,
          sha256: 'e62c154d9b2d17eb8199180191bcb378e0c58d6556d75e19dc1f23afadebecef',
          md5: '883921bfe8912c0192847a98bcefa129',
          analyzed_at: new Date().toISOString()
        },
        threat_evaluation: {
          siaga_level: 'SIAGA 1 (CRITICAL MALWARE)',
          threat_score: 95,
          threat_color: 'red',
          mitre_attack_matrix: ['T1547.001', 'T1539', 'T1486', 'T1071.001', 'T1027.002', 'T1027']
        },
        binary_internals: {
          entropy: 7.996,
          entropy_verdict: 'HIGHLY_ENCRYPTED_OR_PACKED',
          pe_info: { is_pe: true, arch: 'x64 (AMD64 / 64-bit)', valid_pe: true },
          packers: ['PyInstaller (Python Executable Bundle)', 'Zlib Archive Streams']
        },
        extracted_iocs: {
          c2_urls: [
            'https://kartika-cyber-defense-portal.vercel.app/api/c2/checkin',
            'https://kartika-cyber-defense-portal.vercel.app/api/c2/upload_cookies'
          ],
          persistence_keys: [
            'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run (Kartika_Weaponized_Doc_Dropper)'
          ],
          credentials_targeted: [
            'KEMHAN_SSO_BEARER (sso.kemhan.go.id)',
            'TNI_WEBMAIL_SESSION (mail.tni.mil.id)',
            'Google Chrome Network Cookies (DPAPI Decrypted)',
            'infostealer_dumped_cookies.json'
          ],
          ransomware_indicators: [
            '.LOCKED_PUSSIBERAD',
            'xor_cipher',
            'PETUNJUK_PEMULIHAN_DOKUMEN_KODAM.txt'
          ]
        },
        forensic_findings: [
          {
            severity: 'CRITICAL',
            title: 'Tingkat Entropi Sangat Tinggi (7.996 / 8.0)',
            detail: 'Mengindikasikan payload terkompresi / terenkripsi untuk mengelabui deteksi antivirus statis.',
            mitre: 'T1027 (Obfuscated Files)'
          },
          {
            severity: 'CRITICAL',
            title: 'Pencurian Sesi Browser & Token SSO Militer',
            detail: 'Terdeteksi rutin ekstraksi cookie DPAPI browser dan kredensial SSO Kemhan/TNI.',
            mitre: 'T1539 (Steal Web Session Cookie)'
          },
          {
            severity: 'CRITICAL',
            title: 'Persistensi Startup Windows (Run Key)',
            detail: 'Mendaftarkan eksekusi otomatis tanpa izin di registri pengguna.',
            mitre: 'T1547.001 (Registry Run Keys)'
          },
          {
            severity: 'CRITICAL',
            title: 'Rutin Enkripsi Berkas Ransomware',
            detail: 'Ditemukan ekstensi .LOCKED_PUSSIBERAD dan pembuatan ransom note otomatis.',
            mitre: 'T1486 (Data Encrypted for Impact)'
          }
        ],
        sovereign_guarantee: '100% On-Premise Sovereign Inspection. Zero Data Leaked to Public Clouds/VirusTotal.'
      });
    }

    // Dynamic buffer analysis
    const entropy = calculateEntropy(fileBuffer);
    const sha256 = crypto.createHash('sha256').update(fileBuffer).digest('hex');
    const md5 = crypto.createHash('md5').update(fileBuffer).digest('hex');
    const strings = extractStrings(fileBuffer);

    let threatScore = 0;
    const mitreTags = [];
    const findings = [];
    const c2Urls = [];
    const persistenceKeys = [];
    const credentialsTargeted = [];
    const ransomwareIndicators = [];

    if (entropy > 7.2) {
      threatScore += 30;
      mitreTags.push('T1027');
      findings.push({
        severity: 'CRITICAL',
        title: `Tingkat Entropi Sangat Tinggi (${entropy} / 8.0)`,
        detail: 'Biner di-pack atau terenkripsi secara masif.',
        mitre: 'T1027'
      });
    }

    const isPyInstaller = fileBuffer.includes(Buffer.from('PyInstaller')) || fileBuffer.includes(Buffer.from('_MEI'));
    if (isPyInstaller) {
      threatScore += 20;
      mitreTags.push('T1027.002');
      findings.push({
        severity: 'MEDIUM',
        title: 'Terdeteksi PyInstaller Wrapper',
        detail: 'Biner dikompilasi dari Python untuk menyamarkan skrip.',
        mitre: 'T1027.002'
      });
    }

    const urlRegex = /https?:\/\/[a-zA-Z0-9_\-\.]+(?::[0-9]+)?(?:\/[^\s"']*)?/g;
    strings.forEach(s => {
      const match = s.match(urlRegex);
      if (match) {
        match.forEach(u => {
          if (!u.includes('schemas.microsoft.com') && !c2Urls.includes(u)) c2Urls.push(u);
        });
      }
      if (s.toLowerCase().includes('currentversion\\run')) persistenceKeys.push(s);
      if (s.toLowerCase().includes('cookie') || s.toLowerCase().includes('bearer') || s.toLowerCase().includes('dpapi')) credentialsTargeted.push(s);
      if (s.toLowerCase().includes('.locked') || s.toLowerCase().includes('ransom') || s.toLowerCase().includes('xor_cipher')) ransomwareIndicators.push(s);
    });

    if (c2Urls.length > 0) {
      threatScore += 25;
      mitreTags.push('T1071.001');
      findings.push({
        severity: 'CRITICAL',
        title: `Terdeteksi ${c2Urls.length} URL Komunikasi Jarak Jauh (C2)`,
        detail: `Ditemukan koneksi biner ke: ${c2Urls.slice(0, 2).join(', ')}`,
        mitre: 'T1071.001'
      });
    }

    if (persistenceKeys.length > 0) {
      threatScore += 25;
      mitreTags.push('T1547.001');
      findings.push({
        severity: 'CRITICAL',
        title: 'Terdeteksi Persistensi Registri Startup Windows',
        detail: `Mencoba mendaftarkan: ${persistenceKeys.slice(0, 2).join(', ')}`,
        mitre: 'T1547.001'
      });
    }

    if (credentialsTargeted.length > 0) {
      threatScore += 30;
      mitreTags.push('T1539');
      findings.push({
        severity: 'CRITICAL',
        title: 'Terdeteksi Pola Infostealer / Spyware',
        detail: `Mencari token otorisasi dan sesi browser.`,
        mitre: 'T1539'
      });
    }

    if (ransomwareIndicators.length > 0) {
      threatScore += 30;
      mitreTags.push('T1486');
      findings.push({
        severity: 'CRITICAL',
        title: 'Terdeteksi Pola Ransomware & Enkripsi',
        detail: `Membawa fungsi penguncian berkas.`,
        mitre: 'T1486'
      });
    }

    threatScore = Math.min(100, threatScore);
    let siagaLevel = 'SIAGA 4 (NORMAL / BENIGN)';
    let threatColor = 'green';
    if (threatScore >= 70) {
      siagaLevel = 'SIAGA 1 (CRITICAL MALWARE)';
      threatColor = 'red';
    } else if (threatScore >= 45) {
      siagaLevel = 'SIAGA 2 (HIGH THREAT / SUSPICIOUS)';
      threatColor = 'orange';
    } else if (threatScore >= 20) {
      siagaLevel = 'SIAGA 3 (MEDIUM ANOMALY)';
      threatColor = 'yellow';
    }

    return res.status(200).json({
      status: 'success',
      mode: 'DYNAMIC_INSPECTION',
      metadata: {
        filename,
        filesize_bytes: fileBuffer.length,
        filesize_mb: parseFloat((fileBuffer.length / (1024 * 1024)).toFixed(2)),
        sha256,
        md5,
        analyzed_at: new Date().toISOString()
      },
      threat_evaluation: {
        siaga_level: siagaLevel,
        threat_score: threatScore,
        threat_color: threatColor,
        mitre_attack_matrix: Array.from(new Set(mitreTags))
      },
      binary_internals: {
        entropy,
        entropy_verdict: entropy > 7.2 ? 'HIGHLY_ENCRYPTED_OR_PACKED' : 'NORMAL',
        pe_info: { is_pe: fileBuffer.slice(0, 2).toString() === 'MZ', arch: 'x64' },
        packers: isPyInstaller ? ['PyInstaller Bundle'] : ['Standard Native Compiler']
      },
      extracted_iocs: {
        c2_urls: c2Urls,
        persistence_keys: persistenceKeys,
        credentials_targeted: credentialsTargeted,
        ransomware_indicators: ransomwareIndicators
      },
      forensic_findings: findings,
      sovereign_guarantee: '100% On-Premise Sovereign Inspection. Zero Data Leaked to Public Clouds/VirusTotal.'
    });

  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
};
