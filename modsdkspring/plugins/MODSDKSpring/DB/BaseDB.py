# -*- coding: utf-8 -*-
DB_CHANGE_EVENT = "DB_CHANGE_EVENT"     # 数据变化事件


class BaseDB(object):

    def __init__(self):
        pass

    def insert(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        pass

    def select(self, *args, **kwargs):
        pass
