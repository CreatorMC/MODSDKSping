# -*- coding: utf-8 -*-

class DecoratorUseException(Exception):
    """
    装饰器使用异常
    """
    
    def __init__(self, error_message):
        super(DecoratorUseException, self).__init__(error_message)