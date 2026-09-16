# -*- mode: python ; coding: utf-8 -*-

"""
PyInstaller spec file for Markup+.

Builds a standalone executable (mup.exe) that does not require
Python to be installed on the target system.

Usage:
    pyinstaller mup.spec --clean --noconfirm
"""

block_cipher = None


a = Analysis(
    ['launcher.py'],
    pathex=['src'],
    binaries=[],
    datas=[
        ('assets', 'assets'),
        ('src/markup_plus/themes/css', 'markup_plus/themes/css'),  # ← اضافه شد
        ('README.md', '.'),
        ('LICENSE', '.'),
    ],
    hiddenimports=[
        'markup_plus',
        'markup_plus.cli',
        'markup_plus.cli.commands',
        'markup_plus.cli.display',
        'markup_plus.cli.errors',
        'markup_plus.cli.theme',
        'markup_plus.parser',
        'markup_plus.renderer',
        'markup_plus.ast',
        'markup_plus.errors',
        'markup_plus.lexer',
        'markup_plus.themes',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'unittest',
        'pydoc',
        'doctest',
        'test',
        'distutils',
        'setuptools',
        'pip',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='mup',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icons/mup-logo.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='mup',
)