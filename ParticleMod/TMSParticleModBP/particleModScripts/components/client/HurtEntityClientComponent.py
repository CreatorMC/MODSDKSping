# -*- coding: utf-8 -*-
from particleModScripts.plugins.MODSDKSpring.core.ListenEvent import ListenEvent
from particleModScripts.plugins.MODSDKSpring.core.Autowired import Autowired
from particleModScripts.modCommon import modConfig
from particleModScripts.modCommon import eventConfig

@ListenEvent.InitComponentClient
class HurtEntityClientComponent(object):

    @Autowired
    def __init__(self, client, particleClientComponent):
        self.client = client
        self.particleClientComponent = particleClientComponent

    @ListenEvent.Client(namespace=modConfig.MOD_NAMESPACE, systemName=modConfig.SERVER_SYSTEM_NAME, eventName=eventConfig.DAMAGE_EVENT_TO_CLIENT)
    def damageEvent(self, event):
        """
        接收到服务端传递给客户端的实体受伤事件
        """
        self.particleClientComponent.createAndPlayMicrosoftParticle('tms:fire_circle', event['pos'])