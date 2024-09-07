# -*- coding: utf-8 -*-
from multipleModScripts.plugins.MODSDKSpring.core.ListenEvent import ListenEvent
from multipleModScripts.modCommon import modConfig
from multipleModScripts.plugins.MODSDKSpring.core.log.Log import logger

@ListenEvent.InitComponentServer(namespace=modConfig.MOD_NAMESPACE_1, systemName=modConfig.SERVER_SYSTEM_NAME_1)
class CCopyServerComponent(object):

    def __init__(self, server):
        self.server = server
        logger.info("CCopyServerComponent 获取到的系统：" + str(server))