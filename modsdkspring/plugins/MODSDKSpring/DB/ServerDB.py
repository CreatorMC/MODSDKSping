# -*- coding: utf-8 -*-
import mod.server.extraServerApi as serverApi

from .BaseDB import BaseDB, DB_CHANGE_EVENT
from .dto.DBDTO import DBDTO
from .dto.ResponseDTO import ResponseDTO
from ..Network.NotifyManage import AllowNotify, NotifyToClient, BroadcastToAllClient
from ..Network.server.NotifyServer import NotifyServer
from ..core.log.Log import logger


class ServerDB(BaseDB):
    
    def __init__(self):
        super(ServerDB, self).__init__()
        comp = serverApi.GetEngineCompFactory().CreateExtraData(serverApi.GetLevelId())
        self.set = comp.SetExtraData
        self.get = comp.GetExtraData
        self.clean = comp.CleanExtraData

    def _change(self, dto, func):
        # type: (DBDTO, 'function') -> 'tuple[bool, DBDTO]'
        oldDTO = self._get(dto.key, dto.uid)

        # 版本判断
        if dto.version >= oldDTO.version:
            dto.version += 1

            # 私有 key 拼接（不改变 dto 中的 key）
            key = dto.key
            if dto.uid:
                key = dto.key + dto.uid

            func(key, dto)

            # 借由通信系统发送本地广播事件，通知该 MOD 内的数据变化
            NotifyServer.getSystem().BroadcastEvent(DB_CHANGE_EVENT, dto.value)
            return True, dto

        return False, oldDTO

    def _set(self, dto):
        # type: (DBDTO) -> 'tuple[bool, DBDTO]'
        return self._change(dto, lambda k, d: self.set(k, d.parseToDict(), True))

    def _get(self, key, uid):
        # type: (str, str) -> 'DBDTO'
        uid = str(uid)
        tempDict = self.get(key + uid)
        if tempDict is None:
            tempDict = {}
        tempDict[DBDTO.KEY] = key
        dto = DBDTO.parseToObject(tempDict)
        dto.uid = uid
        return dto

    def _clean(self, dto):
        # type: (DBDTO) -> 'tuple[bool, DBDTO]'
        return self._change(dto, lambda k, d: self.clean(k))

    def insert(self, key, value, uid='', playerId=''):
        # type: (str, '(dict | None)', '(str | int)', str) -> None
        """
        插入数据
        key: 标识符
        value: 数据字典
        uid: 玩家 UID，当插入的数据是玩家私有数据时需要设置
        playerId: 玩家 playerId，当插入的数据是玩家私有数据时需要设置
        备注：key 如果已存在，则为更新数据
        玩家 UID 不要使用服务端接口 GetPlayerUid 获取，可能与客户端接口 getUid 获取的不一致
        """
        dto = self._get(key, uid)
        dto.value = value
        result, newDTO = self._set(dto)
        _sendDBMessage(result, newDTO, playerId)

    def delete(self, key, uid='', playerId=''):
        # type: (str, '(str | int)', str) -> None
        """
        删除数据
        key: 标识符
        uid: 玩家 UID，当删除的数据是玩家私有数据时需要设置
        playerId: 玩家 playerId，当插入的数据是玩家私有数据时需要设置
        备注：受限于网易接口，客户端只能做到将 key 对应的数据清空为 {}，key 本身依然存在
        服务端会将 key 本身也删除
        玩家 UID 不要使用服务端接口 GetPlayerUid 获取，可能与客户端接口 getUid 获取的不一致
        """
        dto = self._get(key, uid)
        dto.value = {}
        result, newDTO = self._clean(dto)
        _sendDBMessage(result, newDTO, playerId)

    def update(self, key, subkey, value, uid='', playerId=''):
        # type: (str, str, any, '(str | int)', str) -> None
        """
        更新 key 对应数据中的 subkey 对应的数据
        key: 标识符。如果没有，则自动添加
        subkey: key 对应数据中的子键。如果没有，则自动添加
        value: 更新的数据
        uid: 玩家 UID，当更新的数据是玩家私有数据时需要设置
        playerId: 玩家 playerId，当插入的数据是玩家私有数据时需要设置
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
        result, newDTO = self._set(dto)
        _sendDBMessage(result, newDTO, playerId)

    def select(self, key, uid=''):
        # type: (str, '(str | int)') -> dict
        """
        查询 key 对应的数据
        key: 标识符
        uid: 玩家 UID，当查询的数据是玩家私有数据时需要设置
        备注：玩家 UID 不要使用服务端接口 GetPlayerUid 获取，可能与客户端接口 getUid 获取的不一致
        数据不存在时会返回空字典：{}
        """
        dto = self._get(key, uid)
        return dto.value


serverDB = ServerDB()


def _sendDBMessage(result, newDTO, playerId):
    # type: (bool, 'DBDTO', str) -> None
    """
    发送 DTO 给客户端
    """
    if newDTO.uid:
        if not playerId:
            logger.error("玩家 UID %s 对应的 playerId 缺失，请检查您传递的参数！", newDTO.uid)
            return
        # 如果存在 uid，说明是此玩家的私有数据，仅同步到此玩家的客户端
        NotifyToClient(playerId, '_receiveServerDBMessage', ResponseDTO(result, newDTO).parseToDict())
    else:
        # 不存在 uid，同步到所有玩家的客户端
        BroadcastToAllClient('_receiveServerDBMessage', ResponseDTO(result, newDTO).parseToDict())


# noinspection PyProtectedMember
@AllowNotify
def _receiveClientDBMessage(event):
    """
    接收客户端的更新服务端数据请求
    """
    playerId = event['playerId']
    dto = DBDTO.parseToObject(event)
    result, newDTO = serverDB._set(dto)
    _sendDBMessage(result, newDTO, playerId)
