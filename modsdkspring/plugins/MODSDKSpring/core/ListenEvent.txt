# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
import mod.server.extraServerApi as serverApi
import inspect
import functools
import constant.SystemType as SystemType
import constant.Target as Target
from log.Log import logger
from BeanFactory import BeanFactory
from Autowired import Autowired
from Lazy import Lazy
ClientSystem = clientApi.GetClientSystemCls()
ServerSystem = serverApi.GetServerSystemCls()

class ListenEvent(object):
    """
    处理事件监听的类
    """

    @staticmethod
    def InitClient(cls):
        """
        添加在被 modMain.py 注册的客户端类的上方，开启框架相关功能
        """
        return ListenEvent.Init(cls, SystemType.CLIENT)

    @staticmethod
    def InitServer(cls):
        """
        添加在被 modMain.py 注册的服务端类的上方，开启框架相关功能
        """
        return ListenEvent.Init(cls, SystemType.SERVER)

    @staticmethod
    def InitComponentClient(cls = None, namespace = Target.DEFAULT, systemName = Target.DEFAULT):
        """
        添加到自定义的客户端 Component 类的上方，开启框架相关功能

        Args:
            namespace (str, optional): 注入的客户端系统的命名空间，当 modMain.py 中只注册了一个客户端时不用填写此参数
            systemName (str, optional): 注入的客户端系统的系统名称，当 modMain.py 中只注册了一个客户端时不用填写此参数
        """
        if cls:
            return ListenEvent.InitComponent(cls, SystemType.CLIENT, namespace, systemName)

        def wrapper(clazz):
            return ListenEvent.InitComponent(clazz, SystemType.CLIENT, namespace, systemName)

        return wrapper

    @staticmethod
    def InitComponentServer(cls = None, namespace = Target.DEFAULT, systemName = Target.DEFAULT):
        """
        添加到自定义的服务端 Component 类的上方，开启框架相关功能

        Args:
            namespace (str, optional): 注入的服务端系统的命名空间，当 modMain.py 中只注册了一个服务端时不用填写此参数
            systemName (str, optional): 注入的服务端系统的系统名称，当 modMain.py 中只注册了一个服务端时不用填写此参数
        """
        if cls:
            return ListenEvent.InitComponent(cls, SystemType.SERVER, namespace, systemName)

        def wrapper(clazz):
            ListenEvent.InitComponent(clazz, SystemType.SERVER, namespace, systemName)

        return wrapper

    @staticmethod
    def Init(cls, systemType):
        """
        添加在被 modMain.py 注册的类的上方，开启框架相关功能 (不能直接使用)

        Args:
            systemType (str): 系统的类型，请使用常量 SystemType.CLIENT 或 SystemType.SERVER
        """
        # 记录原本的构造方法
        origInit = cls.__init__
        # 记录原本的 Destroy 方法
        origDestroy = cls.Destroy

        def newInit(self, namespace, systemName, *args, **kwargs):
            if isinstance(self, ServerSystem):
                ServerSystem.__init__(self, namespace, systemName)
            elif isinstance(self, ClientSystem):
                ClientSystem.__init__(self, namespace, systemName)

            # 处理监听
            ListenEvent.listenEvent(cls, self, self)

            # 处理带 @InitComponent 的 Bean 的创建和依赖注入
            BeanFactory.createBean(self, systemType, namespace, systemName)

            # 处理当前自己的依赖注入
            dependenceList = [namespace, systemName]
            dependenceList.extend(BeanFactory.createBeanWithInit(cls, self, systemType, namespace, systemName))

            # 最后一次依赖注入 (解决循环依赖对象的注入)
            BeanFactory.dependenceInjectLast(systemType)

            # 清理不需要的变量，以节省内存
            BeanFactory.clearNoNeedVariable(systemType)

            logger.info("%s 系统创建成功", cls.__name__)
            # 执行原来的初始化方法
            origInit(self, *dependenceList)

        def newDestroy(self):
            self.UnListenAllEvents()
            origDestroy(self)

        # 检查装饰器
        ListenEvent.checkDecorator(origInit, newInit)

        # 用新的方法覆盖原来的方法
        cls.__init__ = newInit
        cls.Destroy = newDestroy
        return cls

    @staticmethod
    def InitComponent(cls, systemType, targetNamespace, targetSystemName):
        """
        添加到自定义的 Component 类的上方，开启框架相关功能 (不能直接使用)

        Args:
            systemType (str): 系统的类型，请使用常量 SystemType.CLIENT 或 SystemType.SERVER
            targetNamespace (str): 注入的系统的命名空间，如果值为 Target.DEFAULT 则不判断注入的系统对象的命名空间
            targetSystemName (str): 注入的系统的系统名称，如果值为 Target.DEFAULT 则不判断注入的系统对象的系统名称
        """
        origInit = cls.__init__
        
        def newInit(self, system, *args, **kwargs):

            # 处理监听
            ListenEvent.listenEvent(cls, system, self)

            logger.info("%s 组件创建成功", cls.__name__)
            origInit(self, system, *args, **kwargs)

        # 检查装饰器
        ListenEvent.checkDecorator(origInit, newInit)

        cls.__init__ = newInit
        BeanFactory.componentClsDict[systemType][cls.__name__[0].lower() + cls.__name__[1:]] = [ cls, targetNamespace, targetSystemName ]
        return cls

    @staticmethod
    def Client(eventName, namespace = clientApi.GetEngineNamespace(), systemName = clientApi.GetEngineSystemName(), priority = 0):
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
    def Server(eventName, namespace = clientApi.GetEngineNamespace(), systemName = clientApi.GetEngineSystemName(), priority = 0):
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
    def listenEvent(cls, system, component):
        """
        处理监听

        Args:
            cls (type): 要监听的类型本身
            system (ClientSystem | ServerSystem): 被注册的客户端或服务端对象
            component (object): 客户端或服务端组件对象
        """
        members = inspect.getmembers(cls, predicate=inspect.ismethod)
        for name, method in members:
            if "eventName" in method.__dict__:
                if isinstance(system, ClientSystem) or isinstance(system, ServerSystem):
                    system.ListenForEvent(method.namespace, method.systemName, method.eventName, component, method, method.priority)

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