# -*- coding: utf-8 -*-
from ClientSystem import ClientSystem
from ServerSystem import ServerSystem
from plugins.MODSDKSpring.core.BeanFactory import BeanFactory
import plugins.MODSDKSpring.core.constant.SystemType as SystemType

clientSystem = ClientSystem('tms', 'ClientSystem')
serverSystem = ServerSystem('tms', 'ServerSystem')
print(BeanFactory.getBean(SystemType.CLIENT, 'testClientComponent'))