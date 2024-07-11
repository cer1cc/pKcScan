# pKcScan © 2024.7.11 by cer1cc is licensed under CC BY-NC-SA 4.0 
# 第三方库
from core.library import requests
from core.library import requests_HTTPError, requests_RequestException

import copy
# 读取对象PocData并形成数据包结构,使其能正常发送
from core.bin.Oreadjson import PocData
from core.bin.Oreadjson import RequestResponse
from core.bin.OInitializeURL import OInitializeURL
from core.initialize import globals
from core.initialize.printf import printfa, printToConsole, printToFile,clear_file,MultiThreadCommunication, sender_function

# 被动指纹匹配
def passiveFingerprintMatching(response,allFingerprintOPocData):
    """
    被动指纹匹配
    :param PocData: PocData对象
    :return: 匹配结果
    """
    for fingerOPocData in allFingerprintOPocData:
        requestResponse=fingerOPocData.get_main_request_by_key("1")#获取第一个请求包
        if requestResponse.response_body in response.text:
            printfa(f"识别到指纹为{fingerOPocData.name}","info")
            return fingerOPocData.name
        

def switchexecPoc(type, fingerOPocData):  # 按类型执行Poc
    switch = {
        "1": tpye1execPoc,
        "2": tpye2execPoc,
        "3": tpye3execPoc
    }
    selected_function = switch.get(type, None)
    if selected_function:
        return selected_function(fingerOPocData)
    else:
        return "错误的Poc类型"


def tpye1execPoc(fingerOPocData):
    """
    执行指定的Poc测试
    :param fingerOPocData: Poc数据对象
    :return: 返回0表示未发现漏洞或发生错误
    """
    ObaseURL = OInitializeURL(globals.get_value("BaseURL_Path"))  # 加载一个基础Url
    PocORequestResponse = fingerOPocData.get_main_request_by_key("1")
    Url = OInitializeURL(PocORequestResponse.request_path)
    
    if not PocORequestResponse.request_method:
        printfa(f"存在一条错误Poc：关键信息 {fingerOPocData.name}: {fingerOPocData.vuln}")
        return "0"
    
    if PocORequestResponse.request_path:
        ObaseURL.path = Url.path
        ObaseURL.query = Url.query
    else:
        ObaseURL.path = ""
        ObaseURL.query = ""
    
    cookies = PocORequestResponse.request_cookie or {}
    headers = PocORequestResponse.request_header or {}
    
    try:
        printfa(f"正在检测是否存在 {fingerOPocData.vuln}", "message")
        
        if PocORequestResponse.request_method.upper() == "GET":
            response = requests.get(ObaseURL.url, cookies=cookies, headers=headers)
        elif PocORequestResponse.request_method.upper() == "POST":
            data = PocORequestResponse.request_body or {}
            if globals.get_value("Test"):
                printfa(data,"test")
            response = requests.post(ObaseURL.url, cookies=cookies, headers=headers, data=data)
        else:
            printfa(f"不支持的请求方法：{PocORequestResponse.request_method}", "red")
            return "0"
        
        if globals.get_value("Test"):
            printfa(ObaseURL.url,"test")
            printfa(headers,"test")
            printfa(cookies,"test")


        response.raise_for_status()  # 检查HTTP响应状态码是否是200 (成功)
        
    except requests_HTTPError as http_err:
        printfa(f"HTTP error occurred: {http_err}", "red")  # HTTP错误
        return "0"
    except requests_RequestException as req_err:
        printfa(f"Request error occurred: {req_err}", "red")  # 其他请求错误
        return "0"
    except Exception as err:
        printfa(f"An error occurred: {err}", "red")  # 其他非请求相关错误
        return "0"
    else:
        if globals.get_value("Test"):
            printfa(PocORequestResponse.response_body,"test")
            if globals.get_value("TestResponse"):
                printfa(response.text)
        if PocORequestResponse.response_body in response.text:
            globals.GlobalObjectStore.get_object("Msg").send_message({"cyan":f"网址 '{ObaseURL.scheme}://{ObaseURL.netloc}' 指纹识别为 {fingerOPocData.name} 发现存在: {fingerOPocData.vuln}漏洞"})
        else:
            globals.GlobalObjectStore.get_object("Msg").send_message({"red":f"未发现 {fingerOPocData.vuln}"})


