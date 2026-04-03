# -*- coding: utf-8 -*-
from mod_log import logger as lg


class SpringLogger(object):
    """
    自定义日志包装器
    强制添加自定义前缀
    """

    def __init__(self, baseLogger, prefix):
        self._logger = baseLogger
        self._prefix = prefix

    def _formatMsg(self, msg):
        # 确保前缀被添加，同时兼容 msg 已经是字符串的情况
        return "{} {}".format(self._prefix, msg)

    def info(self, msg, *args, **kwargs):
        self._logger.info(self._formatMsg(msg), *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self._logger.debug(self._formatMsg(msg), *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._logger.warning(self._formatMsg(msg), *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._logger.error(self._formatMsg(msg), *args, **kwargs)


logger = SpringLogger(lg, "[MODSDKSpring]")
