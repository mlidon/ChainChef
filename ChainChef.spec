# ChainChef.spec
# -*- mode: python ; coding: utf-8 -*-

import sys
import os

# ⚡ Añadir el directorio raíz al path para que 'app' sea importable
sys.path.insert(0, SPECPATH)

from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

spec_dir = SPECPATH
frontend_dir = os.path.join(spec_dir, 'frontend')

# Recopilar archivos del frontend
frontend_datas = []
if os.path.exists(frontend_dir):
    for root, dirs, files in os.walk(frontend_dir):
        for file in files:
            src = os.path.join(root, file)
            dest = os.path.relpath(src, spec_dir)
            frontend_datas.append((src, os.path.dirname(dest)))

# Módulos ocultos base
hiddenimports = [
    'langchain_ollama',
    'langchain_core',
    'langchain_community',
    'pydantic',
    'uvicorn.logging',
    'uvicorn.loops',
    'uvicorn.loops.auto',
    'uvicorn.protocols',
    'uvicorn.protocols.http',
    'uvicorn.protocols.http.auto',
    'uvicorn.protocols.websockets',
    'uvicorn.protocols.websockets.auto',
    'uvicorn.lifespan',
    'uvicorn.lifespan.on',
    'starlette',
    'fastapi',
    'passlib.handlers.argon2',
    'passlib.handlers.bcrypt',
    'passlib.handlers.pbkdf2',
]

hiddenimports += collect_submodules('app')
hiddenimports += collect_submodules('passlib')

a = Analysis(
    ['run_server.py'],
    pathex=[spec_dir],          # Redundante pero lo mantenemos
    binaries=[],
    datas=frontend_datas,
    hiddenimports=hiddenimports,
    hookspath=[],
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
    name='ChainChef',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    icon=os.path.join(frontend_dir, 'img', 'logo_dark.ico')
)