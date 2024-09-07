# -*- coding: utf-8 -*-
from circulateModScripts.plugins.MODSDKSpring.core.ListenEvent import ListenEvent
from circulateModScripts.plugins.MODSDKSpring.core.Autowired import Autowired
from circulateModScripts.plugins.MODSDKSpring.core.Lazy import Lazy
import mod.client.extraClientApi as clientApi
compFactory = clientApi.GetEngineCompFactory()
levelId = clientApi.GetLevelId()

@ListenEvent.InitComponentClient
class B(object):

    @Lazy
    @Autowired
    def __init__(self, client, a, c):
        self.client = client
        self.a = a
        self.c = c
    
    def say(self, name):
        compFactory.CreateTextNotifyClient(levelId).SetLeftCornerNotify("B 被 " + name + " 调用了")