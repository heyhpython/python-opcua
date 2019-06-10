# coding=utf-8
from opcua.client.client import Client as Cgit
from my_opcua_client.handler import K6Handler
from opcua.common.node import Node

vc_url = 'opc.tcp://op2:op2@192.168.0.10:4840'


class Client(C):
    """
    my_opcua_client for webservice
    """

    def __init__(self, url, timeout=4):
        super(Client, self).__init__(url, timeout)
        self.connect()
        self.handler = K6Handler()
        self.sub = self.create_subscription(1000, self.handler)

    @property
    def objects_node(self):
        return self.get_objects_node()

    @property
    def robot_node(self):
        for child in self.objects_node.get_children():
            if child.get_display_name().Text.startswith('Station'):
                return child

    @property
    def robot_axes_node(self):
        for child in self.robot_node.get_children():
            if child.get_display_name().Text == 'Axes':
                return child

    def subscribe_to_robot(self):
        """
        subscribe all the Variable data change no matter how deep
        """
        for child in self.robot_node.get_children():
            self.subscribe_(child)

    def subscribe_(self, node: Node):
        if node.get_node_class().name == 'Variable':
            self.sub.subscribe_data_change(node)
        if node.get_children():
            for c in node.get_children():
                self.subscribe_(c)

    def subscribe_to_robot_axis(self):
        self.subscribe_(self.robot_axes_node)

    def subscribe_event(self):
        self.sub.subscribe_events()


if __name__ == '__main__':
    # 先导包
    client = Client(vc_url)
    client.subscribe_to_robot_axis()
