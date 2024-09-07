# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi
from multipleModScripts.plugins.MODSDKSpring.core.ListenEvent import ListenEvent
from components.CopyMod.server import *
ServerSystem = serverApi.GetServerSystemCls()
compFactory = serverApi.GetEngineCompFactory()

@ListenEvent.InitServer
class CopyServerSystem(ServerSystem):

    def __init__(self, namespace, systemName):
        pass
