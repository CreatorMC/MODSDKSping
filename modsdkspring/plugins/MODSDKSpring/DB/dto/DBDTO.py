# -*- coding: utf-8 -*-


class DBDTO(object):
    """
    DB 数据传输对象
    """
    KEY = '__modsdkspring_db_key__'
    VALUE = "__modsdkspring_db_value__"
    VERSION = "__modsdkspring_db_version__"
    UID = "__modsdkspring_db_uid__"

    # 操作枚举值
    INSERT = 0      # 增
    DELETE = 1      # 删
    UPDATE = 2      # 改
    SELECT = 3      # 查

    # 优化内存
    __slots__ = ["key", "value", "version", "uid", "operation", "subkey", "requestId", "extraValue"]

    def __init__(self, key, value, version, uid, operation=SELECT):
        # type: (str, dict, int, str, int) -> None
        self.key = key                          # key
        self.value = value                      # 自定义数据
        self.version = version                  # 版本号
        self.uid = uid                          # 玩家 UID 字符串，如果此字段有有效值，则服务端存储时需要在 key 后拼接此值

        # 非持久化字段
        self.operation = operation              # 操作标识，用于服务端拒绝更新时的客户端操作判断
        self.subkey = ''                        # UPDATE 操作时保存的子键
        self.requestId = ''                     # 请求 ID，用于对应消息队列中的请求
        self.extraValue = {}                    # 额外的用于事件回调的自定义字典

    def mergeDTO(self, newDTO):
        # type: ('DBDTO') -> None
        """
        合并新的 DTO
        如果当前 DTO 的操作类型是 INSERT 或 DELETE，则只更新当前版本号为 newDTO 的版本号
        如果当前 DTO 的操作类型是 UPDATE，则执行特殊合并规则
        如果当前 DTO 的操作类型是 SELECT，则什么都不执行
        """
        if self.operation == DBDTO.INSERT or self.operation == DBDTO.DELETE:
            self.version = newDTO.version

        elif self.operation == DBDTO.UPDATE:
            self.version = newDTO.version
            targetSubKeyValue = self.value.get(self.subkey, None)
            self.value = newDTO.value
            self.value[self.subkey] = targetSubKeyValue

    def parseToDict(self):
        # type: () -> dict
        return {
            DBDTO.KEY: self.key,
            DBDTO.VALUE: self.value,
            DBDTO.VERSION: self.version,
            DBDTO.UID: self.uid,
            'operation': self.operation,
            'subkey': self.subkey,
            'requestId': self.requestId,
            'extraValue': self.extraValue
        }

    def parseToSave(self):
        # type: () -> dict
        """
        持久化专用
        """
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
        operation = tempDict.get('operation', DBDTO.SELECT)
        subkey = tempDict.get('subkey', '')
        requestId = tempDict.get('requestId', '')
        extraValue = tempDict.get('extraValue', {})
        dto = DBDTO(key, value, version, uid, operation)
        dto.subkey = subkey
        dto.requestId = requestId
        dto.extraValue = extraValue
        return dto
