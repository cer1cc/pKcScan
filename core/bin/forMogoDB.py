# pKcScan © 2024.7.11 by cer1cc is licensed under CC BY-NC-SA 4.0 
from core.initialize import globals


def get_all_fingerprints(): # 查询所有fingerprint
    mongodb = globals.GlobalObjectStore.get_object("Omongo")
    if mongodb is None:
        print("Database connection is not initialized")
        return []
    try:
        collection = mongodb["FingerPrint"]
        fingerprints = list(collection.find({}, {"_id": 0})) 
        return fingerprints
    except Exception as e:
        print("Error occurred while querying database:", e)
        return []

def returnFingerprints():
    """
    查询所有fingerprint并返回不重复的name列表

    Returns:
        list: 不重复的name列表
    """
    mongodb = globals.GlobalObjectStore.get_object("Omongo")
    if mongodb is None:
        print("Database connection is not initialized")
        return []
    try:
        collection = mongodb["FingerPrint"]
        fingerprints = list(collection.find({}, {"_id": 0, "name": 1}))
        # 使用集合去重
        unique_names = list(set(fp['name'] for fp in fingerprints))
        return unique_names
    except Exception as e:
        print("Error occurred while querying database:", e)
        return []

def get_all_fingerprints_with_empty_method(): # 查询所有请求方法为空的
    mongodb = globals.GlobalObjectStore.get_object("Omongo")
    if mongodb is None:
        print("Database connection is not initialized")
        return []

    try:
        collection = mongodb["FingerPrint"]
        # 查询 mainRequest 中 method 字段为空的文档
        fingerprints = list(collection.find({"mainRequest.1.request.method": ""}, {"_id": 0}))
        if fingerprints:
            return fingerprints
    except Exception as e:
        print("Error occurred while querying database:", e)
        return []


def get_all_poc():
    """
    查询所有Poc数据
    """
    mongodb = globals.GlobalObjectStore.get_object("Omongo")
    if mongodb is None:
        print("Database connection is not initialized")
        return []
    try:
        collection = mongodb["Poc"]
        fingerprints = list(collection.find({}, {"_id": 0}))
        return fingerprints
    except Exception as e:
        print("Error occurred while querying database:", e)
        return []

def get_poc_by_name(fingerprint):
    """
    根据名称查询Poc数据
    :param fingerprint: Poc名称
    :return: 匹配的Poc数据或空列表
    """
    mongodb = globals.GlobalObjectStore.get_object("Omongo")
    if mongodb is None:
        print("Database connection is not initialized")
        return []
    try:
        collection = mongodb["Poc"]
        pocs = list(collection.find({"name": fingerprint}, {"_id": 0}))
        if pocs:
            return pocs
        else:
            print(f"No Poc found with the name: {fingerprint}")
            return []
    except Exception as e:
        print(f"Error occurred while querying database: {e}")
        return []

def get_poc_by_name_vuln(fingerprint, vuln):
    """
    根据名称和漏洞信息查询Poc数据
    :param fingerprint: Poc名称
    :param vuln: Poc漏洞
    :return: 匹配的Poc数据或空列表
    """
    mongodb = globals.GlobalObjectStore.get_object("Omongo")
    if mongodb is None:
        print("Database connection is not initialized")
        return []
    
    try:
        # 获取名为 "Poc" 的集合
        collection = mongodb["Poc"]
        
        # 根据名称和漏洞信息查询匹配的 Poc 数据
        pocs = list(collection.find({"name": fingerprint, "vuln": vuln}, {"_id": 0}))
        
        if pocs:
            return pocs
        else:
            print(f"No Poc found with the name: {fingerprint} and vuln: {vuln}")
            return []
    except Exception as e:
        print(f"Error occurred while querying database: {e}")
        return []


def returnPocVuln(poc_name):
    """
    查询fingerprint并返回不重复的vuln列表

    Returns:
        list: 不重复的vuln列表
    """
    mongodb = globals.GlobalObjectStore.get_object("Omongo")
    if mongodb is None:
        print("Database connection is not initialized")
        return []
    try:
        collection = mongodb["Poc"]
        pocs = list(collection.find({"name": poc_name}, {"_id": 0}))
        # 使用集合去重
        vulns = list(set(fp['vuln'] for fp in pocs))
        return vulns
    except Exception as e:
        print("Error occurred while querying database:", e)
        return []

# 示例用法
if __name__ == "__main__":
    fingerprints = get_all_fingerprints()
    print(f"Retrieved {len(fingerprints)} fingerprints")
    for fingerprint in fingerprints:
        print(fingerprint)
