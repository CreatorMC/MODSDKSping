# -*- coding: utf-8 -*-

from notifyModScripts.plugins.MODSDKSpring.Network.NotifyManage import AllowNotify, NotifyToServer
from notifyModScripts.plugins.MODSDKSpring.core.ListenEvent import ListenEvent


@ListenEvent.InitComponentClient
class TestClientComponent(object):

    def __init__(self, client):
        self.client = client

    @ListenEvent.Client(eventName="PlayerAttackEntityEvent")
    def PlayerAttackEntityEvent(self, event):
        data = {'playerId': event['playerId'], 'damage': event['damage'], 'from': self.__class__.__name__}
        NotifyToServer("testServer1", data)
        NotifyToServer("unboundTestServer1", data)

    @AllowNotify
    def testClient1(self, event):
        print("testClient1: {}".format(event))

@AllowNotify
def unboundTestClient1(event):
    print("unboundTestClient1: {}".format(event))