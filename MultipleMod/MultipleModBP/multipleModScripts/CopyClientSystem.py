# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
from multipleModScripts.plugins.MODSDKSpring.core.ListenEvent import ListenEvent
from components.CopyMod.client import *
ClientSystem = clientApi.GetClientSystemCls()
compFactory = clientApi.GetEngineCompFactory()

@ListenEvent.InitClient
class CopyClientSystem(ClientSystem):

    def __init__(self, namespace, systemName):
        pass
