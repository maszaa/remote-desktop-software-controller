# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['app\\manage.py'],
             pathex=['venv\\Lib\\site-packages'],
             binaries=[],
             datas=[
                 ('venv\\Lib\\site-packages\\ahk\\templates', 'ahk\\templates'),
                 ('LICENSE', '.'),
                 ('README.md', '.'),
				 ('examples\\glm4.json', 'examples')
             ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=['scripts\\pyi_rth_django.py'],
             excludes=['tkinter'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='RDSC',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='RDSC')
