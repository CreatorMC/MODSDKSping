# -*- coding: utf-8 -*-
from circulateModScripts.plugins.MODSDKSpring.core.ListenEvent import ListenEvent
from circulateModScripts.plugins.MODSDKSpring.core.Autowired import Autowired
import mod.client.extraClientApi as clientApi
compFactory = clientApi.GetEngineCompFactory()
levelId = clientApi.GetLevelId()

@ListenEvent.InitComponentClient
class C(object):

    @Autowired
    def __init__(self, client, a, b):
        self.client = client
        self.a = a
        self.b = b

    def say(self, name):
        compFactory.CreateTextNotifyClient(levelId).SetLeftCornerNotify("C 被 " + name + " 调用了")