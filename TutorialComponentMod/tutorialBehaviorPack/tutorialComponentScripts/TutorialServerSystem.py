# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi
# 因为文件夹名称改变，所以导入路径也改变了
from tutorialComponentScripts.plugins.MODSDKSpring.core.ListenEvent import ListenEvent
# 导入组件，尽管这里你没有显式使用它，也必须导入！
from tutorialComponentScripts.components.server.ChatServerComponent import ChatServerComponent
ServerSystem = serverApi.GetServerSystemCls()
compFactory = serverApi.GetEngineCompFactory()

@ListenEvent.InitServer
class TutorialServerSystem(ServerSystem):

    def __init__(self, namespace, systemName):
        pass
