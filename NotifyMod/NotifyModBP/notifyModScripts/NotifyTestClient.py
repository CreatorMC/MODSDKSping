# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
from notifyModScripts.plugins.MODSDKSpring.core.ListenEvent import ListenEvent
from notifyModScripts.plugins.MODSDKSpring.Network.NotifyManage import AllowNotify, NotifyToServer, NotifyFromClientToClient
from notifyModScripts.components.client import *
ClientSystem = clientApi.GetClientSystemCls()
compFactory = clientApi.GetEngineCompFactory()

@ListenEvent.InitClient
class NotifyTestClient(ClientSystem):

    def __init__(self, namespace, systemName):
        pass

    @ListenEvent.Client(eventName="PlayerAttackEntityEvent")
    def PlayerAttackEntityEvent(self, event):
        data = {'playerId': event['playerId'], 'damage': event['damage'], 'from': self.__class__.__name__}
        NotifyToServer("testServerSystem", data)
        NotifyToServer("testServer1", data)
        NotifyToServer("unboundTestServer1", data)
        NotifyFromClientToClient(clientApi.GetPlayerList(), "testClientSystem4", data)

    @AllowNotify
    def testClientSystem(self, event):
        print("testClientSystem: {}".format(event))

    @AllowNotify
    def testClientSystem2(self, event):
        print("testClientSystem2: {}".format(event))

    @AllowNotify
    def testClientSystem3(self, event):
        print("testClientSystem3: {}".format(event))

    @AllowNotify
    def testClientSystem4(self, event):
        print("testClientSystem4: {}".format(event))
