# -*- coding: utf-8 -*-

from mod.common.mod import Mod
import mod.client.extraClientApi as clientApi
import mod.server.extraServerApi as serverApi
from modCommon import modConfig
from mod_log import logger

@Mod.Binding(name=modConfig.MOD_NAMESPACE, version=modConfig.MOD_VERSION)
class [MOD_NAME](object):

    def __init__(self):
        logger.info("===== init %s mod =====", modConfig.MOD_NAMESPACE)

    @Mod.InitServer()
    def [MOD_NAME]ServerInit(self):
        logger.info("===== init %s server =====", modConfig.SERVER_SYSTEM_NAME)
        serverApi.RegisterSystem(modConfig.MOD_NAMESPACE, modConfig.SERVER_SYSTEM_NAME, modConfig.SERVER_SYSTEM_CLS_PATH)

    @Mod.DestroyServer()
    def [MOD_NAME]ServerDestroy(self):
        logger.info("===== destroy %s server =====", modConfig.SERVER_SYSTEM_NAME)
    
    @Mod.InitClient()
    def [MOD_NAME]ClientInit(self):
        logger.info("===== init %s client =====", modConfig.CLIENT_SYSTEM_NAME)
        clientApi.RegisterSystem(modConfig.MOD_NAMESPACE, modConfig.CLIENT_SYSTEM_NAME, modConfig.CLIENT_SYSTEM_CLS_PATH)
    
    @Mod.DestroyClient()
    def [MOD_NAME]ClientDestroy(self):
        logger.info("===== destroy %s client =====", modConfig.CLIENT_SYSTEM_NAME)
