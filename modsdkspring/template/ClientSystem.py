# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
from [MOD_DIR_NAME].plugins.MODSDKSpring.core.ListenEvent import ListenEvent
# noinspection PyUnusedImports
from [MOD_DIR_NAME].plugins.MODSDKSpring.DB.ClientDB import clientDB
ClientSystem = clientApi.GetClientSystemCls()
compFactory = clientApi.GetEngineCompFactory()

@ListenEvent.InitClient
class [CLIENT_SYSTEM_NAME](ClientSystem):

    def __init__(self, namespace, systemName):
        pass
