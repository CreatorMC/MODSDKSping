# -*- coding: utf-8 -*-


class MemoryUtil(object):

    @staticmethod
    def getMemorySize(obj, seen=None):
        """
        递归计算对象的内存占用大小
        返回单位: Byte
        """
        if seen is None:
            seen = set()

        # 获取对象ID，防止重复计算
        obj_id = id(obj)
        if obj_id in seen:
            return 0

        # 标记已访问
        seen.add(obj_id)

        # 获取对象本身的大小
        size = obj.__sizeof__()

        # 递归计算嵌套对象的大小
        if isinstance(obj, (list, tuple, set, frozenset)):
            for item in obj:
                size += MemoryUtil.getMemorySize(item, seen)
        elif isinstance(obj, dict):
            for key, value in obj.iteritems():
                size += MemoryUtil.getMemorySize(key, seen)
                size += MemoryUtil.getMemorySize(value, seen)
        elif hasattr(obj, '__class__'):
            # 处理类实例
            if hasattr(obj, '__slots__'):
                # 计算__slots__的大小
                for slot in obj.__slots__:
                    if hasattr(obj, slot):
                        slot_value = getattr(obj, slot)
                        size += MemoryUtil.getMemorySize(slot_value, seen)
            elif hasattr(obj, '__dict__'):
                # 计算__dict__的大小
                size += MemoryUtil.getMemorySize(obj.__dict__, seen)
        return size