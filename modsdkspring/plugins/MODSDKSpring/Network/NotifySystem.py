# -*- coding: utf-8 -*-
from NotifyManage import NotifyManage

class NotifySystem(object):
    """
    通信系统
    """

    def _callFunction(self, eventDate):
        NotifyManage.callFunction(eventDate)