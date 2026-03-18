# -*- coding: utf-8 -*-


class JSONUtil(object):
    """
    JSON 工具类
    """

    @staticmethod
    def convertUnicodeToStr(obj):
        """
        递归地将所有 unicode 字符串转换为 str
        """
        if isinstance(obj, unicode):
            return obj.encode('utf-8')
        elif isinstance(obj, list):
            return [JSONUtil.convertUnicodeToStr(item) for item in obj]
        elif isinstance(obj, dict):
            return {JSONUtil.convertUnicodeToStr(key): JSONUtil.convertUnicodeToStr(value) for key, value in obj.iteritems()}
        else:
            return obj
