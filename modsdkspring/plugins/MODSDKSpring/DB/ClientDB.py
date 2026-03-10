# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi

from .BaseDB import BaseDB, DB_CHANGE_EVENT
from .dto.DBDTO import DBDTO
from .dto.ResponseDTO import ResponseDTO
from .utils.MessageQueue import MessageQueue
from ..Network.NotifyManage import NotifyToServer, AllowNotify
from ..Network.client.NotifyClient import NotifyClient


class ClientDB(BaseDB):

    def __init__(self):
        super(ClientDB, self).__init__()
        comp = clientApi.GetEngineCompFactory().CreateConfigClient(clientApi.GetLevelId())
        self.set = comp.SetConfigData
        self.get = comp.GetConfigData

    def _set(self, dto):
        # type: (DBDTO) -> bool
        # TODO 客户端需要检查版本吗？
        result = self.set(dto.key, dto.parseToDict(), False)

        # 借由通信系统发送本地广播事件，通知该 MOD 内的数据变化
        NotifyClient.getSystem().BroadcastEvent(DB_CHANGE_EVENT, dto.value)
        return result

    def _get(self, key):
        tempDict = self.get(key, False)
        if tempDict is None:
            tempDict = {}
        tempDict[DBDTO.KEY] = key
        return DBDTO.parseToObject(tempDict)

    def _getDTO(self, key, uid):
        """
        因为这里直接取的本地数据，用本地数据构造 dto，所以在服务端还没有返回给客户端的时候，客户端此时对数据的任何操作，均无效
        """
        dto = self._get(key)
        dto.uid = str(uid)
        return dto

    # noinspection PyMethodMayBeStatic
    def _pushAndSendDTO(self, dto):
        MessageQueue.push(dto)
        _sendDBMessage(dto.key)

    def insert(self, key, value, uid=''):
        # type: (str, '(dict | None)', '(str | int)') -> None
        """
        插入数据
        key: 标识符
        value: 数据字典
        uid: 玩家 UID，当插入的数据是玩家私有数据时需要设置
        备注：key 如果已存在，则为更新数据
        玩家 UID 不要使用服务端接口 GetPlayerUid 获取，可能与客户端接口 getUid 获取的不一致
        """
        if value is None:
            value = {}

        dto = self._getDTO(key, uid)
        dto.value = value
        self._pushAndSendDTO(dto)

    def delete(self, key, uid=''):
        # type: (str, '(str | int)') -> None
        """
        删除数据
        key: 标识符
        uid: 玩家 UID，当删除的数据是玩家私有数据时需要设置
        备注：受限于网易接口，客户端只能做到将 key 对应的数据清空为 {}，key 本身依然存在
        服务端会将 key 本身也删除
        玩家 UID 不要使用服务端接口 GetPlayerUid 获取，可能与客户端接口 getUid 获取的不一致
        """
        self.insert(key, {}, uid)

    def update(self, key, subkey, value, uid=''):
        # type: (str, str, any, '(str | int)') -> None
        """
        更新 key 对应数据中的 subkey 对应的数据
        key: 标识符
        subkey: key 对应数据中的子键。如果没有，则自动添加
        value: 更新的数据
        uid: 玩家 UID，当更新的数据是玩家私有数据时需要设置
        备注：玩家 UID 不要使用服务端接口 GetPlayerUid 获取，可能与客户端接口 getUid 获取的不一致
        当你用 key 存储了以下格式的数据时：

        ```python
        {
            "a": 1,
            "b": 1
        }
        ```

        当 subkey 为 "a"，value 为 2 时，key 对应的数据会被更新为以下格式：

        ```python
        {
            "a": 2,
            "b": 1
        }
        ```

        如果 key 对应的数据过多，且需要频繁的更新 subkey 对应的数据，建议在业务层面将 subkey 提升为 key，以提高效率
        """
        dto = self._getDTO(key, uid)
        dto.value[subkey] = value
        self._pushAndSendDTO(dto)

    def select(self, key):
        # type: (str) -> dict
        """
        查询 key 对应的数据
        key: 标识符
        """
        dto = self._getDTO(key, '')
        return dto.value


clientDB = ClientDB()


def _sendDBMessage(key):
    # type: (str) -> None
    """
    从消息队列中取数据发送给服务端
    """
    dto = MessageQueue.get(key)
    if dto:
        dtoDict = dto.parseToDict()
        dtoDict['playerId'] = clientApi.GetLocalPlayerId()
        NotifyToServer(
            '_receiveClientDBMessage',
            dtoDict
        )


# noinspection PyProtectedMember
@AllowNotify
def _receiveServerDBMessage(event):
    """
    接收服务端的数据更新回调
    """
    responseDTO = ResponseDTO.parseToObject(event)
    dto = responseDTO.dto
    MessageQueue.pop(dto.key)                                               # 从队列中弹出
    clientDB._set(dto)                                                      # 更新数据到本地
    _sendDBMessage(dto.key)                                                 # 继续从队列中取数据发送
