# -*- coding: utf-8 -*-
from circulateModScripts.plugins.MODSDKSpring.core.ListenEvent import ListenEvent
from circulateModScripts.plugins.MODSDKSpring.core.Autowired import Autowired
from circulateModScripts.plugins.MODSDKSpring.core.Lazy import Lazy
import mod.client.extraClientApi as clientApi
compFactory = clientApi.GetEngineCompFactory()
levelId = clientApi.GetLevelId()

@ListenEvent.InitComponentClient
class A(object):

    @Lazy
    @Autowired
    def __init__(self, client, b, c):
        self.client = client
        self.b = b
        self.c = c
    
    def say(self, name):
        compFactory.CreateTextNotifyClient(levelId).SetLeftCornerNotify("A 被 " + name + " 调用了")