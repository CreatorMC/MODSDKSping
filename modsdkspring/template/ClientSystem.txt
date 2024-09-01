# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
from [MOD_DIR_NAME].plugins.MODSDKSpring.core.ListenEvent import ListenEvent
ClientSystem = clientApi.GetClientSystemCls()
compFactory = clientApi.GetEngineCompFactory()

@ListenEvent.InitClient
class [CLIENT_SYSTEM_NAME](ClientSystem):

    def __init__(self, namespace, systemName):
        pass
