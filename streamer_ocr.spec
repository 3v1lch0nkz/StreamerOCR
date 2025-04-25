# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from PyInstaller.utils.hooks import collect_all

block_cipher = None

# Add the src directory to the path
src_path = os.path.abspath('src')

# Collect all necessary data
datas = [('resources/icon.png', 'resources')]
binaries = []
hiddenimports = [
    'PyQt5',
    'pytesseract',
    'keyboard',
    'PIL._tkinter_finder',  # Required for PIL
    'PIL.ImageGrab',
    'pyttsx3',
    'win32api',
    'win32con',
    'src.gui.region_selector',
    'src.ocr.processor',
    'src.tts.speaker'
]

# Add threading related imports
hiddenimports.extend([
    'threading',
    '_thread',
    'win32process',
    'win32gui'
])

a = Analysis(
    ['src/main.py'],
    pathex=[src_path],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='StreamerOCR',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Keeping console for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
) 