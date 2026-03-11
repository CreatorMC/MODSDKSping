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
        factory = clientApi.GetEngineCompFactory()
        levelId = clientApi.GetLevelId()

        # 用于调用网易存储接口
        comp = factory.CreateConfigClient(levelId)
        self.set = comp.SetConfigData
        self.get = comp.GetConfigData

        # 用于超时重传
        comp = factory.CreateGame(levelId)
        self.addTimer = comp.AddTimer
        self.cancelTimer = comp.CancelTimer
        # 超时定时器按 key 管理
        self.timerDict = {}

    def _set(self, dto):
        # type: (DBDTO) -> bool
        # 客户端不需要检查版本（由网易接口保证服务端发到客户端的顺序性，服务端发过来的，一定是最新的）
        result = self.set(dto.key, dto.parseToSave(), False)

        # 借由通信系统发送本地广播事件，通知该 MOD 内的数据变化
        NotifyClient.getSystem().BroadcastEvent(DB_CHANGE_EVENT, dto.value)
        return result

    def _get(self, key, uid):
        """
        因为这里直接取的本地数据，用本地数据构造 dto，所以在服务端还没有返回给客户端的时候，客户端此时对数据的任何操作，均无效（客户端取的 version 均未改变）
        """
        tempDict = self.get(key, False)
        if tempDict is None:
            tempDict = {}
        tempDict[DBDTO.KEY] = key
        dto = DBDTO.parseToObject(tempDict)
        dto.uid = str(uid)
        return dto

    # noinspection PyMethodMayBeStatic
    def _pushAndSendDTO(self, dto):
        isEmpty = MessageQueue.isEmpty(dto.key)
        MessageQueue.push(dto)
        if isEmpty:
            # 只有之前是空队列，才会发送请求到服务端，避免重复发送
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

        dto = self._get(key, uid)
        dto.value = value
        dto.operation = DBDTO.INSERT
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
        dto = self._get(key, uid)
        dto.value = {}
        dto.operation = DBDTO.DELETE
        self._pushAndSendDTO(dto)

    def update(self, key, subkey, value, uid=''):
        # type: (str, str, any, '(str | int)') -> None
        """
        更新 key 对应数据中的 subkey 对应的数据
        key: 标识符。如果没有，则自动添加
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
        dto = self._get(key, uid)
        dto.value[subkey] = value
        dto.operation = DBDTO.UPDATE
        dto.subkey = subkey
        self._pushAndSendDTO(dto)

    def select(self, key):
        # type: (str) -> dict
        """
        查询 key 对应的数据
        key: 标识符
        备注：数据不存在时会返回空字典：{}
        """
        dto = self._get(key, '')
        dto.operation = DBDTO.SELECT
        return dto.value


clientDB = ClientDB()


def _sendDBMessage(key):
    # type: (str) -> None
    """
    从消息队列中取数据发送给服务端
    """
    # 取消超时定时器
    if key in clientDB.timerDict and clientDB.timerDict[key]:
        clientDB.cancelTimer(clientDB.timerDict[key])
        del clientDB.timerDict[key]

    dto = MessageQueue.get(key)
    if dto:
        dtoDict = dto.parseToDict()
        dtoDict['playerId'] = clientApi.GetLocalPlayerId()
        NotifyToServer(
            '_receiveClientDBMessage',
            dtoDict
        )
        # 启动超时定时器，当请求超时时，尝试重新发送
        clientDB.timerDict[key] = clientDB.addTimer(10.0, _sendDBMessage, key)


# noinspection PyProtectedMember
@AllowNotify
def _receiveServerDBMessage(event):
    """
    接收从客户端发到服务端的数据更新回调（从服务端发起的更新不调用此函数）
    """
    responseDTO = ResponseDTO.parseToObject(event)
    if responseDTO.playerId != clientApi.GetLocalPlayerId():
        # 如果不是当前玩家发送的请求回调，则调用另一个函数
        _receiveFromServerDBMessage(event)
        return

    newDTO = responseDTO.dto
    oldDTO = MessageQueue.pop(newDTO.key)

    if responseDTO.result:
        # 服务端更新成功，客户端保存
        clientDB._set(newDTO)
    else:
        # 服务端更新失败，客户端根据操作类型进行合并
        oldDTO.mergeDTO(newDTO)
        # 合并后重发请求（放入队首，避免操作顺序问题）
        MessageQueue.pushFront(oldDTO)

    # 继续从队列中取数据发送
    _sendDBMessage(newDTO.key)


# noinspection PyProtectedMember
@AllowNotify
def _receiveFromServerDBMessage(event):
    """
    接收从服务端发起的更新
    """
    responseDTO = ResponseDTO.parseToObject(event)

    # 服务端更新成功，客户端直接存储，服务端更新失败则客户端直接丢弃
    if responseDTO.result:
        clientDB._set(responseDTO.dto)
