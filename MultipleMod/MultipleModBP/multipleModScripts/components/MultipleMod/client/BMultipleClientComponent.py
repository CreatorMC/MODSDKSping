# -*- coding: utf-8 -*-
from multipleModScripts.plugins.MODSDKSpring.core.ListenEvent import ListenEvent
from multipleModScripts.modCommon import modConfig
from multipleModScripts.plugins.MODSDKSpring.core.log.Log import logger

@ListenEvent.InitComponentClient(namespace=modConfig.MOD_NAMESPACE, systemName=modConfig.CLIENT_SYSTEM_NAME)
class BMultipleClientComponent(object):

    def __init__(self, client):
        self.client = client
        logger.info("BMultipleClientComponent 获取到的系统：" + str(client))