# -*- coding: utf-8 -*-
from ..core.SystemInfo import ROOT_DIR_NAME
from ..core.log.Log import logger

class NotifyManage(object):
    """
    通信管理类
    """

    NAMESPACE = "MODSDKSPRING_{}".format(ROOT_DIR_NAME)
    CLIENT_SYSTEM_NAME = "MODSDKSPRING_NOTIFY_CLIENT_{}".format(ROOT_DIR_NAME)
    SERVER_SYSTEM_NAME = "MODSDKSPRING_NOTIFY_SERVER_{}".format(ROOT_DIR_NAME)
    SERVER_TO_CLIENT = "SERVER_TO_CLIENT"
    CLIENT_TO_SERVER = "CLIENT_TO_SERVER"
    CLIENT_TO_CLIENT = "CLIENT_TO_CLIENT"
    EVENT_METHOD_NAME = "__modsdkspring_method_name__"
    EVENT_ID_LIST = "__modsdkspring_id_list__"
    # 存放当前系统的通过 @AllowNotify 注册的函数
    _functionDict = {}

    @staticmethod
    def registerFunction(func):
        # type: (function) -> None
        """
        注册函数到字典
        """
        key = func.__module__ + '.' + func.__name__
        # 注册一个全限定名称的 key（在方法名称冲突时作为保底方案，调用时需要填写全限定名称）
        NotifyManage._functionDict[key] = func
        # 注册一个只有方法名称的 key（方便调用）
        NotifyManage._functionDict[func.__name__] = func

    @staticmethod
    def callFunction(eventDate):
        # type: (dict) -> None
        """
        调用注册的函数
        """
        key = eventDate.pop(NotifyManage.EVENT_METHOD_NAME, None)
        func = NotifyManage._functionDict.get(key)
        if not func:
            logger.error("调用 Notify 时异常，请检查是否在 %s 方法上添加了 @AllowNotify", key)
            return
        func(eventDate)

def AllowNotify(func):
    # type: (function) -> function
    """
    设置此方法能被框架中的通信方法进行调用
    """
    func.allowNotify = True
    # 在这里直接注册仅仅是为了支持没有绑定实例的函数
    NotifyManage.registerFunction(func)
    return func

def BroadcastToAllClient(methodName, eventData):
    # type: (str, dict) -> 'None'
    """
    服务端广播事件到所有客户端

    Args:
        methodName (str): 客户端方法名称
        eventData (dict): 发送的数据
    """
    # 避免循环引用
    from server.NotifyServer import NotifyServer
    eventData[NotifyManage.EVENT_METHOD_NAME] = methodName
    NotifyServer.getSystem().BroadcastToAllClient(NotifyManage.SERVER_TO_CLIENT, eventData)

def NotifyToClient(targetId, methodName, eventData):
    # type: (str, str, dict) -> 'None'
    """
    服务端发送事件到指定客户端

    Args:
        targetId (str): 客户端玩家 ID
        methodName (str): 客户端方法名称
        eventData (dict): 发送的数据
    """
    # 避免循环引用
    from server.NotifyServer import NotifyServer
    eventData[NotifyManage.EVENT_METHOD_NAME] = methodName
    NotifyServer.getSystem().NotifyToClient(targetId, NotifyManage.SERVER_TO_CLIENT, eventData)

def NotifyToMultiClients(targetIdList, methodName, eventData):
    # type: (list[str], str, dict) -> 'None'
    """
    服务端发送事件到指定一批客户端

    Args:
        targetIdList (list): 客户端玩家 ID 列表
        methodName (str): 客户端方法名称
        eventData (dict): 发送的数据
    """
    # 避免循环引用
    from server.NotifyServer import NotifyServer
    eventData[NotifyManage.EVENT_METHOD_NAME] = methodName
    NotifyServer.getSystem().NotifyToMultiClients(targetIdList, NotifyManage.SERVER_TO_CLIENT, eventData)

def NotifyToServer(methodName, eventData):
    # type: (str, dict) -> 'None'
    """
    客户端发送事件到服务端

    Args:
        methodName (str): 服务端方法名称
        eventData (dict): 发送的数据
    """
    # 避免循环引用
    from client.NotifyClient import NotifyClient
    eventData[NotifyManage.EVENT_METHOD_NAME] = methodName
    NotifyClient.getSystem().NotifyToServer(NotifyManage.CLIENT_TO_SERVER, eventData)

def NotifyFromClientToClient(targetId, methodName, eventData):
    # type: (str | list[str], str, dict) -> 'None'
    """
    客户端发送事件到另一批玩家的客户端

    Args:
        targetId (str | list): 客户端玩家 ID
        methodName (str): 客户端方法名称
        eventData (dict): 发送的数据
    """
    # 避免循环引用
    from client.NotifyClient import NotifyClient
    eventData[NotifyManage.EVENT_METHOD_NAME] = methodName
    targetIdList = targetId
    if not isinstance(targetIdList, list):
        targetIdList = [targetIdList]
    eventData[NotifyManage.EVENT_ID_LIST] = targetIdList
    NotifyClient.getSystem().NotifyToServer(NotifyManage.CLIENT_TO_CLIENT, eventData)