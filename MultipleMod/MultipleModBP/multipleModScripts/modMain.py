# -*- coding: utf-8 -*-

from mod.common.mod import Mod
import mod.client.extraClientApi as clientApi
import mod.server.extraServerApi as serverApi
from modCommon import modConfig
from mod_log import logger

@Mod.Binding(name=modConfig.MOD_NAMESPACE, version=modConfig.MOD_VERSION)
class TMSMultipleMod(object):

    def __init__(self):
        logger.info("===== init %s mod =====", modConfig.MOD_NAMESPACE)

    @Mod.InitServer()
    def TMSMultipleModServerInit(self):
        logger.info("===== init %s server =====", modConfig.SERVER_SYSTEM_NAME)
        serverApi.RegisterSystem(modConfig.MOD_NAMESPACE, modConfig.SERVER_SYSTEM_NAME, modConfig.SERVER_SYSTEM_CLS_PATH)

    @Mod.DestroyServer()
    def TMSMultipleModServerDestroy(self):
        logger.info("===== destroy %s server =====", modConfig.SERVER_SYSTEM_NAME)
    
    @Mod.InitClient()
    def TMSMultipleModClientInit(self):
        logger.info("===== init %s client =====", modConfig.CLIENT_SYSTEM_NAME)
        clientApi.RegisterSystem(modConfig.MOD_NAMESPACE, modConfig.CLIENT_SYSTEM_NAME, modConfig.CLIENT_SYSTEM_CLS_PATH)
    
    @Mod.DestroyClient()
    def TMSMultipleModClientDestroy(self):
        logger.info("===== destroy %s client =====", modConfig.CLIENT_SYSTEM_NAME)

@Mod.Binding(name=modConfig.MOD_NAMESPACE_1, version=modConfig.MOD_VERSION_1)
class TMSCopyMod(object):

    def __init__(self):
        logger.info("===== init %s mod =====", modConfig.MOD_NAMESPACE_1)

    @Mod.InitServer()
    def TMSCopyModServerInit(self):
        logger.info("===== init %s server =====", modConfig.SERVER_SYSTEM_NAME_1)
        serverApi.RegisterSystem(modConfig.MOD_NAMESPACE_1, modConfig.SERVER_SYSTEM_NAME_1, modConfig.SERVER_SYSTEM_CLS_PATH_1)

    @Mod.DestroyServer()
    def TMSCopyModServerDestroy(self):
        logger.info("===== destroy %s server =====", modConfig.SERVER_SYSTEM_NAME_1)
    
    @Mod.InitClient()
    def TMSCopyModClientInit(self):
        logger.info("===== init %s client =====", modConfig.CLIENT_SYSTEM_NAME_1)
        clientApi.RegisterSystem(modConfig.MOD_NAMESPACE_1, modConfig.CLIENT_SYSTEM_NAME_1, modConfig.CLIENT_SYSTEM_CLS_PATH_1)
    
    @Mod.DestroyClient()
    def TMSCopyModClientDestroy(self):
        logger.info("===== destroy %s client =====", modConfig.CLIENT_SYSTEM_NAME_1)
