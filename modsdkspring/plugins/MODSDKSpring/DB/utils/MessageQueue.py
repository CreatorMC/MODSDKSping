# -*- coding: utf-8 -*-
from collections import deque

from ..dto.DBDTO import DBDTO


class MessageQueue(object):
    # 队列字典，相同的 key 是同一队列
    __queueDict = {}

    @staticmethod
    def push(dto):
        # type: (DBDTO) -> None
        """
        向消息队列中添加数据
        """
        key = dto.key
        if key not in MessageQueue.__queueDict:
            MessageQueue.__queueDict[key] = deque()

        MessageQueue.__queueDict[key].append(dto)

    @staticmethod
    def pop(key):
        # type: (str) -> '(DBDTO | None)'
        """
        取出队列中的第一个数据（删除队列中的第一个数据）
        """
        if key not in MessageQueue.__queueDict or len(MessageQueue.__queueDict[key]) == 0:
            return None

        dbDTO = MessageQueue.__queueDict[key].popleft()
        if len(MessageQueue.__queueDict[key]) == 0:
            del MessageQueue.__queueDict[key]
        return dbDTO

    @staticmethod
    def get(key):
        # type: (str) -> '(DBDTO | None)'
        """
        获取队列中的第一个数据（只获取，不删除）
        """
        if key not in MessageQueue.__queueDict or len(MessageQueue.__queueDict[key]) == 0:
            return None

        dbDTO = MessageQueue.__queueDict[key][0]
        return dbDTO
