# -*- coding: utf-8 -*-
from plugins.MODSDKSpring.core.ListenEvent import ListenEvent
from plugins.MODSDKSpring.core.Autowired import Autowired
from plugins.MODSDKSpring.core.Lazy import Lazy

@ListenEvent.InitComponentClient(namespace="special", systemName="specialName")
class TestClientComponent(object):
    
    @Lazy
    @Autowired
    def __init__(self, client, helloClientComponent, myClientComponent):
        self.client = client
        self.helloClientComponent = helloClientComponent
    
    @ListenEvent.Client(eventName="TestClientEvent")
    def testClientEvent(self, arg):
        pass