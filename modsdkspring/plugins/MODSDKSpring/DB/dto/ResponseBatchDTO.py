# -*- coding: utf-8 -*-
from .DBDTO import DBDTO


class ResponseBatchDTO(object):
    """
    回调数据传输对象
    传输一批 DTO
    """

    def __init__(self, result, batch, playerId):
        # type: (bool, 'list["DBDTO"]', str) -> None
        self.result = result
        self.batch = batch
        self.playerId = playerId

    def parseToDict(self):
        tempBatch = []
        for value in self.batch:
            tempBatch.append(value.parseToDict())
        return {
            'result': self.result,
            'batch': tempBatch,
            'playerId': self.playerId
        }

    @staticmethod
    def parseToObject(tempDict):
        tempBatch = tempDict['batch']
        batch = []
        for value in tempBatch:
            batch.append(DBDTO.parseToObject(value))
        return ResponseBatchDTO(tempDict['result'], batch, tempDict['playerId'])