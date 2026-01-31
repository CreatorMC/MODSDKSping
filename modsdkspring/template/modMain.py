# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
import mod.server.extraServerApi as serverApi
from mod.common.mod import Mod
from mod_log import logger

from modCommon import modConfig
from .plugins.MODSDKSpring.core.SystemInfo import SystemInfo


@Mod.Binding(name=modConfig.MOD_NAMESPACE, version=modConfig.MOD_VERSION)
class SpringTask(object):

    def __init__(self):
        logger.info("===== init %s mod =====", modConfig.MOD_NAMESPACE)

    @Mod.InitServer()
    def SpringTaskServerInit(self):
        logger.info("===== init %s server =====", modConfig.SERVER_SYSTEM_NAME)
        from threading import current_thread
        SystemInfo.serverThreadId = current_thread().ident
        serverApi.RegisterSystem(modConfig.MOD_NAMESPACE, modConfig.SERVER_SYSTEM_NAME, modConfig.SERVER_SYSTEM_CLS_PATH)

    @Mod.DestroyServer()
    def SpringTaskServerDestroy(self):
        logger.info("===== destroy %s server =====", modConfig.SERVER_SYSTEM_NAME)

    @Mod.InitClient()
    def SpringTaskClientInit(self):
        logger.info("===== init %s client =====", modConfig.CLIENT_SYSTEM_NAME)
        from threading import current_thread
        SystemInfo.clientThreadId = current_thread().ident
        clientApi.RegisterSystem(modConfig.MOD_NAMESPACE, modConfig.CLIENT_SYSTEM_NAME, modConfig.CLIENT_SYSTEM_CLS_PATH)
    
    @Mod.DestroyClient()
    def SpringTaskClientDestroy(self):
        logger.info("===== destroy %s client =====", modConfig.CLIENT_SYSTEM_NAME)
