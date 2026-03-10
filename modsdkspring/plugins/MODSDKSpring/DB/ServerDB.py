# -*- coding: utf-8 -*-
import mod.server.extraServerApi as serverApi

from .BaseDB import BaseDB
from .dto.DBDTO import DBDTO
from .dto.ResponseDTO import ResponseDTO
from ..Network.NotifyManage import AllowNotify, NotifyToClient, BroadcastToAllClient


class ServerDB(BaseDB):
    
    def __init__(self):
        super(ServerDB, self).__init__()
        comp = serverApi.GetEngineCompFactory().CreateExtraData(serverApi.GetLevelId())
        self.set = comp.SetExtraData
        self.get = comp.GetExtraData
        self.clean = comp.CleanExtraData

    def _set(self, dto):
        # type: (DBDTO) -> 'tuple[bool, DBDTO]'
        oldDTO = self._get(dto.key)

        # 版本判断
        if dto.version >= oldDTO.version:
            dto.version += 1

            # 私有 key 拼接（不改变 dto 中的 key）
            key = dto.key
            if dto.uid:
                key = dto.key + dto.uid

            self.set(key, dto.parseToDict(), True)
            return True, dto

        return False, oldDTO

    def _get(self, key):
        tempDict = self.get(key)
        if tempDict is None:
            tempDict = {}
        tempDict[DBDTO.KEY] = key
        return DBDTO.parseToObject(tempDict)

    def _clean(self, key):
        return self.clean(key)


serverDB = ServerDB()


# noinspection PyProtectedMember
@AllowNotify
def _receiveClientDBMessage(event):
    """
    接收客户端的更新服务端数据请求
    """
    playerId = event['playerId']
    dto = DBDTO.parseToObject(event)
    result, newDTO = serverDB._set(dto)

    if dto.uid:
        # 如果存在 uid，说明是此玩家的私有数据，仅同步到此玩家的客户端
        NotifyToClient(playerId, '_receiveServerDBMessage', ResponseDTO(result, newDTO).parseToDict())
    else:
        # 不存在 uid，同步到所有玩家的客户端
        BroadcastToAllClient('_receiveServerDBMessage', ResponseDTO(result, newDTO).parseToDict())
