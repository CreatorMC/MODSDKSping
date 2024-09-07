# -*- coding: utf-8 -*-
from multipleModScripts.plugins.MODSDKSpring.core.ListenEvent import ListenEvent
from multipleModScripts.modCommon import modConfig
from multipleModScripts.plugins.MODSDKSpring.core.log.Log import logger

@ListenEvent.InitComponentClient(namespace=modConfig.MOD_NAMESPACE_1, systemName=modConfig.CLIENT_SYSTEM_NAME_1)
class CCopyClientComponent(object):

    def __init__(self, client):
        self.client = client
        logger.info("CCopyClientComponent 获取到的系统：" + str(client))