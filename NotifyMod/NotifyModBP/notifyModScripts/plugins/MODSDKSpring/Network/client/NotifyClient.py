# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ..NotifyManage import NotifyManage
from ..NotifySystem import NotifySystem
from ...core.log.Log import logger
ClientSystem = clientApi.GetClientSystemCls()

class NotifyClient(ClientSystem, NotifySystem):
    """
    通信客户端
    """

    @staticmethod
    def getSystem():
        system = clientApi.GetSystem(NotifyManage.NAMESPACE, NotifyManage.CLIENT_SYSTEM_NAME)
        if system:
            return system
        logger.info("通信客户端注册成功")
        return clientApi.RegisterSystem(NotifyManage.NAMESPACE, NotifyManage.CLIENT_SYSTEM_NAME, NotifyClient.__module__ + '.' + NotifyClient.__name__)

    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)
        # 监听服务端事件
        self.ListenForEvent(NotifyManage.NAMESPACE, NotifyManage.SERVER_SYSTEM_NAME, NotifyManage.SERVER_TO_CLIENT, self, self._callFunction)

    def Destroy(self):
        self.UnListenAllEvents()