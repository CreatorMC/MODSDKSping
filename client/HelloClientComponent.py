# -*- coding: utf-8 -*-
from plugins.MODSDKSpring.core.ListenEvent import ListenEvent
from plugins.MODSDKSpring.core.Autowired import Autowired

@ListenEvent.InitComponentClient
class HelloClientComponent(object):

    @Autowired
    def __init__(self, client, testClientComponent):
        self.client = client
        self.testClientComponent = testClientComponent
    
    def helloWorld(self):
        print("Hello World!")