# coding=utf-8
from opcua.common.node import Node
import logging

logger = logging.getLogger(__name__)


class SubHandler(object):
    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another
    thread if you need to do such a thing
    """

    def datachange_notification(self, node: Node, val, data):
        # todo find out the data pattern
        logger.error(data)

    def event_notification(self, event):
        logger.error(event)
