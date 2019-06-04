# -*- mode: python -*-

block_cipher = None


a = Analysis(['shit.py'],
             pathex=['C:\\Users\\linhaichao\\Desktop\\有用的东西\\我的小玩意儿\\滚球进洞(√)'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='shit',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
