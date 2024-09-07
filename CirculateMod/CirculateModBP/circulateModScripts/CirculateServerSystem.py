# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi
from circulateModScripts.plugins.MODSDKSpring.core.ListenEvent import ListenEvent
ServerSystem = serverApi.GetServerSystemCls()
compFactory = serverApi.GetEngineCompFactory()

@ListenEvent.InitServer
class CirculateServerSystem(ServerSystem):

    def __init__(self, namespace, systemName):
        pass
