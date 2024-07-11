# pKcScan © 2024.7.11 by cer1cc is licensed under CC BY-NC-SA 4.0 
from core.initialize import globals
from core.initialize import system
from core.bin.Oreadjson import PocData

def fingerToPoc(finger,versions=None):
    if not finger:
        raise ValueError("指纹不能为空")
    poc_path = system.path_add(globals.get_value("Poc_Path"), finger)
    if not versions:
        if system.path_check(poc_path):
            return poc_path
        else:
            return "库中没有该指纹Poc"
    else:
        poc_path = system.path_add(poc_path, versions)
        if system.path_check(poc_path):
            return poc_path
        else:
            return "库中没有该指纹(或该版本)Poc"
        
def findAllfinger():
    return system.findAllFilePathName(globals.get_value("Poc_Path"))

def findAllVersion(finger):            
    
    if not finger:
        raise ValueError("指纹不能为空")
    return system.findAllFilePathName(system.path_add(globals.get_value("Poc_Path"), finger))

def loadAlljsonForFile(json_directory):
    """
    此函数从JSON文件夹中加载所有JSON为对象
    """
    if not json_directory:
        raise ValueError("JSON文件夹不能为空")
    if not system.path_check(json_directory):
        raise RuntimeError("JSON文件夹不存在")
    # 返回对象 读取所有 JSON 文件并创建对象
    return [PocData.from_json_file(json_file) for json_file in system.getAllFilePath(json_directory)]
  
def loadAlljsonsForDB(jsons):
    return [PocData(json) for json in jsons]