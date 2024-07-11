# pKcScan © 2024.7.11 by cer1cc is licensed under CC BY-NC-SA 4.0 
import os
import platform
from datetime import datetime

def os_check():
    if platform.system().lower() == 'windows':
        return "windows"
    elif platform.system().lower() == 'linux':
        return "linux"
    else:
        return "other"

def path_add(base_path, *paths):  # 路径增加处理
    if not base_path:
        raise ValueError("基础路径不能为空")

    if not all(isinstance(p, str) and p for p in paths):
        raise ValueError("所有附加路径必须是非空字符串")

    try:
        for add_path in paths:
            base_path = os.path.join(base_path, add_path)
        return base_path
    except Exception as e:
        raise RuntimeError(f"连接路径时发生错误: {e}")

def path_check(path,filename=None):
    if not isinstance(path, str):
        raise ValueError("路径必须是字符串")
    
    if not path:
        raise ValueError("路径不能为空")

    try:
        if os.path.exists(path):
            return True
        else:
            return False
    except Exception as e:
        raise RuntimeError(f"检查路径时发生错误: {e}")
    
def findAllFilePathName(path):
    # 检查路径是否存在
    if not path_check(path):
        raise ValueError("路径不存在")
    
    # 检查路径是否为文件夹
    if not os.path.isdir(path):
        raise ValueError("路径必须是文件夹")
    
    # 获取所有子文件夹的名称
    folder_list = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]
    return folder_list

# 获目录下的全部文件名称
def get_all_files_name(path):
    # 检查路径是否存在
    if not path_check(path):
        raise ValueError("路径不存在")
    
    # 检查路径是否为文件夹
    if not os.path.isdir(path):
        raise ValueError("路径必须是文件夹")
    
    # 获取所有子文件夹的名称
    return [name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))]

# 获取目录下的全部文件路径
def getAllFilePath(path):
    # 检查路径是否存在
    if not path_check(path):
        raise ValueError("路径不存在")
    
    # 检查路径是否为文件夹
    if not os.path.isdir(path):
        raise ValueError("路径必须是文件夹")
    
    # 获取所有子文件夹的路径
    return [os.path.join(root, file) for root, dirs, files in os.walk(path) for file in files]


# 获取时间
def get_time():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def printAllpayload(Payload_Path):
    allpath=[]
    for path in getAllFilePath(Payload_Path):
        allpath.append(format_path(path))
    return allpath
    
def format_path(full_path):
    """
    处理路径, 将倒数第二级目录和最后一个文件名组合成所需的格式
    :param full_path: 完整的路径
    :return: 处理后的路径
    """
    # 拆分路径成各级目录和文件名
    path_parts = full_path.split(os.sep)

    # 确保路径中至少有两级目录
    if len(path_parts) < 3:
        raise ValueError("路径中至少需要包含两级目录和一个文件名")

    # 获取倒数第二级目录和最后一个文件名
    second_last_dir = path_parts[-2]
    file_name = path_parts[-1]

    # 组合成所需的格式
    formatted_path = f"{second_last_dir}+{file_name}"

    return formatted_path

def restore_path(formatted_path, base_path):
    """
    将格式化后的路径还原为完整的路径
    :param formatted_path: 格式化后的路径，例如 "password-attacks+top100.txt"
    :param base_path: 基础路径，用于构建完整路径
    :return: 完整的路径
    """
    # 拆分格式化后的路径
    parts = formatted_path.split('+')

    # 确保路径格式正确
    if len(parts) != 2:
        raise ValueError("格式化后的路径格式不正确")

    # 构建完整路径
    full_path = os.path.join(base_path, *parts)

    return full_path