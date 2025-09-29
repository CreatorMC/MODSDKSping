# -*- coding: utf-8 -*-
from exception.DecoratorUseException import DecoratorUseException

class Autowired:
    """
    添加到 __init__ 方法上的装饰器，表示此方法需要依赖注入
    """
    
    def __init__(self, function):
        if function.__name__ != '__init__':
            raise DecoratorUseException("方法 %s 不是 __init__，不能使用 @Autowired 装饰器。" % function.__name__)
        self.function = function

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)