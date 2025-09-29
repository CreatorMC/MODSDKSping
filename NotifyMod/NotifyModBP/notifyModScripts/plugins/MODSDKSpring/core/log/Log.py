# -*- coding: utf-8 -*-
import logging

class LogAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return ('[MODSDKSpring] ' + msg, kwargs)

# 使用适配器
logger = LogAdapter(logging.getLogger('MODSDKSpring'), {})