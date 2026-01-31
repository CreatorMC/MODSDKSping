# -*- coding: utf-8 -*-

class SystemInfo(object):
    """
    系统信息类
    """

    # 线程 ID
    clientThreadId = None
    serverThreadId = None

    def __init__(self):
        pass

ROOT_DIR_NAME = SystemInfo.__module__.split('.')[0]

def isClientThread():
    from threading import current_thread
    return SystemInfo.clientThreadId is not None and SystemInfo.clientThreadId == current_thread().ident

def isServerThread():
    from threading import current_thread
    return SystemInfo.serverThreadId is not None and SystemInfo.serverThreadId == current_thread().ident