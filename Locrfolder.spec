# -*- mode: python ; coding: utf-8 -*-
import sys ; sys.setrecursionlimit(sys.getrecursionlimit() * 5)

a = Analysis(['Locrfolder.py'],
             pathex=['/path/to/your/project'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['torch', 'torchvision', 'torchaudio', 'cuda', 'nvidia', 'tensorboard',
                       'scipy', 'sklearn', 'numpy', 'gi.repository', 'Gtk', 'GdkPixbuf', 
                       'Pango', 'HarfBuzz', 'matplotlib', 'jupyter', 'notebook', 'pandas', 
                       'boto3', 'tensorflow', 'transformers', 'lightgbm', 'altair', 'sox', 'torchaudio', 
                       'argon2', 'jedi'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False)
