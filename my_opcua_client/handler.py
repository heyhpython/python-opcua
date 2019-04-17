# coding=utf-8
from opcua.common.node import Node
import logging
from redis import StrictRedis

logger = logging.getLogger(__name__)


class SubHandler(object):
    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another
    thread if you need to do such a thing
    """
    redis_client = StrictRedis.from_url('redis://127.0.0.1:6379/2')

    def datachange_notification(self, node: Node, val, data):
        # todo find out the data pattern
        # logger.error(node.nodeid.Identifier)
        string_nodeid: str = node.nodeid.Identifier
        property_name, comp_name = string_nodeid.split('-', 1)
        # logger.error(data)
        # logger.error(val)
        if isinstance(val, bool):
            val = str(val)
        self.redis_client.hset(comp_name, property_name, val)
        self.redis_client.expire(comp_name, 10)

    def event_notification(self, event):
        logger.error(event)
