# -*- mode: python ; coding: utf-8 -*-

import os
import ansible
import site
import pkg_resources

block_cipher = None


a = Analysis(['entrypoint.py'],
             pathex=[],
             binaries=[],
             datas=[
              (os.path.join(site.getsitepackages()[0], 'ansible'), 'ansible'),
              (os.path.join(site.getsitepackages()[0], 'ansible_collections'), 'ansible_collections'),
              (os.path.join(site.getsitepackages()[0], f'mac_maker-{pkg_resources.get_distribution("mac_maker").version}.dist-info'), f'mac_maker-{pkg_resources.get_distribution("mac_maker").version}.dist-info')
             ],
             hiddenimports=['ansible_collections', 'configparser', 'smtplib', 'logging.handlers', 'distutils.version', 'pty', 'xml.etree'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='mac_maker',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
