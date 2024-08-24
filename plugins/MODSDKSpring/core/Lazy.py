# -*- coding: utf-8 -*-
from Autowired import Autowired
from exception.DecoratorUseException import DecoratorUseException

class Lazy:
    """
    添加到 @Autowired 上的装饰器，表示此方法在进行依赖注入时先用 None 进行注入，对象创建之后再注入真正需要的依赖

    此装饰器一般用于解决循环依赖
    """
    
    def __init__(self, autowired):
        if not isinstance(autowired, Autowired):
            raise DecoratorUseException("@Lazy 必须添加在 @Autowired 的上方。")
        self.autowired = autowired

    def __call__(self, *args, **kwargs):
        return self.autowired(*args, **kwargs)