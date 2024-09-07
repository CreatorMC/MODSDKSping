# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
from particleModScripts.plugins.MODSDKSpring.core.ListenEvent import ListenEvent
# 不要忘记 import
from particleModScripts.components.client.HurtEntityClientComponent import HurtEntityClientComponent
from particleModScripts.components.client.ParticleClientComponent import ParticleClientComponent
ClientSystem = clientApi.GetClientSystemCls()
compFactory = clientApi.GetEngineCompFactory()

@ListenEvent.InitClient
class ParticleClientSystem(ClientSystem):

    def __init__(self, namespace, systemName):
        pass

    def Destroy(self):
        self.UnListenAllEvents()
