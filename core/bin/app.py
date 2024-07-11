# pKcScan © 2024.7.11 by cer1cc is licensed under CC BY-NC-SA 4.0 
# 第三方库
from core.library import requests
from core.library import requests_HTTPError, requests_RequestException
import concurrent.futures
# 自定义库
from core.initialize import globals
from core.initialize import system
from core.bin import core
from core.bin import handlePoc
from core.bin import forMogoDB
from core.initialize.printf import printfa
from core.initialize.printf import printToConsole
from core.initialize.printf import printToFile
from core.bin.OInitializeURL import OInitializeURL


def fingerprintRecognition():
    """
    进行指纹识别的主函数，包括被动指纹识别和主动指纹识别。

    步骤：
    1. 将输入的BaseURL_Path加载至OInitializeURL类中。
    2. 发送HTTP GET请求获取Base URL的响应。
    3. 捕获并处理HTTP请求。
    4. 执行被动指纹匹配。
    5. 如果被动指纹识别成功，返回指纹信息；否则，进行主动指纹识别。

    异常处理：
    - 捕获HTTPError并打印HTTP错误信息。
    - 捕获RequestException并打印请求错误信息。
    - 捕获其他异常并打印错误信息。

    返回：
    返回指纹信息,类型为str
    """
    def get_fingerprint(url):
        try:
            response = requests.get(url)
            response.raise_for_status()  # 检查HTTP响应状态码是否是200 (成功)
            fingerprint = core.passiveFingerprintMatching(
                response,
                handlePoc.loadAlljsonsForDB(forMogoDB.get_all_fingerprints_with_empty_method())
            )
            return fingerprint
        except requests_HTTPError as http_err:
            printfa(f"HTTP error occurred: {http_err}", "red")  # HTTP错误
        except requests_RequestException as req_err:
            printfa(f"Request error occurred: {req_err}", "red")  # 其他请求错误
        except Exception as err:
            printfa(f"An error occurred: {err}", "red")  # 其他非请求相关错误
        return None

    ObaseURL = OInitializeURL(globals.get_value("BaseURL_Path"))  # 将输入的BaseURL_Path加载至OInitializeURL类中
    printfa("[*] 正在进行被动指纹识别", "message")

    # 尝试第一种URL
    fingerprint = get_fingerprint(ObaseURL.url)
    if fingerprint:
        return fingerprint

    # 尝试第二种URL
    printfa(f"尝试识别 {ObaseURL.scheme}://{ObaseURL.netloc}")
    fingerprint = get_fingerprint(f"{ObaseURL.scheme}://{ObaseURL.netloc}")
    if fingerprint:
        return fingerprint

    return "0"  # 指纹识别失败

    
def execPoc():
    """
    执行Poc检测流程
    """
    # 从全局参数中获取是否设置Poc
    poc_path = globals.get_value("Poc")
    fingerOPocDatas = []
    if poc_path:
        # 如果设置Poc，根据指纹名称和漏洞加载对应的Poc数据
        fingerprints = globals.get_value("Fingerprint")
        pocs_data = forMogoDB.get_poc_by_name_vuln(fingerprints, poc_path)
    else:
        # 如果未设置Poc，仅根据指纹名称加载对应的Poc数据
        fingerprints = globals.get_value("Fingerprint")
        pocs_data = forMogoDB.get_poc_by_name(fingerprints)

    if pocs_data:
        fingerOPocDatas = handlePoc.loadAlljsonsForDB(pocs_data)
    else:
        printfa("未能找到fingerprint,请确认输入正确")

    # 打印检测开始的消息
    printfa("[*] 正在进行Poc检测", "message")

    # 定义一个内部函数，用于多线程执行Poc检测
    def process_poc(fingerOPocData):
        msg = core.switchexecPoc(fingerOPocData.type, fingerOPocData)
        if msg == "0":
            printfa(f"Poc {fingerOPocData.vuln} 检测失败")
        elif msg is not None:
            printfa(msg, "info")

    # 遍历加载的Poc数据进行检测
    if fingerOPocDatas:
        with concurrent.futures.ThreadPoolExecutor(int(globals.get_value('Threads'))) as executor:
            futures = [executor.submit(process_poc, fingerOPocData) for fingerOPocData in fingerOPocDatas]
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    printfa(f"Error occurred: {e}")
    else:
        printToConsole("未能找到该Poc,请确认Poc正确")

    # 打印检测结束的消息
    printfa("检测结束", "message")

