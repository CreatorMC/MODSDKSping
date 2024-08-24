# -*- coding: utf-8 -*-

class BeanCurrentlyInCreationException(Exception):
    """
    Bean 创建异常
    """
    
    def __init__(self, error_message):
        super(BeanCurrentlyInCreationException, self).__init__(error_message)