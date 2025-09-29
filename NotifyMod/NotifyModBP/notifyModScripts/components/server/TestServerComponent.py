# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi
from notifyModScripts.plugins.MODSDKSpring.Network.NotifyManage import AllowNotify, NotifyToClient
from notifyModScripts.plugins.MODSDKSpring.core.ListenEvent import ListenEvent


@ListenEvent.InitComponentServer
class TestServerComponent(object):

    def __init__(self, server):
        self.server = server

    @ListenEvent.Server(eventName="ServerChatEvent")
    def ServerChatEvent(self, event):
        hostId = serverApi.GetHostPlayerId()
        data = {'message': event['message'], 'from': self.__class__.__name__}
        NotifyToClient(hostId, "testClient1", data)
        NotifyToClient(hostId, "unboundTestClient1", data)

    @AllowNotify
    def testServer1(self, event):
        print("testServer1: {}".format(event))

@AllowNotify
def unboundTestServer1(event):
    print("unboundTestServer1: {}".format(event))