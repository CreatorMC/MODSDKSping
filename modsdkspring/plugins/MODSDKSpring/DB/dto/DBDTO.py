# -*- coding: utf-8 -*-


class DBDTO(object):
    """
    DB 数据传输对象
    """
    KEY = '__modsdkspring_db_key__'
    VALUE = "__modsdkspring_db_value__"
    VERSION = "__modsdkspring_db_version__"
    UID = "__modsdkspring_db_uid__"

    def __init__(self, key, value, version, uid):
        # type: (str, dict, int, str) -> None
        self.key = key                          # key
        self.value = value                      # 自定义数据
        self.version = version                  # 版本号
        self.uid = uid                          # 玩家 UID 字符串，如果此字段有有效值，则服务端存储时需要在 key 后拼接此值

    def parseToDict(self):
        # type: () -> dict
        return {
            DBDTO.KEY: self.key,
            DBDTO.VALUE: self.value,
            DBDTO.VERSION: self.version,
            DBDTO.UID: self.uid
        }

    @staticmethod
    def parseToObject(tempDict):
        # type: (dict) -> 'DBDTO'
        key = tempDict[DBDTO.KEY]
        value = tempDict.get(DBDTO.VALUE, {})
        version = tempDict.get(DBDTO.VERSION, 0)
        uid = tempDict.get(DBDTO.UID, '')
        return DBDTO(key, value, version, uid)
