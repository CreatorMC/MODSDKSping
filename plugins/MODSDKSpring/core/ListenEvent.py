# -*- coding: utf-8 -*-
import inspect
import functools
import constant.SystemType as SystemType
from BeanFactory import BeanFactory
from Autowired import Autowired
from Lazy import Lazy
# ClientSystem = clientApi.GetClientSystemCls()
# ServerSystem = serverApi.GetServerSystemCls()
ClientSystem = object
ServerSystem = object

class ListenEvent(object):
    """
    处理事件监听的类
    """

    @staticmethod
    def InitClient(cls):
        """
        添加在被 modMain.py 注册的客户端类的上方，创建对象时触发
        """
        return ListenEvent.Init(cls, SystemType.CLIENT)

    @staticmethod
    def InitServer(cls):
        """
        添加在被 modMain.py 注册的服务端类的上方，创建对象时触发
        """
        return ListenEvent.Init(cls, SystemType.SERVER)

    @staticmethod
    def InitComponentClient(cls):
        """
        添加到自定义的客户端 Component 类的上方，创建对象时触发
        """
        return ListenEvent.InitComponent(cls, SystemType.CLIENT)

    @staticmethod
    def InitComponentServer(cls):
        """
        添加到自定义的服务端 Component 类的上方，创建对象时触发
        """
        return ListenEvent.InitComponent(cls, SystemType.SERVER)

    @staticmethod
    def Init(cls, systemType):
        """
        添加在被 modMain.py 注册的类的上方，创建对象时触发 (不推荐使用)

        Args:
            systemType (str): 系统的类型，请使用常量 SystemType.CLIENT 或 SystemType.SERVER
        """
        # 记录原本的构造方法
        origInit = cls.__init__

        def newInit(self, namespace, systemName, *args, **kwargs):
            # super(cls, self).__init__(namespace, systemName)
            super(cls, self).__init__()

            # 处理监听
            ListenEvent.listenEvent(cls, self)

            # 处理带 @InitComponent 的 Bean 的创建和依赖注入
            BeanFactory.createBean(self, systemType)

            # 处理当前自己的依赖注入
            dependenceList = [namespace, systemName]
            dependenceList.extend(BeanFactory.createBeanWithInit(cls, self, systemType))

            # 最后一次依赖注入 (解决循环依赖对象的注入)
            BeanFactory.dependenceInjectLast(systemType)

            print(cls.__name__ + " system created!")
            # 执行原来的初始化方法
            origInit(self, *dependenceList)

        # 检查装饰器
        ListenEvent.checkDecorator(origInit, newInit)

        # 用新的方法覆盖原来的方法
        cls.__init__ = newInit
        return cls

    @staticmethod
    def InitComponent(cls, systemType):
        """
        添加到自定义的 Component 类的上方，创建对象时触发 (不推荐使用)

        Args:
            systemType (str): 系统的类型，请使用常量 SystemType.CLIENT 或 SystemType.SERVER
        """
        origInit = cls.__init__
        
        def newInit(self, system, *args, **kwargs):

            # 处理监听
            ListenEvent.listenEvent(cls, system)

            print(cls.__name__ + " object created!")
            origInit(self, system, *args, **kwargs)

        # 检查装饰器
        ListenEvent.checkDecorator(origInit, newInit)

        cls.__init__ = newInit
        BeanFactory.componentClsDict[systemType][cls.__name__[0].lower() + cls.__name__[1:]] = cls
        return cls

    @staticmethod
    def Client(eventName, namespace = "namespace", systemName = "systemName", priority = 0):
        """
        客户端监听事件
        Args:
            eventName (str): 监听的事件名称
            namespace (str, optional): 所监听事件的来源系统的 namespace。默认值为 clientApi.GetEngineNamespace()。
            systemName (str, optional): 所监听事件的来源系统的 systemName。默认值为 clientApi.GetEngineSystemName()。
            priority (int, optional): 回调函数的优先级。默认值为 0，这个数值越大表示被执行的优先级越高，最高为10。
        """
        def register(func):

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                func(*args, **kwargs)
            
            wrapper.eventName = eventName
            wrapper.namespace = namespace
            wrapper.systemName = systemName
            wrapper.priority = priority
            return wrapper
        return register

    @staticmethod
    def Server(eventName, namespace = "namespace", systemName = "systemName", priority = 0):
        """
        服务端监听事件
        Args:
            eventName (str): 监听的事件名称
            namespace (str, optional): 所监听事件的来源系统的 namespace。默认值为 clientApi.GetEngineNamespace()。
            systemName (str, optional): 所监听事件的来源系统的 systemName。默认值为 clientApi.GetEngineSystemName()。
            priority (int, optional): 回调函数的优先级。默认值为 0，这个数值越大表示被执行的优先级越高，最高为10。
        """
        def register(func):

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                func(*args, **kwargs)
            
            wrapper.eventName = eventName
            wrapper.namespace = namespace
            wrapper.systemName = systemName
            wrapper.priority = priority
            return wrapper
        return register

# region 功能方法，使用者不应该显式调用此部分！

    @staticmethod
    def listenEvent(cls, system):
        """
        处理监听

        Args:
            cls (type): 要监听的类型本身
            system (ClientSystem | ServerSystem): 被注册的客户端或服务端对象
        """
        members = inspect.getmembers(cls, predicate=inspect.ismethod)
        for name, method in members:
            if "eventName" in method.__dict__:
                if isinstance(system, ClientSystem) or isinstance(system, ServerSystem):
                    print("Name Space: " + method.namespace + "\nSystem Name: " + method.systemName + "\nListen Event: " + method.eventName + "\nPriority: " + str(method.priority))
                    # system.ListenForEvent(method.namespace, method.systemName, method.eventName, system, method, method.priority)

    @staticmethod
    def checkDecorator(origInit, newInit):
        """
        检查原始构造方法上的装饰器，并根据装饰器类型，给新构造方法赋值

        Args:
            origInit (method): 原始构造方法
            newInit (method): 新构造方法
        """
        # 如果方法最上方是 @Lazy
        if isinstance(origInit, Lazy):
            newInit.lazy = True
            newInit.args = inspect.getargspec(origInit.autowired.function).args
        # 如果方法最上方是 @Autowired
        elif isinstance(origInit, Autowired):
            # 存储此构造方法的参数名称列表
            newInit.args = inspect.getargspec(origInit.function).args

# endregion