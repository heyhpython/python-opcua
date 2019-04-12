# coding=utf-8
from opcua.client.client import Client as C
from opcua.common.node import Node
from opcua.ua.uatypes import FourByteNodeId
from opcua.ua import ObjectIds
from client.handler import SubHandler

vc_url = 'opc.tcp://10.234.24.103:51210/UA/vc2OpcUaServer/'


# attrs = node.get_attributes([ua.AttributeIds.DisplayName, ua.AttributeIds.BrowseName, ua.AttributeIds.NodeId])
# 1. 订阅只能对属性

def get_property_of_comp_node(node: Node, property_name):
    """
    :param node:
    :param property_name str
    :return:
    """
    p = node.get_parent()
    p_name = p.get_display_name().Text
    assert p_name == 'Components'
    for child in node.get_children():
        properties = child.get_display_name().Text
        if properties == 'Properties':
            for c in child.get_children():
                name = c.get_display_name().Text
                if name == property_name:
                    return c.get_value()


def get_all_comps(node: Node):
    """
    get all children nodes no matter how deep
    :param node: Node
    :return: dict
    """
    ret = {}
    name = node.get_display_name().Text
    assert name == 'Components'
    for comp in node.get_children():
        comp_name = get_property_of_comp_node(comp, 'Name')
        ret[hash(comp_name)] = comp
    return ret


def get_all_property_nodes_of_comp_node(node: Node):
    ret = []
    p = node.get_parent()
    p_name = p.get_display_name().Text
    assert p_name == 'Components'
    for child in node.get_children():
        properties = child.get_display_name().Text
        if properties == 'Properties':
            for c in child.get_children():
                # name = c.get_display_name().Text
                # value = c.get_value()
                ret.append(c)
    return ret


def get_property_name_value_of_node(node: Node):
    ret = {}
    for p in get_all_property_nodes_of_comp_node(node):
        ret[p.get_display_name().Text] = p.get_value()

    return ret


class Client(C):
    """
    client for webservice
    """

    def __init__(self, url, timeout=4):
        super(Client, self).__init__(url, timeout)
        self.connect()
        self.handler = SubHandler()
        self.sub = self.create_subscription(1000, self.handler)

    @property
    def root_node(self):
        return self.get_root_node()

    @property
    def objects_node(self):
        return self.get_objects_node()

    @property
    def comps(self):
        return get_all_comps(self.comps_node)

    @property
    def comps_node(self):
        for child in self.vc_root_node.get_children():
            if child.get_display_name().Text == 'Components':
                return child

    @property
    def vc_app_node(self):
        for child in self.vc_root_node.get_children():
            if child.get_display_name().Text == 'VC Application':
                return child

    @property
    def vc_root_node(self):
        for child in self.objects_node.get_children():
            if child.get_display_name().Text == 'VisualComponents':
                return child

    def subscribe_all_comps(self):
        for comp_name_hash, comp in self.comps.items():
            handle = self.sub.subscribe_data_change(get_all_property_nodes_of_comp_node(comp))
            self.sub.subscribe_events()


if __name__ == '__main__':
    client = Client(vc_url)
    client.connect()
    open()
