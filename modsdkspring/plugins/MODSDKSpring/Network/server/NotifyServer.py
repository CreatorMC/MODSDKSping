# -*- coding: utf-8 -*-
import mod.server.extraServerApi as serverApi
from ..NotifyManage import NotifyManage
from ..NotifySystem import NotifySystem
from ...core.log.Log import logger
ServerSystem = serverApi.GetServerSystemCls()

class NotifyServer(ServerSystem, NotifySystem):
    """
    通信服务端
    """

    @staticmethod
    def getSystem():
        system = serverApi.GetSystem(NotifyManage.NAMESPACE, NotifyManage.SERVER_SYSTEM_NAME)
        if system:
            return system
        logger.info("通信服务端注册成功")
        return serverApi.RegisterSystem(NotifyManage.NAMESPACE, NotifyManage.SERVER_SYSTEM_NAME, NotifyServer.__module__ + '.' + NotifyServer.__name__)

    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        # 监听客户端事件
        self.ListenForEvent(NotifyManage.NAMESPACE, NotifyManage.CLIENT_SYSTEM_NAME, NotifyManage.CLIENT_TO_SERVER, self, self._callFunction)
        self.ListenForEvent(NotifyManage.NAMESPACE, NotifyManage.CLIENT_SYSTEM_NAME, NotifyManage.CLIENT_TO_CLIENT, self, self._callClientFunction)

    def _callClientFunction(self, eventDate):
        targetIdList = eventDate.pop(NotifyManage.EVENT_ID_LIST, None)
        self.NotifyToMultiClients(targetIdList, NotifyManage.SERVER_TO_CLIENT, eventDate)

    def Destroy(self):
        self.UnListenAllEvents()