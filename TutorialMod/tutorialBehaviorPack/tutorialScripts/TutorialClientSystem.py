# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
from tutorialScripts.plugins.MODSDKSpring.core.ListenEvent import ListenEvent
ClientSystem = clientApi.GetClientSystemCls()
compFactory = clientApi.GetEngineCompFactory()

@ListenEvent.InitClient
class TutorialClientSystem(ClientSystem):

    def __init__(self, namespace, systemName):
        pass
