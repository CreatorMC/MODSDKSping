# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
# 因为文件夹名称改变，所以导入路径也改变了
from tutorialComponentScripts.plugins.MODSDKSpring.core.ListenEvent import ListenEvent
ClientSystem = clientApi.GetClientSystemCls()
compFactory = clientApi.GetEngineCompFactory()

@ListenEvent.InitClient
class TutorialClientSystem(ClientSystem):

    def __init__(self, namespace, systemName):
        pass
