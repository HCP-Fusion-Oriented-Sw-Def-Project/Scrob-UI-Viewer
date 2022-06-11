import traceback

from PyQt5.QtGui import QPainter, QPen, QIcon
from PyQt5.QtWidgets import QLabel, QDialog, QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSignal, QPoint, QRect, Qt

from backend.utility import ElementType, ShowType, VersionType, WorkState, get_node_by_idx


# 所以说其实可以自己写一个类 继承于QMainWindow 然后在init的时候进行一些基本设置
class MyWindow(QMainWindow):
    # 设置信号 将元素的信息传给label 用于显示
    ele_signal = pyqtSignal(list)

    # 设置信号 用于告知label目前展示的是哪个面板 然后进行画图
    show_all_signal = pyqtSignal(list)

    close_signal = pyqtSignal(list)

    def __init__(self):
        super(MyWindow, self).__init__()

        # self.setWindowIcon(QIcon('../images/app_icon.png'))
        self.setWindowIcon(QIcon('images/app_icon.png'))

        self.work_state = WorkState.NEW.value  # 初始化为new即可

    # 那还不如关闭窗口 然后发信号过去那边进行处理 可以的
    def closeEvent(self, event):

        try:
            if self.work_state == WorkState.CHANGE.value:
                reply = QMessageBox.question(self, 'Message', 'The current work has been modified. Do you want to '
                                                              'save changes?', QMessageBox.Yes |
                                             QMessageBox.No | QMessageBox.Cancel)

                if reply == QMessageBox.Yes:
                    # 发送窗口关闭信号
                    self.close_signal.emit(['yes', self])
                    event.accept()

                elif reply == QMessageBox.No:
                    # 直接关闭
                    event.accept()

                # elif reply == QMessageBox.Cancel:
                #     event.ignore()

                else:
                    event.ignore()

        except Exception as e:
            print(e)
            print(traceback.print_exc())


