# -*- coding: utf-8 -*-
from plugins.MODSDKSpring.core.ListenEvent import ListenEvent
from plugins.MODSDKSpring.core.Autowired import Autowired
from plugins.MODSDKSpring.core.Lazy import Lazy
from server.HelloServerComponent import HelloServerComponent

@ListenEvent.InitServer
class ServerSystem(object):

    @Autowired
    def __init__(self, namespace, systemName):
        pass

    @ListenEvent.Server(eventName="OnScriptTickClient")
    def onScriptTickClient(self, args = None):
        pass