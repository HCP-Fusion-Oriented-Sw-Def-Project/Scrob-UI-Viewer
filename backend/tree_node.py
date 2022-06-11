class TreeNode(object):
    """
    xml树节点
    """

    def __init__(self, xml_node, layer):
        self.xml_node = xml_node
        self.attrib = {}
        for key, value in xml_node.attrib.items():
            self.attrib[key] = xml_node.attrib[key]

        self.parent = None
        self.children = []
        self.descendants = []  # 节点的子孙节点

        # 对比后发生变化的属性
        self.changed_attrs = {
            'class': 0,
            'resource-id': 0,
            'text': 0,
            'content-desc': 0,
            'size': 0,
            'location': 0,
            'color': 0
        }

        self.idx = -1  # 在结点数组中的序号
        self.layer = layer  # 层级
        self.class_index = -1

        self.full_xpath = ''  # 绝对路径
        self.xpath = []  # 所有有效的相对路径

        self.width = -1
        self.height = -1

        # 节点左上角坐标
        self.loc_x = -1
        self.loc_y = -1

        # 匹配的对象
        self.matched_node_idx = -1

        # 元素所属版本
        self.version = -1

        # 子孙节点的数量
        self.desc_num = 0

        # 兄弟节点的数量
        self.sibling_num = 0

        # 是否在列表中
        self.is_in_list = False

    def parse_bounds(self):
        """
        解析bounds 获取节点坐标范围
        """
        bounds = self.attrib['bounds']
        str_1 = bounds.split(']')[0] + ']'
        x1 = str_1.split(',')[0]
        x1 = int(x1[1:])

        y1 = str_1.split(',')[1]
        y1 = int(y1[:-1])

        str_2 = bounds.split(']')[1] + ']'
        x2 = str_2.split(',')[0]
        x2 = int(x2[1:])

        y2 = str_2.split(',')[1]
        y2 = int(y2[:-1])

        # 返回元素左上角和右下角坐标
        return x1, y1, x2, y2

    def get_bounds(self):
        """
        获取节点的长和宽，坐标
        """
        if 'bounds' in self.attrib:
            x1, y1, x2, y2 = self.parse_bounds()
            self.loc_x = x1
            self.loc_y = y1
            self.width = x2 - x1
            self.height = y2 - y1

    def get_descendants(self, node):
        """
        获取所有子孙节点 dfs
        """
        if not node.children:
            return

        for child_node in node.children:
            self.descendants.append(child_node)
            self.get_descendants(child_node)
