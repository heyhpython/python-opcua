# coding=utf-8
from functools import lru_cache
from opcua.common.node import Node


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


@lru_cache(maxsize=1)
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
    p = node.get_parent()
    p_name = p.get_display_name().Text
    assert p_name == 'Components'
    for child in node.get_children():
        properties = child.get_display_name().Text
        if properties == 'Properties':
            return child.get_children()


def get_property_name_value_of_node(node: Node):
    ret = {}
    for p in get_all_property_nodes_of_comp_node(node):
        ret[p.get_display_name().Text] = p.get_value()

    return ret
