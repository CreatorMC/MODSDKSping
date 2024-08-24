# -*- coding: utf-8 -*-
from plugins.MODSDKSpring.core.ListenEvent import ListenEvent
from plugins.MODSDKSpring.core.Autowired import Autowired
from client.TestClientComponent import TestClientComponent
from client.HelloClientComponent import HelloClientComponent

@ListenEvent.InitClient
class ClientSystem(object):

    @Autowired
    def __init__(self, namespace, systemName):
        pass

    @ListenEvent.Client(eventName="OnScriptTickClient")
    def onScriptTickClient(self, args = None):
        pass