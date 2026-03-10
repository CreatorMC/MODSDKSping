# -*- coding: utf-8 -*-


class BaseDB(object):

    def __init__(self):
        pass

    def _set(self, dto):
        pass

    def _get(self, key):
        pass

    def insert(self, key, value, uid=''):
        # type: (str, '(dict | None)', '(str | int)') -> None
        """
        插入数据
        key: 标识符
        value: 数据字典
        uid: 玩家 UID，当设置的数据是玩家私有数据时需要设置
        备注：key 如果已存在，则为更新数据
        """
        if value is None:
            value = {}

    def delete(self, key):
        # type: (str) -> None
        """
        删除数据
        备注：受限于网易接口，客户端只能做到将 key 对应的数据清空为 {}，key 本身依然存在
        服务端会将 key 本身也删除
        """
        pass

    def update(self, key, subkey, value):
        # type: (str, str, any) -> None
        """
        更新 key 对应数据中的 subkey 对应的数据
        备注：当你用 key 存储了以下格式的数据时：

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
        pass

    def select(self, key):
        # type: (str) -> '(dict | None)'
        """
        查询 key 对应的数据
        """
        pass
