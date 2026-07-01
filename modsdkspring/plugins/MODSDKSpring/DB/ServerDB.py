# -*- coding: utf-8 -*-
import json

import mod.server.extraServerApi as serverApi

from .BaseDB import BaseDB, DB_CHANGE_EVENT
from .dto.DBDTO import DBDTO
from .dto.ResponseBatchDTO import ResponseBatchDTO
from .dto.ResponseDTO import ResponseDTO
from ..Network.NotifyManage import AllowNotify, NotifyToClient, BroadcastToAllClient
from ..Network.server.NotifyServer import NotifyServer
from ..core.log.Log import logger
from ..utils.json.JSONUtil import JSONUtil
from ..utils.memory.MemoryUtil import MemoryUtil


class ServerDB(BaseDB):

    def __init__(self):
        super(ServerDB, self).__init__()
        comp = serverApi.GetEngineCompFactory().CreateExtraData(serverApi.GetLevelId())
        self.set = comp.SetExtraData
        self.clean = comp.CleanExtraData
        self.save = comp.SaveExtraData
        self.get = comp.GetExtraData
        self.getWholeExtraData = comp.GetWholeExtraData

        # 用于订阅转换的钩子函数
        self._hook = None

        # 订阅的 key
        self._subscribe = ''
        NotifyServer.getSystem().ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ClientLoadAddonsFinishServerEvent", self,
                                                self.ClientLoadAddonsFinishServerEvent, 10)

    def _set(self, dto, nowDTO=None):
        # type: (DBDTO, DBDTO) -> 'tuple[bool, DBDTO]'
        if nowDTO is None:
            nowDTO = self._get(dto.key, dto.uid)

        # 版本判断
        if dto.version == nowDTO.version:
            dto.version += 1

            # 私有 key 拼接（不改变 dto 中的 key）
            key = dto.key
            if dto.uid:
                key = dto.key + dto.uid

            self.set(key, json.dumps(dto.parseToSave()), True)

            # 借由通信系统发送本地广播事件，通知该 MOD 内的数据变化
            NotifyServer.getSystem().BroadcastEvent(DB_CHANGE_EVENT, {
                'key': key,  # 拼接 UID 后的真实的 key
                'newValue': dto.value,
                'oldValue': nowDTO.value,
                'extraValue': dto.extraValue
            })
            return True, dto

        logger.error("版本不一致！")
        return False, nowDTO

    def _get(self, key, uid):
        # type: (str, str) -> 'DBDTO'
        uid = str(uid)
        tempDict = self.get(key + uid)

        # 确保 tempDict 是字典
        if tempDict is None:
            tempDict = {
                DBDTO.VALUE: {}
            }
        elif isinstance(tempDict, basestring):
            try:
                tempDict = json.loads(tempDict)
                if not isinstance(tempDict, dict):
                    tempDict = {
                        DBDTO.VALUE: tempDict
                    }
            except ValueError:
                logger.warning("无效的 JSON, 自动将此字符串作为 DBDTO 的 value. key: %s, uid: %s, value: %s", key, uid, tempDict)
                tempDict = {
                    DBDTO.VALUE: tempDict
                }
        elif isinstance(tempDict, dict):
            pass
        else:
            tempDict = {
                DBDTO.VALUE: tempDict
            }

        tempDict = JSONUtil.convertUnicodeToStr(tempDict)
        dto = None
        if DBDTO.VALUE in tempDict:
            tempDict[DBDTO.KEY] = key
            dto = DBDTO.parseToObject(tempDict)
        elif callable(self._hook):
            dto = self._hook(self, key, tempDict, uid)

        # 兜底检查
        if dto is None:
            dto = DBDTO(key, {}, 0, uid)

        dto.uid = uid
        return dto

    def insert(self, key, value, uid='', playerId='', extraValue=None):
        # type: (str, '(dict | None)', '(str | int)', str, dict) -> None
        """
        插入数据
        key: 标识符
        value: 数据字典
        uid: 玩家 UID，当插入的数据是玩家私有数据时需要设置
        playerId: 玩家 playerId，当插入的数据是玩家私有数据时需要设置
        extraValue: 额外的字典值，用于在事件回调中传递自定义的额外数据。此数据不会持久化保存
        备注：key 如果已存在，则为更新数据
        玩家 UID 不要使用服务端接口 GetPlayerUid 获取，可能与客户端接口 getUid 获取的不一致
        """
        if value is None:
            value = {}

        # 确保在 uid 不为空的情况下，playerId 也不为空，反之亦然
        if bool(uid) ^ bool(playerId):
            logger.error("玩家 UID %s 和 playerId %s 需要同时存在/不存在，请检查您传递的参数！", uid, playerId)
            return

        nowDTO = self._get(key, uid)
        dto = DBDTO.parseToObject(nowDTO.parseToDict())
        dto.value = value
        result, newDTO = self._set(dto, nowDTO)
        if isinstance(extraValue, dict):
            newDTO.extraValue = extraValue
        _sendDBMessage(result, newDTO, playerId)

    def delete(self, key, uid='', playerId='', extraValue=None):
        # type: (str, '(str | int)', str, dict) -> None
        """
        删除数据
        key: 标识符
        uid: 玩家 UID，当删除的数据是玩家私有数据时需要设置
        playerId: 玩家 playerId，当插入的数据是玩家私有数据时需要设置
        extraValue: 额外的字典值，用于在事件回调中传递自定义的额外数据。此数据不会持久化保存
        备注：为了保证删除操作也能同步到客户端，服务端数据只会清空为 {}，key 本身不删除
        玩家 UID 不要使用服务端接口 GetPlayerUid 获取，可能与客户端接口 getUid 获取的不一致
        """
        self.insert(key, {}, uid, playerId, extraValue)

    def update(self, key, subkey, value, uid='', playerId='', extraValue=None):
        # type: (str, str, any, '(str | int)', str, dict) -> None
        """
        更新 key 对应数据中的 subkey 对应的数据
        key: 标识符。如果没有，则自动添加
        subkey: key 对应数据中的子键。如果没有，则自动添加
        value: 更新的数据
        uid: 玩家 UID，当更新的数据是玩家私有数据时需要设置
        playerId: 玩家 playerId，当插入的数据是玩家私有数据时需要设置
        extraValue: 额外的字典值，用于在事件回调中传递自定义的额外数据。此数据不会持久化保存
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
        # 确保在 uid 不为空的情况下，playerId 也不为空，反之亦然
        if bool(uid) ^ bool(playerId):
            logger.error("玩家 UID %s 和 playerId %s 需要同时存在/不存在，请检查您传递的参数！", uid, playerId)
            return

        nowDTO = self._get(key, uid)
        dto = DBDTO.parseToObject(nowDTO.parseToDict())
        dto.value[subkey] = value
        result, newDTO = self._set(dto, nowDTO)
        if isinstance(extraValue, dict):
            newDTO.extraValue = extraValue
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

    def subscribe(self, preKey):
        # type: (str) -> None
        """
        服务端订阅数据
        preKey: 订阅的 key 的前缀
        备注：订阅后，在有玩家进入时，服务端会在 ClientLoadAddonsFinishServerEvent 事件中，自动将前缀为 preKey 的 key 对应的非玩家私有数据发送给玩家
        订阅的数据必须为使用 insert、delete、update 方法保存的数据，否则将会引发错误
        推荐在服务端系统调用 __init__ 方法时进行订阅
        """
        self._subscribe = preKey

    # noinspection PyMethodMayBeStatic
    def _subscribeConvertHook(self, key, value, uid=''):
        # type: ('ServerDB', str, any, str) -> '(DBDTO | None)'
        """
        默认的订阅数据钩子函数
        """
        if isinstance(value, dict):
            return DBDTO(key, value, 0, uid)
        elif isinstance(value, basestring):
            return DBDTO(key, json.loads(value), 0, uid)
        return None

    def subscribeConvert(self, preKey, hook=_subscribeConvertHook):
        """
        服务端订阅数据并进行数据格式转换
        适用于将已上线的未使用此框架处理的数据，纳入此框架的管理
        preKey: 订阅的 key 的前缀
        hook: 进行数据格式转换时使用的钩子函数
        备注：订阅后，在有玩家进入时，服务端会在 ClientLoadAddonsFinishServerEvent 事件中，自动将前缀为 preKey 的 key 对应的非玩家私有数据发送给玩家
        订阅的数据如果不符合框架内部的数据存储格式，会调用 hook 函数进行转换，转换后会自动持久化保存
        推荐在服务端系统调用 __init__ 方法时进行订阅
        """
        self.subscribe(preKey)
        self._hook = hook

    def ClientLoadAddonsFinishServerEvent(self, event):
        """
        触发时机：客户端mod加载完成时，服务端触发此事件。服务器可以使用此事件，往客户端发送数据给其初始化。
        """
        playerId = event['playerId']
        if self._subscribe:
            allDataDict = self.getWholeExtraData()
            isSend = False
            if allDataDict:
                batch = []
                isHook = False
                for key, value in allDataDict.iteritems():
                    if isinstance(key, basestring) and key.startswith(self._subscribe):
                        if isinstance(value, basestring) and DBDTO.KEY in value:
                            dto = DBDTO.parseToObject(JSONUtil.convertUnicodeToStr(json.loads(value)))
                            # 排除玩家私有数据
                            if not dto.uid:
                                batch.append(dto)
                        elif callable(self._hook):
                            dto = self._hook(self, key, value)
                            if dto is not None and not dto.uid:
                                batch.append(dto)
                                self.set(key, json.dumps(dto.parseToSave()), False)
                                isHook = True

                    # 优化，不让一个网络包过大（限制在 512 KB 多一点）
                    memorySize = MemoryUtil.getMemorySize(batch)
                    if memorySize >= 512 * 1024:
                        logger.info("服务端发送同步共享数据大小: %s KB", memorySize / 1024.0)
                        NotifyToClient(playerId, '_receiveFromServerBatchDBMessage', ResponseBatchDTO(True, batch, playerId).parseToDict())
                        isSend = True
                        batch = []

                if isHook:
                    self.save()

                # 兜底
                if batch:
                    logger.info("服务端发送同步共享数据大小: %s KB", MemoryUtil.getMemorySize(batch) / 1024.0)
                    NotifyToClient(playerId, '_receiveFromServerBatchDBMessage', ResponseBatchDTO(True, batch, playerId).parseToDict())
                    isSend = True

            # 如果没有数据发送，发给客户端空数据，而不是保持静默
            if not isSend:
                NotifyToClient(playerId, '_receiveFromServerEmptyDBMessage', {
                    'isPrivate': False
                })


serverDB = ServerDB()


def _sendDBMessage(result, newDTO, playerId):
    # type: (bool, 'DBDTO', str) -> None
    """
    服务端主动更新，发送 DTO 给客户端
    """
    # 从服务端更新都更新不成功，就没有必要与客户端通信了
    if not result:
        return

    if newDTO.uid:
        # 如果存在 uid，说明是此玩家的私有数据，仅同步到此玩家的客户端
        if not playerId:
            logger.error("玩家 UID %s 对应的 playerId 缺失，请检查您传递的参数！", newDTO.uid)
            return
        NotifyToClient(playerId, '_receiveFromServerDBMessage', ResponseDTO(result, newDTO, playerId).parseToDict())
    else:
        # 不存在 uid，同步到所有玩家的客户端
        BroadcastToAllClient('_receiveFromServerDBMessage', ResponseDTO(result, newDTO, playerId).parseToDict())


# noinspection PyProtectedMember
@AllowNotify
def _receiveClientDBMessage(event):
    """
    接收客户端的更新服务端数据请求
    """
    playerId = event['playerId']
    dto = DBDTO.parseToObject(event)
    result, newDTO = serverDB._set(dto)
    newDTO.requestId = dto.requestId

    if newDTO.uid or (not result):
        # 如果存在 uid，说明是此玩家的私有数据，仅同步到此玩家的客户端
        # 如果服务端拒绝更新，仅回调此玩家的客户端，不广播到所有玩家客户端
        NotifyToClient(playerId, '_receiveServerDBMessage', ResponseDTO(result, newDTO, playerId).parseToDict())
    else:
        # 不存在 uid，同步到所有玩家的客户端
        BroadcastToAllClient('_receiveServerDBMessage', ResponseDTO(result, newDTO, playerId).parseToDict())


# noinspection PyProtectedMember
@AllowNotify
def _receiveClientUIDDBMessage(event):
    """
    接收客户端进入时获取私有数据的请求
    """
    playerId = event['playerId']
    uid = str(event['uid'])
    preKey = event['_subscribe']
    if preKey:
        allDataDict = serverDB.getWholeExtraData()
        isSend = False
        if allDataDict:
            batch = []
            isHook = False
            for key, value in allDataDict.items():
                if isinstance(key, basestring) and key.startswith(preKey):
                    if isinstance(value, basestring) and DBDTO.KEY in value:
                        dto = DBDTO.parseToObject(JSONUtil.convertUnicodeToStr(json.loads(value)))
                        # 只保留玩家私有数据
                        if dto.uid == uid:
                            batch.append(dto)
                    elif callable(serverDB._hook):
                        _key = key
                        isEndNone = False
                        if _key.endswith('None'):
                            _key = _key[:-len('None')] + '0'
                            isEndNone = True
                        if _key.endswith(uid):
                            _key = _key[:-len(uid)]
                        dto = serverDB._hook(serverDB, _key, value, '0' if isEndNone else uid)
                        if dto is not None and dto.uid == uid:
                            batch.append(dto)
                            serverDB.clean(_key)                                                                    # 删除不带 uid 的旧数据，防止再次进入存档时被再次转换
                            serverDB.set(_key + uid, json.dumps(dto.parseToSave()), False)
                            isHook = True

                # 优化，不让一个网络包过大（限制在 512 KB 多一点）
                memorySize = MemoryUtil.getMemorySize(batch)
                if memorySize >= 512 * 1024:
                    logger.info("服务端发送同步私有数据大小: %s KB", memorySize / 1024.0)
                    NotifyToClient(playerId, '_receiveFromServerBatchDBMessage', ResponseBatchDTO(True, batch, playerId).parseToDict())
                    isSend = True
                    batch = []

            if isHook:
                serverDB.save()

            # 兜底
            if batch:
                logger.info("服务端发送同步私有数据大小: %s KB", MemoryUtil.getMemorySize(batch) / 1024.0)
                NotifyToClient(playerId, '_receiveFromServerBatchDBMessage', ResponseBatchDTO(True, batch, playerId).parseToDict())
                isSend = True

        # 如果没有数据发送，发给客户端空数据，而不是保持静默
        if not isSend:
            NotifyToClient(playerId, '_receiveFromServerEmptyDBMessage', {
                'isPrivate': True
            })
