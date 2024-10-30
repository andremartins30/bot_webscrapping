# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['robo_valentina.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('abrir_e_autenticar.py', '.'),
        ('consulta_cpf.py', '.'),
        ('consulta_cpf_endereco.py', '.'),
        ('chromedriver.exe', '.'),
    ],
    hiddenimports=[
        'selenium',
        'selenium.webdriver',
        'selenium.webdriver.common',
        'selenium.webdriver.support',
        'selenium.webdriver.chrome',
        'selenium.webdriver.support.ui',
        'selenium.webdriver.support.expected_conditions',  # Adicione esta linha
        'pandas',
        'tkinter',
        'tqdm'
    ],
    hookspath=['.'],  # Adicione o diretório atual ao hookspath
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
    name='robo_valentina',
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
    name='robo_valentina',
)