# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi
from plugins.MODSDKSpring.core.ListenEvent import ListenEvent
ServerSystem = serverApi.GetServerSystemCls()
compFactory = serverApi.GetEngineCompFactory()

@ListenEvent.InitServer
class [SERVER_SYSTEM_NAME](ServerSystem):

    def __init__(self, namespace, systemName):
        super([SERVER_SYSTEM_NAME], self).__init__(namespace, systemName)

    def Destroy(self):
        self.UnListenAllEvents()