def tpye2execPoc(fingerOPocData):
    """
    执行类型为2的Poc检测

    Args:
        fingerOPocData (object): Poc数据对象

    Returns:
        str: 检测结果
    """
    flag = 0
    # 加载基础URL
    ObaseURL = OInitializeURL(globals.get_value("BaseURL_Path"))
    # 选择的payload路径
    payloadpath = globals.get_value("Payload")
    # 获取主请求响应对象
    PocORequestResponse = fingerOPocData.get_main_request_by_key("1")
    baseRequestResponse = copy.deepcopy(PocORequestResponse)
    # 初始化URL对象
    Url = OInitializeURL(PocORequestResponse.request_path)
    msg=globals.GlobalObjectStore.get_object("Msg")

    # 检查关键信息是否完整
    if not PocORequestResponse.request_method:
        printfa(f"存在一条错误Poc：关键信息 {fingerOPocData.name}: {fingerOPocData.vuln}")
        return "0"
    
    # 设置请求路径
    if PocORequestResponse.request_path:
        ObaseURL.path = Url.path
        ObaseURL.query = Url.query
    else:
        ObaseURL.path = ""
        ObaseURL.query = ""
    
    # 获取所有包含§符号闭合的键
    keys = baseRequestResponse.get_keys_with_enclosed_content()
    if globals.get_value("Test"):
        printfa(keys,"test")
        printfa(ObaseURL.path,"test")
        printfa(ObaseURL.query,"test")
        printfa(PocORequestResponse.request_body,"test")
        printfa(PocORequestResponse.request_method,"test")
        
    # 执行Poc检测
    printfa(f"正在检测并尝试 {fingerOPocData.vuln}", "info")
    with open(payloadpath) as file:
        for payloads in file.readlines():
            for key in keys:
                for payload in payloads.split():  # 迭代每个payload
                    # 替换请求中的§符号闭合内容
                    text = baseRequestResponse.replace_enclosed_content(key, payload)
                    printfa(text)
                    PocORequestResponse.alternatText(key, text)
                    # 获取请求的cookie和header信息
                    cookies = PocORequestResponse.request_cookie or {}
                    headers = PocORequestResponse.request_header or {}
                    try:
                        # 发起HTTP请求
                        if PocORequestResponse.request_method.upper() == "GET":
                            response = requests.get(ObaseURL.url, cookies=cookies, headers=headers)
                        elif PocORequestResponse.request_method.upper() == "POST":
                            data = PocORequestResponse.request_body or {}
                            if globals.get_value("Test"):
                                printfa(data,"test")
                            response = requests.post(ObaseURL.url, cookies=cookies, headers=headers, data=data)
                        else:
                            printfa(f"不支持的请求方法：{PocORequestResponse.request_method}", "red")
                            return "0"
                        response.raise_for_status()  # 检查HTTP响应状态码是否是200 (成功)
                    except requests_HTTPError as http_err:
                        printfa(f"HTTP error occurred: {http_err}", "red")  # HTTP错误
                        return "0"
                    except requests_RequestException as req_err:
                        printfa(f"Request error occurred: {req_err}", "red")  # 其他请求错误
                        return "0"
                    except Exception as err:
                        printfa(f"An error occurred: {err}", "red")  # 其他非请求相关错误
                        return "0"
                    else:
                        flag += 1
                        # 判断漏洞是否存在
                        if PocORequestResponse.response_body in response.text:
                            globals.GlobalObjectStore.get_object("Msg").send_message({"cyan":f"网址 '{ObaseURL.scheme}://{ObaseURL.netloc}' 指纹识别为 {fingerOPocData.name} 发现存在: {fingerOPocData.vuln}漏洞"})
                            return None
    if flag >= 10:
        globals.GlobalObjectStore.get_object("Msg").send_message({"info":f"存在{fingerOPocData.vuln}漏洞,尝试暴力破解失败,可以尝试--payload选项查看payload,选择更强的字典"})
        return None
    globals.GlobalObjectStore.get_object("Msg").send_message({"red":f"未发现 {fingerOPocData.vuln}"})



def tpye3execPoc(fingerOPocData):
    flag=0
    ObaseURL = OInitializeURL(globals.get_value("BaseURL_Path"))
    int_requestNumber=fingerOPocData.get_main_request_key_count()# mainRequest中键的个数
    msg=globals.GlobalObjectStore.get_object("Msg")
    printfa(f"正在检测是否存在 {fingerOPocData.vuln}", "message")
    for i in range(1,int_requestNumber+1):
        PocORequestResponse = fingerOPocData.get_main_request_by_key(f"{i}")
        Url = OInitializeURL(PocORequestResponse.request_path)
        if not PocORequestResponse.request_method:
            printfa(f"存在一条错误Poc：关键信息 {fingerOPocData.name}: {fingerOPocData.vuln}")
            return "0"
    
        if PocORequestResponse.request_path:
            ObaseURL.path = Url.path
            ObaseURL.query = Url.query
        else:
            ObaseURL.path = ""
            ObaseURL.query = ""

        cookies = PocORequestResponse.request_cookie or {}
        headers = PocORequestResponse.request_header or {}

        try:
            if PocORequestResponse.request_method.upper() == "GET":
                response = requests.get(ObaseURL.url, cookies=cookies, headers=headers)
            elif PocORequestResponse.request_method.upper() == "POST":
                data = PocORequestResponse.request_body or {}
                if globals.get_value("Test"):
                    printfa(data,"test")
                response = requests.post(ObaseURL.url, cookies=cookies, headers=headers, data=data)
            else:
                printfa(f"不支持的请求方法：{PocORequestResponse.request_method}", "red")
                return "0"

            if globals.get_value("Test"):
                printfa(ObaseURL.url,"test")
                printfa(headers,"test")
                printfa(cookies,"test")

            response.raise_for_status()  # 检查HTTP响应状态码是否是200 (成功)

        except requests_HTTPError as http_err:
            printfa(f"HTTP error occurred: {http_err}", "red")  # HTTP错误
            return "0"
        except requests_RequestException as req_err:
            printfa(f"Request error occurred: {req_err}", "red")  # 其他请求错误
            return "0"
        except Exception as err:
            printfa(f"An error occurred: {err}", "red")  # 其他非请求相关错误
            return "0"
        else:
            if globals.get_value("Test"):
                printfa(PocORequestResponse.response_body,"test")
                if globals.get_value("TestResponse"):
                    printfa(response.text)
            if PocORequestResponse.response_body in response.text:
                flag+=1
    if flag>0:
        globals.GlobalObjectStore.get_object("Msg").send_message({"cyan":f"网址 '{ObaseURL.scheme}://{ObaseURL.netloc}' 指纹识别为 {fingerOPocData.name} 发现存在: {fingerOPocData.vuln}漏洞"})
    else:
        globals.GlobalObjectStore.get_object("Msg").send_message({"red":f"未发现 {fingerOPocData.vuln}"})