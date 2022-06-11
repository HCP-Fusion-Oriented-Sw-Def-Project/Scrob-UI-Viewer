import qdarkstyle
import sys

import pyi_splash # 报错了也没事
from PyQt5.QtWidgets import QApplication

from frontend.my_widget import MyWindow
from frontend import Tag_new_2


if __name__ == '__main__':
    # 关闭闪动图片
    pyi_splash.close()
    app = QApplication(sys.argv)
    main_window = MyWindow()
    # 实例化了一个对象
    ui = Tag_new_2.Ui_MainWindow()
    # 这里其实就是自动化给MainWindow设置组件
    ui.setupUi(main_window)

    # 设置暗黑样式
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    main_window.show()
    sys.exit(app.exec_())


