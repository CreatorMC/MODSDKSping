# -*- coding: utf-8 -*-
from particleModScripts.plugins.MODSDKSpring.core.ListenEvent import ListenEvent
import mod.client.extraClientApi as clientApi
compFactory = clientApi.GetEngineCompFactory()

@ListenEvent.InitComponentClient
class ParticleClientComponent(object):

    def __init__(self, client):
        self.client = client

    def createAndPlayMicrosoftParticle(self, effectName, offset=(0,0,0), rotation=(0,0,0)):
        """
        创建并播放微软粒子

        Args:
            effectName (str): 粒子发射器名称(粒子发射器json文件中的identifier)
            offset (tuple(float,float,float), optional): 三维 表示在某处创建粒子发射器. Defaults to (0,0,0).   
            rotation (tuple(float,float,float), optional): 粒子发射器创建后使用的三维旋转(使用角度制，按照ZYX顺序旋转). Defaults to (0,0,0).
        """
        compFactory.CreateParticleSystem(None).Create(effectName, offset, rotation)