# coding=utf-8
from opcua.common.node import Node
import logging
from redis import StrictRedis
import json

logger = logging.getLogger(__name__)


class K6Handler(object):
    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another
    thread if you need to do such a thing
    """
    redis_client = StrictRedis.from_url('redis://127.0.0.1:6379/2')

    def datachange_notification(self, node: Node, val, data):
        node_id = node.nodeid.Identifier
        station, levels = node_id.split('.', maxsplit=1)
        self.redis_client.hset(station, levels, val if not isinstance(val, bool) else str(val))
        logger.error(node_id)
        logger.error(val)
        logger.error(data)

    def event_notification(self, event):
        logger.error(event)