class MyLabel(QLabel):
    """
    自定义重写Label类
    """

    removed_nodes = []
    changed_nodes = []
    added_nodes = []
    matched_nodes = []

    # 定义一个信号 传送一个节点的信息
    ele_signal = pyqtSignal(list)

    def __init__(self, parent=None):
        super(MyLabel, self).__init__(parent)

        # self.x1 = 0
        # self.y1 = 0
        # self.x2 = 0
        # self.y2 = 0
        #
        # self.left_top_x = 10.215
        # self.left_top_y = 38.1612
        # self.right_bottom_x = 30.06
        # self.right_bottom_y = 60.799

        self.xml_tree = None

        # 可见的节点 放到内部
        self.visible_nodes = []

        # 不可见的节点
        self.invisible_nodes = []

        self.version = -1

        self.search_version = -1

        self.image_width = 0
        self.image_height = 0

        # 目前点击的元素
        self.current_ele_x1 = 0
        self.current_ele_y1 = 0
        self.current_ele_x2 = 0
        self.current_ele_y2 = 0

        # 元素类型
        self.ele_type = ElementType.LEAF.value

        # 目前显示的元素类别
        self.show_type = ShowType.BVISIBLE.value

        # 图片放缩的比例
        self.width_ratio = 1
        self.height_ratio = 1

        # 是否展示全部节点
        self.show_all = False

    def mouseDoubleClickEvent(self, event):
        """
        重写Label单击事件
        :param event:
        :return:
        """

        # # 获取鼠标的当前坐标
        # current_x = event.x()
        # current_y = event.y()

        # if (current_x >= self.left_top_x and current_x <= self.right_bottom_x) and \
        #         (self.left_top_y <= current_y <= self.right_bottom_y):
        #     self.x1 = self.left_top_x
        #     self.y1 = self.left_top_y
        #     self.x2 = self.right_bottom_x
        #     self.y2 = self.right_bottom_y
        #     self.update()

        try:

            # 获取鼠标当前坐标
            current_x = event.x()
            current_y = event.y()

            # 获取图片的放缩比例
            self.width_ratio = int(self.width()) / self.image_width
            self.height_ratio = int(self.height()) / self.image_height

            print(self.width())
            print(self.height())

            if self.ele_type == ElementType.LEAF.value:
                search_nodes = self.xml_tree.leaf_nodes
            else:
                search_nodes = self.xml_tree.branch_nodes

            ele_flag = False
            node_list = []

            for node in search_nodes:
                x1, y1, x2, y2 = node.parse_bounds()
                tmp_x1 = x1 * self.width_ratio
                tmp_y1 = y1 * self.height_ratio
                tmp_x2 = x2 * self.width_ratio
                tmp_y2 = y2 * self.height_ratio

                if (tmp_x1 <= current_x <= tmp_x2) and \
                        (tmp_y1 <= current_y <= tmp_y2):
                    ele_flag = True
                    node_list.append(node)

            if ele_flag:
                if self.ele_type == ElementType.LEAF.value:
                    # 如果是叶子节点 则按照面积来排序 选择点击
                    node_list.sort(key=lambda x: x.width * x.height)
                else:
                    # 否则 按照层次高低来进行排序
                    # node_list.sort(key=lambda x: x.layer, reverse=True)

                    sort_for_layout_nodes(node_list)

                # node_list.sort(key=lambda x: x.layer, reverse=True)
                target_node = node_list[0]
                x1, y1, x2, y2 = target_node.parse_bounds()
                self.current_ele_x1 = x1 * self.width_ratio
                self.current_ele_y1 = y1 * self.height_ratio
                self.current_ele_x2 = x2 * self.width_ratio
                self.current_ele_y2 = y2 * self.height_ratio


                self.ele_signal.emit([target_node])
                self.update()
        except Exception as e:
            print(e)
            traceback.print_exc()

    # def mousePressEvent(self, event):
    #     if self.flag:
    #         self.update()

    # def enterEvent(self, e):
    #     """
    #     鼠标移入Label
    #     :param e:
    #     :return:
    #     """
    #
    #     print('enter label')

    def paintEvent(self, event):
        """
        画图事件
        :param event:
        :return:
        """

        # # 只有加上这句话 才能在图片上画图 然后把begin和end去掉
        # super().paintEvent(event)
        #
        # point_1 = QPoint(self.x1, self.y1)
        # point_4 = QPoint(self.x2, self.y2)
        # rect = QRect(point_1, point_4)
        #
        # painter = QPainter(self)
        # painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        #
        # painter.drawRect(rect)

        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))

        try:
            if self.show_all:

                # 获取图片的放缩比例
                self.width_ratio = int(self.width()) / self.image_width
                self.height_ratio = int(self.height()) / self.image_height
                # 绘制可见的节点 目前看来需要两套 base 和 updated
                if self.show_type == ShowType.BVISIBLE.value and self.version == VersionType.BASE.value:
                    for node in self.visible_nodes:
                        x1, y1, x2, y2 = node.parse_bounds()
                        tmp_x1 = x1 * self.width_ratio
                        tmp_y1 = y1 * self.height_ratio
                        tmp_x2 = x2 * self.width_ratio
                        tmp_y2 = y2 * self.height_ratio

                        rect = QRect(QPoint(tmp_x1, tmp_y1), QPoint(tmp_x2, tmp_y2))
                        painter.drawRect(rect)

                if self.show_type == ShowType.UVISIBLE.value and self.version == VersionType.UPDATED.value:
                    for node in self.visible_nodes:
                        x1, y1, x2, y2 = node.parse_bounds()
                        tmp_x1 = x1 * self.width_ratio
                        tmp_y1 = y1 * self.height_ratio
                        tmp_x2 = x2 * self.width_ratio
                        tmp_y2 = y2 * self.height_ratio

                        rect = QRect(QPoint(tmp_x1, tmp_y1), QPoint(tmp_x2, tmp_y2))
                        painter.drawRect(rect)

                # 绘制删除的节点
                if self.show_type == ShowType.REMOVED.value and self.version == VersionType.BASE.value:
                    for node in self.removed_nodes:
                        x1, y1, x2, y2 = node.parse_bounds()
                        tmp_x1 = x1 * self.width_ratio
                        tmp_y1 = y1 * self.height_ratio
                        tmp_x2 = x2 * self.width_ratio
                        tmp_y2 = y2 * self.height_ratio

                        rect = QRect(QPoint(tmp_x1, tmp_y1), QPoint(tmp_x2, tmp_y2))
                        painter.drawRect(rect)

                # 绘制变化的节点
                if self.show_type == ShowType.CHANGED.value and self.version == VersionType.BASE.value:
                    for node in self.changed_nodes:
                        x1, y1, x2, y2 = node.parse_bounds()
                        tmp_x1 = x1 * self.width_ratio
                        tmp_y1 = y1 * self.height_ratio
                        tmp_x2 = x2 * self.width_ratio
                        tmp_y2 = y2 * self.height_ratio

                        rect = QRect(QPoint(tmp_x1, tmp_y1), QPoint(tmp_x2, tmp_y2))
                        painter.drawRect(rect)

                # 绘制新增的节点
                if self.show_type == ShowType.ADDED.value and self.version == VersionType.UPDATED.value:
                    for node in self.added_nodes:
                        x1, y1, x2, y2 = node.parse_bounds()
                        tmp_x1 = x1 * self.width_ratio
                        tmp_y1 = y1 * self.height_ratio
                        tmp_x2 = x2 * self.width_ratio
                        tmp_y2 = y2 * self.height_ratio

                        rect = QRect(QPoint(tmp_x1, tmp_y1), QPoint(tmp_x2, tmp_y2))
                        painter.drawRect(rect)

                # 绘制不可见的Base节点
                if self.show_type == ShowType.BINVISIBLE.value and self.version == VersionType.BASE.value:
                    for node in self.invisible_nodes:
                        x1, y1, x2, y2 = node.parse_bounds()
                        tmp_x1 = x1 * self.width_ratio
                        tmp_y1 = y1 * self.height_ratio
                        tmp_x2 = x2 * self.width_ratio
                        tmp_y2 = y2 * self.height_ratio

                        rect = QRect(QPoint(tmp_x1, tmp_y1), QPoint(tmp_x2, tmp_y2))
                        painter.drawRect(rect)

                # 绘制不可见的updated节点
                if self.show_type == ShowType.UINVISIBLE.value and self.version == VersionType.UPDATED.value:
                    for node in self.invisible_nodes:
                        x1, y1, x2, y2 = node.parse_bounds()
                        tmp_x1 = x1 * self.width_ratio
                        tmp_y1 = y1 * self.height_ratio
                        tmp_x2 = x2 * self.width_ratio
                        tmp_y2 = y2 * self.height_ratio

                        rect = QRect(QPoint(tmp_x1, tmp_y1), QPoint(tmp_x2, tmp_y2))
                        painter.drawRect(rect)

                # 绘制匹配上的元素
                if self.show_type == ShowType.MATCHED.value and self.version == VersionType.BASE.value:
                    for node in self.matched_nodes:
                        x1, y1, x2, y2 = node.parse_bounds()
                        tmp_x1 = x1 * self.width_ratio
                        tmp_y1 = y1 * self.height_ratio
                        tmp_x2 = x2 * self.width_ratio
                        tmp_y2 = y2 * self.height_ratio

                        rect = QRect(QPoint(tmp_x1, tmp_y1), QPoint(tmp_x2, tmp_y2))
                        painter.drawRect(rect)


        except Exception as e:
            print(e)
            traceback.print_exc()

        # 绘制当前点击节点
        # 这只画笔颜色以及画线类型
        painter.setPen(QPen(Qt.blue, 2, Qt.DashLine))
        rect = QRect(QPoint(self.current_ele_x1, self.current_ele_y1),
                     QPoint(self.current_ele_x2, self.current_ele_y2))
        painter.drawRect(rect)

    def receive_element_event(self, info):
        """
        用于处理主窗口信号的事件
        接收主窗口对于元素的locate
        :return:
        """

        try:

            target_node = info[0]

            # 以下三种类型都是在这更新
            if self.version == target_node.version:
                # 获取图片的放缩比例
                self.width_ratio = int(self.width()) / self.image_width
                self.height_ratio = int(self.height()) / self.image_height
                x1, y1, x2, y2 = target_node.parse_bounds()

                self.current_ele_x1 = x1 * self.width_ratio
                self.current_ele_y1 = y1 * self.height_ratio
                self.current_ele_x2 = x2 * self.width_ratio
                self.current_ele_y2 = y2 * self.height_ratio
                self.update()

            else:
                search_node = None
                if target_node.matched_node_idx != -1:
                    for node in self.xml_tree.nodes:
                        if node.idx == target_node.matched_node_idx:
                            search_node = node
                            break

                    if search_node is not None:
                        self.width_ratio = int(self.width()) / self.image_width
                        self.height_ratio = int(self.height()) / self.image_height
                        x1, y1, x2, y2 = search_node.parse_bounds()
                        self.current_ele_x1 = x1 * self.width_ratio
                        self.current_ele_y1 = y1 * self.height_ratio
                        self.current_ele_x2 = x2 * self.width_ratio
                        self.current_ele_y2 = y2 * self.height_ratio
                        self.update()

        except Exception as e:
            print(e)
            traceback.print_exc()

    def show_all_event(self, info):
        """
        用于接收主窗口的信号
        是否要展示全部元素
        :return:
        """

        # 思路是主窗口发消息过来 然后这边去修改 show_all 以及show_type, 然后进行self.update()

        show_all = info[0]
        show_type = info[1]

        self.show_all = show_all
        self.show_type = show_type

        # print('是否展示全部')
        # print(self.show_all)
        # print('展示类型')
        # print(self.show_type)

        self.update()

    def ele_type_change_event(self, index):
        """
        用于接收主窗口信号
        改变要定位的元素类型
        :param
        :return:
        """

        if index == 0:
            self.ele_type = ElementType.LEAF.value

        if index == 1:
            self.ele_type = ElementType.BRANCH.value

    # def mousePressEvent(self, event):
    #     self.flag = True
    #     self.x0 = event.x()
    #     self.y0 = event.y()
    #     # 鼠标释放事件
    #
    # def mouseReleaseEvent(self, event):
    #     self.flag = False
    #     # 鼠标移动事件
    #
    # def mouseMoveEvent(self, event):
    #     if self.flag:
    #         self.x1 = event.x()
    #         self.y1 = event.y()
    #         self.update()
    #     # 绘制事件

    # def paintEvent(self, event):
    #     super().paintEvent(event)
    #     rect = QRect(self.x0, self.y0, abs(self.x1 - self.x0), abs(self.y1 - self.y0))
    #     painter = QPainter(self)
    #     painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
    #     painter.drawRect(rect)


