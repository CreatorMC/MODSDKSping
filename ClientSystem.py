# -*- coding: utf-8 -*-
from plugins.MODSDKSpring.core.ListenEvent import ListenEvent
from plugins.MODSDKSpring.core.Autowired import Autowired
from plugins.MODSDKSpring.core.Lazy import Lazy
from client.TestClientComponent import TestClientComponent
from client.HelloClientComponent import HelloClientComponent
from client.MyClientComponent import MyClientComponent

@ListenEvent.InitClient
class ClientSystem(object):

    @Autowired
    def __init__(self, namespace, systemName, testClientComponent, helloClientComponent, myClientComponent):
        print(testClientComponent)
        print(helloClientComponent)
        print(myClientComponent)

    @ListenEvent.Client(eventName="OnScriptTickClient")
    def onScriptTickClient(self, args = None):
        pass