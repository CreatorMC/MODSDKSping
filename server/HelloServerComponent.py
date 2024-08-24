# -*- coding: utf-8 -*-
from plugins.MODSDKSpring.core.ListenEvent import ListenEvent
from plugins.MODSDKSpring.core.Autowired import Autowired
from plugins.MODSDKSpring.core.Lazy import Lazy

@ListenEvent.InitComponentServer
class HelloServerComponent(object):

    @Autowired
    def __init__(self, server):
        self.server = server
    
    def helloWorld(self):
        print("Hello World!")