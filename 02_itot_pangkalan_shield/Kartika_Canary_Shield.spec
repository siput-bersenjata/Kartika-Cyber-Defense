# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:/Users/bramg/Documents/Coding/kartikacyberhackathon/02_itot_pangkalan_shield/app.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Users/bramg/Documents/Coding/kartikacyberhackathon/02_itot_pangkalan_shield/templates', 'templates')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Kartika_Canary_Shield',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Kartika_Canary_Shield',
)
