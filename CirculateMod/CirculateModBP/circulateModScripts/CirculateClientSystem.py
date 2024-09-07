# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
from circulateModScripts.plugins.MODSDKSpring.core.ListenEvent import ListenEvent
from circulateModScripts.plugins.MODSDKSpring.core.Autowired import Autowired
from circulateModScripts.components.client import *
ClientSystem = clientApi.GetClientSystemCls()
compFactory = clientApi.GetEngineCompFactory()

@ListenEvent.InitClient
class CirculateClientSystem(ClientSystem):

    @Autowired
    def __init__(self, namespace, systemName, a, b, c):
        self.a = a
        self.b = b
        self.c = c
    
    @ListenEvent.Client(eventName="OnLocalPlayerStopLoading")
    def onLocalPlayerStopLoading(self, event):
        # 通过 a 调用 b 和 c
        self.a.b.say("A")
        self.a.c.say("A")
        # 通过 b 调用 a 和 c
        self.b.a.say("B")
        self.b.c.say("B")
        # 通过 c 调用 a 和 b
        self.c.a.say("C")
        self.c.b.say("C")
