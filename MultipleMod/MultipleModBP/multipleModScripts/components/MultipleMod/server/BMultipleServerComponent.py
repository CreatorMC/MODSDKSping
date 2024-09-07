# -*- coding: utf-8 -*-
from multipleModScripts.plugins.MODSDKSpring.core.ListenEvent import ListenEvent
from multipleModScripts.modCommon import modConfig
from multipleModScripts.plugins.MODSDKSpring.core.log.Log import logger

@ListenEvent.InitComponentServer(namespace=modConfig.MOD_NAMESPACE, systemName=modConfig.SERVER_SYSTEM_NAME)
class BMultipleServerComponent(object):

    def __init__(self, server):
        self.server = server
        logger.info("BMultipleServerComponent 获取到的系统：" + str(server))