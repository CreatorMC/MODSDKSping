# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi
from notifyModScripts.plugins.MODSDKSpring.core.ListenEvent import ListenEvent
from notifyModScripts.plugins.MODSDKSpring.Network.NotifyManage import AllowNotify, NotifyToClient, NotifyToMultiClients, BroadcastToAllClient
from notifyModScripts.components.server import *
ServerSystem = serverApi.GetServerSystemCls()
compFactory = serverApi.GetEngineCompFactory()

@ListenEvent.InitServer
class NotifyTestServer(ServerSystem):

    def __init__(self, namespace, systemName):
        pass

    @ListenEvent.Server(eventName="ServerChatEvent")
    def ServerChatEvent(self, event):
        hostId = serverApi.GetHostPlayerId()
        data = {'message': event['message'], 'from': self.__class__.__name__}
        NotifyToClient(hostId, "testClientSystem", data)
        NotifyToClient(hostId, "testClient1", data)
        NotifyToClient(hostId, "unboundTestClient1", data)
        NotifyToMultiClients(serverApi.GetPlayerList(), "testClientSystem2", data)
        BroadcastToAllClient("testClientSystem3", data)

    @AllowNotify
    def testServerSystem(self, event):
        print("testServerSystem: {}".format(event))
