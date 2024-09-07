# -*- coding: utf-8 -*-
from particleModScripts.plugins.MODSDKSpring.core.ListenEvent import ListenEvent
from particleModScripts.modCommon import eventConfig
import mod.server.extraServerApi as serverApi
compFactory = serverApi.GetEngineCompFactory()

@ListenEvent.InitComponentServer
class HurtEntityServerComponent(object):

    def __init__(self, server):
        self.server = server

    @ListenEvent.Server(eventName="DamageEvent")
    def damageEvent(self, event):
        """
        实体收到伤害时触发
        """
        pos = compFactory.CreatePos(event['entityId']).GetFootPos()
        self.server.BroadcastToAllClient(eventConfig.DAMAGE_EVENT_TO_CLIENT, {
            'entityId': event['entityId'],
            'pos': pos
        })