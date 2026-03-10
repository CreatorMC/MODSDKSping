# -*- coding: utf-8 -*-
import mod.server.extraServerApi as serverApi

from .BaseDB import BaseDB, DB_CHANGE_EVENT
from .dto.DBDTO import DBDTO
from .dto.ResponseDTO import ResponseDTO
from ..Network.NotifyManage import AllowNotify, NotifyToClient, BroadcastToAllClient
from ..Network.server.NotifyServer import NotifyServer


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
        super(ServerDB, self).insert(key, value, uid)
        dto = self._get(key, uid)
        dto.value = value
        tempDict = dto.parseToDict()
        tempDict['playerId'] = playerId
        _receiveClientDBMessage(tempDict)

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
        super(ServerDB, self).delete(key, uid)
        dto = self._get(key, uid)
        result, newDTO = self._clean(dto)
        _sendDBMessage(result, newDTO, playerId)


serverDB = ServerDB()


def _sendDBMessage(result, newDTO, playerId):
    # type: (bool, 'DBDTO', str) -> None
    """
    发送 DTO 给客户端
    """
    if newDTO.uid:
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
