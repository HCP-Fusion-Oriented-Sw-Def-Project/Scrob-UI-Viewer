from backend.utility import VersionType, WorkState


class DataManager(object):
    """
    管理一些后台数据的类
    """

    def __init__(self):
        # 文件路径
        self.base_image_path = ""
        self.base_xml_path = ""
        self.updated_image_path = ""
        self.updated_xml_path = ""

        # 工作目录相当于运行时目录
        self.work_directory = 'work'

        # 保存目录
        self.save_directory = ''

        # 打开文件时的节点 它们应当是副本
        self.base_visible_nodes = []
        self.base_invisible_nodes = []
        self.updated_visible_nodes = []
        self.updated_invisible_nodes = []

        self.removed_nodes = []
        self.changed_nodes = []
        self.added_nodes = []

        self.matched_nodes = []

        # 工作目录子目录
        self.base_visible_path = 'work/base_visible'
        self.updated_visible_path = 'work/updated_visible'
        self.removed_path = 'work/removed'
        self.changed_path = 'work/changed'
        self.added_path = 'work/added'
        self.base_invisible_path = 'work/base_invisible'
        self.updated_invisible_path = 'work/updated_invisible'

        self.matched_path = 'work/matched'

        # xml树解析
        self.base_xml_tree = None
        self.updated_xml_tree = None

        # 当前的节点
        self.current_node = None
        self.current_node_version = ''

        # 当前两个版本的节点
        self.base_current_node = None
        self.updated_current_node = None

        # 读取的图片
        self.base_image = None
        self.updated_image = None

        # 目前搜索的版本
        self.search_version = VersionType.BASE.value

        #  当前项目名字
        self.work_name = ''

        # 当前项目状态
        self.work_state = WorkState.NEW.value

        # # 图片原始尺寸  已放在label类中
        # self.image_width = 0
        # self.image_height = 0

    def reset(self):
        """
        使得属性归为初始化相同
        :return:
        """

        # 文件路径
        self.base_image_path = ""
        self.base_xml_path = ""
        self.updated_image_path = ""
        self.updated_xml_path = ""

        # 保存目录
        self.save_directory = ''

        # 打开文件时的节点 它们应当是副本 用于恢复
        self.base_visible_nodes = []
        self.base_invisible_nodes = []
        self.updated_visible_nodes = []
        self.updated_invisible_nodes = []

        self.removed_nodes = []
        self.changed_nodes = []
        self.added_nodes = []

        self.matched_nodes = []

        # xml树解析
        self.base_xml_tree = None
        self.updated_xml_tree = None

        # 当前的节点
        self.current_node = None
        self.current_node_version = ''

        self.base_current_node = None
        self.updated_current_node = None

        # 读取的图片
        self.base_image = None
        self.updated_image = None

        # 目前搜索的版本
        self.search_version = VersionType.BASE.value

        #  当前项目名字
        self.work_name = ''

        # 当前项目状态
        self.work_state = WorkState.NEW.value
