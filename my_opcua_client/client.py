# coding=utf-8
from opcua.client.client import Client as C
from my_opcua_client.handler import SubHandler
from my_opcua_client.utils import *

vc_url = 'opc.tcp://10.234.24.103:51210/UA/vc2OpcUaServer/'


# attrs = node.get_attributes([ua.AttributeIds.DisplayName, ua.AttributeIds.BrowseName, ua.AttributeIds.NodeId])
# 1. 订阅只能对属性


class Client(C):
    """
    my_opcua_client for webservice
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
            # self.sub.subscribe_events()

    def subscribe_event(self):
        self.sub.subscribe_events()


if __name__ == '__main__':
    client = Client(vc_url)

    client.connect()
    client.subscribe_event()