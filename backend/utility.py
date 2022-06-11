import os
from enum import Enum


class VersionType(Enum):
    """
    版本类型
    :param Enum:
    :return:
    """

    BASE = 0
    UPDATED = 1


class ElementType(Enum):
    """
    元素类型
    """
    LEAF = 'leaf'
    BRANCH = 'branch'


class ShowType(Enum):
    """
    所展示的元素种类
    """

    BVISIBLE = 'base_visible'
    UVISIBLE = 'updated_visible'
    REMOVED = 'removed'
    CHANGED = 'changed'
    ADDED = 'added'
    BINVISIBLE = 'base_invisible'
    UINVISIBLE = 'updated_invisible'
    MATCHED = 'matched'


class SearchType(Enum):
    """
    搜索元素所用的属性类型
    """

    NO = 'no'
    BOUNDS = 'bounds'
    XPATH = 'xpath'
    ILLEGAL = 'illegal'


class WorkState(Enum):
    """
    当前项目的状态
    """

    NEW = 0
    REMAIN = 1
    CHANGE = 2


def is_node_in_list(node, node_list):
    """
    判断一个node是否在列表中
    :param node:
    :param node_list:
    :return:
    """

    for tmp_node in node_list:
        if node.idx == tmp_node.idx:
            return True

    return False


def get_node_by_idx(idx, node_list):
    """
    根据节点的idx找到节点
    :param node:
    :param node_list:
    :return:
    """

    for tmp_node in node_list:
        if tmp_node.idx == idx:
            return tmp_node

    return None


def is_xpath_matched(x_node, y_node):
    """
    判断两个节点的xpath列表是否相交
    :param x_node:
    :param y_node:
    :return:
    """

    for x_xpath in x_node.xpath:
        if x_xpath in y_node.xpath:
            return True

    return False


def get_node_changes(x_node, y_node):
    """
    对两个节点的变化进行简单判断
    只设计文本 不涉及图片
    :param x_node:
    :param y_node:
    :return:
    """

    if x_node.attrib['class'] != y_node.attrib['class']:
        x_node.changed_attrs['class'] = 1

    if x_node.attrib['resource-id'] != y_node.attrib['resource-id']:
        x_node.changed_attrs['resource-id'] = 1

    if x_node.attrib['text'] != y_node.attrib['text']:
        x_node.changed_attrs['text'] = 1

    if x_node.attrib['content-desc'] != y_node.attrib['content-desc']:
        x_node.changed_attrs['content-desc'] = 1

    if x_node.width != y_node.width or x_node.height != y_node.height:
        x_node.changed_attrs['size'] = 1

    if x_node.loc_x != y_node.loc_x or x_node.loc_y != y_node.loc_y:
        x_node.changed_attrs['location'] = 1


def delete_files(path):
    """
    删除一个路径下的所有文件
    深度优先搜索
    :param path:
    :return:
    """

    dirs = os.listdir(path)

    for sub_path in dirs:
        tmp_path = os.path.join(path, sub_path)

        if os.path.isdir(tmp_path):  # 如果是直接子文件夹 那么只删除里面的文件 但是这个文件夹不删除
            delete_files(tmp_path)
        else:  # 否则删除文件
            os.remove(tmp_path)
