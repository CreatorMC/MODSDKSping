# -*- coding: utf-8 -*-
from plugins.MODSDKSpring.core.ListenEvent import ListenEvent
from plugins.MODSDKSpring.core.Autowired import Autowired
from plugins.MODSDKSpring.core.Lazy import Lazy

@ListenEvent.InitComponentClient
class TestClientComponent(object):
    
    @Lazy
    @Autowired
    def __init__(self, client, helloClientComponent):
        self.client = client
        self.helloClientComponent = helloClientComponent
        # self.helloClientComponent.helloWorld()
        pass
    
    @ListenEvent.Client(eventName="TestClientEvent")
    def testClientEvent(self, arg):
        pass