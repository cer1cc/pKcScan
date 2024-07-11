# pKcScan © 2024.7.11 by cer1cc is licensed under CC BY-NC-SA 4.0 
global _global_dict
import json

def init():  # 初始化
    global _global_dict
    _global_dict = {}


def set_value(key, value):
    _global_dict[key] = value  # 定义一个全局变量


def get_value(key, def_value=None):
    '''
    获取全局变量
    '''
    try:
        return _global_dict[key]
    except KeyError:
        return def_value

def get_all_items(): # 获取所有全局变量
    return _global_dict.items()

def print_all_globals():
    """
    打印所有全局变量，优化输出格式
    """
    try:
        all_items = get_all_items()
        formatted_output = json.dumps(dict(all_items), indent=4, ensure_ascii=False)
        return(formatted_output)
    except Exception as e:
        return("Error printing all globals:", e)

class GlobalObjectStore:
    _global_objects = {}

    @classmethod
    def set_object(cls, key, obj):
        """
        存储对象到全局对象存储中
        """
        cls._global_objects[key] = obj

    @classmethod
    def get_object(cls, key):
        """
        从全局对象存储中检索对象
        """
        return cls._global_objects.get(key, None)

    @classmethod
    def remove_object(cls, key):
        """
        从全局对象存储中移除对象
        """
        if key in cls._global_objects:
            del cls._global_objects[key]

    @classmethod
    def clear_objects(cls):
        """
        清空全局对象存储
        """
        cls._global_objects.clear()

