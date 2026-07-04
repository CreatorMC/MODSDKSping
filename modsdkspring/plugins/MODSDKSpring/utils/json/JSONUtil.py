# -*- coding: utf-8 -*-
import base64


class JSONUtil(object):

    # 将常用类型检查移出循环或缓存起来
    _unicodeType = unicode
    _listType = list
    _dictType = dict

    @staticmethod
    def convertUnicodeToStr(obj):
        """
        递归地将所有 unicode 字符串转换为 str
        """

        # 1. 快速路径：如果是字符串，直接处理并返回，避免后续的类型检查
        if isinstance(obj, JSONUtil._unicodeType):
            return obj.encode('utf-8')

        # 2. 列表处理：使用局部变量缓存方法和类型，减少全局查找
        elif isinstance(obj, JSONUtil._listType):
            convert = JSONUtil.convertUnicodeToStr
            return [convert(item) for item in obj]

        # 3. 字典处理：使用 .iteritems() (PY2) 节省内存，缓存方法
        elif isinstance(obj, JSONUtil._dictType):
            convert = JSONUtil.convertUnicodeToStr
            return {convert(key): convert(value) for key, value in obj.iteritems()}

        # 4. 其他类型直接返回
        else:
            return obj

    @staticmethod
    def safeEncode(obj):
        """
        将对象安全的转为 json.dumps 能够编码的对象
        """

        if isinstance(obj, str):
            try:
                return obj.decode('utf-8')
            except UnicodeDecodeError:
                # 用特殊标记包装，用于识别
                return {'__modsdkspring_db_binary__': True, 'data': base64.b64encode(obj).decode('ascii')}
        elif isinstance(obj, dict):
            return {JSONUtil.safeEncode(k): JSONUtil.safeEncode(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [JSONUtil.safeEncode(item) for item in obj]
        else:
            return obj

    @staticmethod
    def safeDecode(obj):
        """
        将 safeEncode 编码的对象安全解码
        """

        if isinstance(obj, dict) and obj.get('__modsdkspring_db_binary__') is True:
            return base64.b64decode(obj['data'])
        elif isinstance(obj, dict):
            return {k: JSONUtil.safeDecode(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [JSONUtil.safeDecode(item) for item in obj]
        else:
            return obj
