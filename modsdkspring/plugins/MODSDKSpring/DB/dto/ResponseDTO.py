# -*- coding: utf-8 -*-
from .DBDTO import DBDTO


class ResponseDTO(object):
    """
    回调数据传输对象
    传输服务端是否更新数据成功，以及服务端最新的数据
    """

    def __init__(self, result, dto):
        # type: (bool, DBDTO) -> None
        self.result = result
        self.dto = dto

    def parseToDict(self):
        return {
            'result': self.result,
            'dto': self.dto.parseToDict()
        }

    @staticmethod
    def parseToObject(tempDict):
        return ResponseDTO(tempDict['result'], DBDTO.parseToObject(tempDict['dto']))