# -*- coding: utf-8 -*-

class NetWorkException(Exception):
    """
    通信模块异常
    """
    
    def __init__(self, error_message):
        super(NetWorkException, self).__init__(error_message)