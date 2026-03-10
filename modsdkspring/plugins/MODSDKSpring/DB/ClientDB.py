# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi

from .BaseDB import BaseDB
from .dto.DBDTO import DBDTO
from .dto.ResponseDTO import ResponseDTO
from .utils.MessageQueue import MessageQueue
from ..Network.NotifyManage import NotifyToServer, AllowNotify


class ClientDB(BaseDB):

    def __init__(self):
        super(ClientDB, self).__init__()
        comp = clientApi.GetEngineCompFactory().CreateConfigClient(clientApi.GetLevelId())
        self.set = comp.SetConfigData
        self.get = comp.GetConfigData

    def _set(self, dto):
        # type: (DBDTO) -> bool
        return self.set(dto.key, dto.parseToDict(), False)

    def _get(self, key):
        tempDict = self.get(key, False)
        if tempDict is None:
            tempDict = {}
        tempDict[DBDTO.KEY] = key
        return DBDTO.parseToObject(tempDict)

    def insert(self, key, value, uid=''):
        super(ClientDB, self).insert(key, value, uid)

        dto = self._get(key)
        dto.uid = str(uid)
        dto.value = value

        MessageQueue.push(dto)
        _sendDBMessage(key)


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
    MessageQueue.pop(dto.key)                       # 从队列中弹出
    clientDB._set(dto)                              # 更新数据到本地
    _sendDBMessage(dto.key)                         # 继续从队列中取数据发送
