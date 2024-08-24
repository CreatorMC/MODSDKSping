# -*- coding: utf-8 -*-
from plugins.MODSDKSpring.core.ListenEvent import ListenEvent
from plugins.MODSDKSpring.core.Autowired import Autowired

@ListenEvent.InitComponentClient
class MyClientComponent(object):

    @Autowired
    def __init__(self, client, testClientComponent, helloClientComponent):
        self.client = client
        self.testClientComponent = testClientComponent
        self.helloClientComponent = helloClientComponent
    
    def helloWorld(self):
        print("Hello World!")