class MyDialog(QDialog):
    """
    自定义重写Dialog类
    :param QDialog:
    :return:
    """

    # 给Dialog添加一个信号 用于传list参数到主窗口
    # 必须定义为类静态属性 而不是放在类对象构造里面
    path_signal = pyqtSignal(list)

    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)
        self.setWindowIcon(QIcon('../images/app_icon.png'))


def sort_for_layout_nodes(node_list):
    """
    对layout节点进行排序
    排序方法为 先按照面积来排序 面积相同的情况下按照包含子节点数量多少来排序 不太行
    选择排序
    :param node_list:
    :return:
    """

    for i in range(0, len(node_list) - 1):
        min_pos = i

        for j in range(i + 1, len(node_list)):

            # if node_list[j].width * node_list[j].height < node_list[min_pos].width * node_list[min_pos].height:
            #     min_pos = j
            #
            # if node_list[j].width * node_list[j].height == node_list[min_pos].width * node_list[min_pos].height:
            #     if node_list[j].desc_num > node_list[i].desc_num:
            #         min_pos = j

            # 按照索引排列 再按照兄弟节点的数量排 (it works .. lol  某些情况不行 如果先按照兄弟节点数量排列 再按照index大小排列呢)
            if int(node_list[j].attrib['index']) > int(node_list[min_pos].attrib['index']):
                min_pos = j

            if int(node_list[j].attrib['index']) == int(node_list[min_pos].attrib['index']):
                if node_list[j].sibling_num > node_list[min_pos].sibling_num:
                    min_pos = j

            # # 按照兄弟节点数量排列
            # if node_list[j].sibling_num > node_list[min_pos].sibling_num:
            #     if node_list[min_pos].layer - node_list[j].layer < 5:
            #         min_pos = j

            # if node_list[j].sibling_num == node_list[min_pos].sibling_num:
            #     # 再比面积
            #     if node_list[j].width * node_list[j].height < node_list[min_pos].width * node_list[min_pos].height:
            #         min_pos = j

        if min_pos != i:
            tmp_node = node_list[min_pos]
            node_list[min_pos] = node_list[i]
            node_list[i] = tmp_node
