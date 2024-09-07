# -*- coding: utf-8 -*-
from multipleModScripts.plugins.MODSDKSpring.core.ListenEvent import ListenEvent
from multipleModScripts.plugins.MODSDKSpring.core.Autowired import Autowired
from multipleModScripts.plugins.MODSDKSpring.core.BeanFactory import BeanFactory
from multipleModScripts.plugins.MODSDKSpring.core.constant import SystemType
from multipleModScripts.modCommon import modConfig
from multipleModScripts.plugins.MODSDKSpring.core.log.Log import logger

@ListenEvent.InitComponentClient(namespace=modConfig.MOD_NAMESPACE, systemName=modConfig.CLIENT_SYSTEM_NAME)
class AMultipleClientComponent(object):

    @Autowired
    def __init__(self, client, aCopyClientComponent):
        self.client = client
        # aCopyClientComponent 将为 None，不要这样做，这是错误用法！
        # 如果您需要跨系统的进行组件调用，请使用 getBean() 方法。
        self.aCopyClientComponent = aCopyClientComponent
        logger.info("AMultipleClientComponent 错误的获取到了：" + str(aCopyClientComponent))
        logger.info("AMultipleClientComponent 获取到的系统：" + str(client))
    
    @ListenEvent.Client(eventName="UiInitFinished")
    def uiInitFinished(self, event):
        # 跨系统调用组件的正确用法
        self.aCopyClientComponent = BeanFactory.getBean(SystemType.CLIENT, 'aCopyClientComponent')
        logger.info("AMultipleClientComponent 正确的获取到了：" + str(self.aCopyClientComponent))