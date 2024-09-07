# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi
from particleModScripts.plugins.MODSDKSpring.core.ListenEvent import ListenEvent
# 不要忘记 import
from particleModScripts.components.server.HurtEntityServerComponent import HurtEntityServerComponent
ServerSystem = serverApi.GetServerSystemCls()
compFactory = serverApi.GetEngineCompFactory()

@ListenEvent.InitServer
class ParticleServerSystem(ServerSystem):

    def __init__(self, namespace, systemName):
        pass

    def Destroy(self):
        self.UnListenAllEvents()
