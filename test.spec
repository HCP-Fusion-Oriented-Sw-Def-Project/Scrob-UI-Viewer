# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

# 添加资源文件 以及需要一起打包的代码
add_files = [
						('E:\\pycharm_files\\dabao_test2\\backend', 'backend'),
						('E:\\pycharm_files\\dabao_test2\\frontend', 'frontend'),
						('E:\\pycharm_files\\dabao_test2\\images', 'images'),
						('E:\\pycharm_files\\dabao_test2\\work', 'work')
					]
						  
					

a = Analysis(['test.py'],
             pathex=['E:\\pycharm_files\\dabao_test2'],
             binaries=[],
             datas=add_files,
             hiddenimports=['pkg_resources.py2_warn'],   # 注意 hiddenimports 是在Analysis里面的
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
			 

# 增加闪存图片
splash = Splash('images\\app_icon.png',
                binaries=a.binaries,
                datas=a.datas, 
				max_img_size=(128, 128),
				text_pos=None)      # 设置图片的最大尺寸
                #text_pos=(10, 50),
                #text_size=6,
                #text_color='black')

			 
			 
			 
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
			splash,              # 增加splash 对象
          a.scripts,
          [],
          exclude_binaries=True,
          name='Scrob UI Viewer',     # 设置应用名
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False, #  设置不要弹出cmd窗口
		  icon='images\\desktop.ico'        # 设置图标
		  )
coll = COLLECT(exe,
			   splash.binaries,      # 增加splash 二进制文件
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='test',
			   )


