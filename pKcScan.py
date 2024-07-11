#!/usr/bin/env python3
# pKcScan © 2024.7.11 by cer1cc is licensed under CC BY-NC-SA 4.0 
import os
import sys

from core.initialize.flag import banner
print(banner())

from core.initialize import globals
from core.initialize import system
from core.initialize import mongoConnect
from core.initialize import shellArgparse
from core.bin import writeJsonToDB
from core.bin import forMogoDB
from core.bin import app
from core.initialize.printf import printfa, printToConsole, printToFile,clear_file,MultiThreadCommunication, sender_function


# _global_dict 全局参数只允许在这个文件中改动
def initialize():# 初始化
    globals.init()
    args=shellArgparse.shellArgparse()
    if not any(vars(args).values()):
        printToConsole("尝试使用 -h 获取帮助", "info")
        sys.exit(0)

    globals.set_value("SYS_OS", system.os_check()) # 当前操作系统
    globals.set_value("SYS_Path", os.path.abspath(os.path.dirname(__file__))) # 当前绝对路径
    sys.path.append(globals.get_value("SYS_Path")) # 添加项目根目录到环境变量
    globals.set_value("Poc_Path", system.path_add(globals.get_value("SYS_Path"), "module", "Poc")) # Poc路径
    globals.set_value("Payload_Path", system.path_add(globals.get_value("SYS_Path"),"module", "PentestDicts")) # Payload路径

    if args.payload:# 查看payload(字典)
        for payload in system.printAllpayload(globals.get_value("Payload_Path")):
            printToConsole(f"{payload}","cyan_fine")
        exit()

    if args.p:# 设置payload(字典)
        print(args.p)
        globals.set_value("Payload",system.restore_path(args.p,globals.get_value("Payload_Path")))# -p选项
    else:
        globals.set_value("Payload",system.restore_path("password-attacks+top100.txt",globals.get_value("Payload_Path")))#默认加载此payload

    globals.set_value("Fingerprint_Path", system.path_add(globals.get_value("SYS_Path"), "module", "fingerprint","allFingerprint")) # fingerprint路径

    if args.report:
        globals.set_value("Report_Path", system.path_add(globals.get_value("SYS_Path"), "module", "Report",f"{system.get_time()}.md")) # 报告路径
        printToConsole(f"此次扫描生成报告位置为:\n{globals.get_value('Report_Path')}", "message")
    else:
        globals.set_value("Report_Path", system.path_add(globals.get_value("SYS_Path"), "module", "Report","report.md")) # 默认生成报告路径
        clear_file()

    globals.set_value("CONFIG_FILE_PATH", system.path_add(globals.get_value("SYS_Path"), "core", "initialize","config.json")) # 初始化配置路径
    globals.set_value("Delete_database",args.r)# 设置目标Url

    if args.u:
        globals.set_value("BaseURL_Path",args.u)

    if args.test:
        globals.set_value("Test","1")
        if args.testResponse:
            globals.set_value("TestResponse","1")
    
    writeJsonToDB.initialize()# 第一次使用时初始化数据库
    mongo_connector_module = mongoConnect.MongoConnector(host='localhost', port=27017, db_name='module')#这里连接数据库
    mongo_connector_module.connect()
    mongoModuledb=mongo_connector_module.get_database('module')
    globals.GlobalObjectStore.set_object("Omongo",mongoModuledb)# 将数据库连接对象放入全局参数中

    globals.GlobalObjectStore.set_object("Msg",MultiThreadCommunication())#消息队列对象，通过多线程实现的消息传递
    msg=globals.GlobalObjectStore.get_object("Msg")
    msg.start_listener()#启动监听

    if args.fingerprint:# 查询指纹
        printToConsole("数据库当前有以下指纹:","info")
        for finger in forMogoDB.returnFingerprints():
            printToConsole(f"{finger}","cyan")
        exit()

    if args.f:# 指定指纹
        if args.f in forMogoDB.returnFingerprints():
            globals.set_value("Fingerprint", args.f)

    if args.fp:# 查询Poc
        printToConsole(f"指纹{args.fp}在数据库中有以下Poc:","info")
        for Poc in forMogoDB.returnPocVuln(args.fp):
            printfa(f"{Poc}","cyan")
        exit()

    if args.v:
        globals.set_value("Poc",args.v)#设置Poc

    if args.t:
        globals.set_value("Threads",args.t)
    else:
        globals.set_value("Threads","4")

    

    printToFile(f"初始化完成,当前时间为:{system.get_time()},全局变量为:\n{globals.print_all_globals()}",globals.get_value("Report_Path"))

if __name__ == "__main__":
    initialize()
    try:
        print(globals.get_value("BaseURL_Path"))
        if globals.get_value("BaseURL_Path"):  # 指纹识别Poc检测流程
            if globals.get_value("Fingerprint") is None:
                fingerprint=app.fingerprintRecognition()
                if fingerprint:
                    globals.set_value("Fingerprint",fingerprint )# 指纹识别
                else:
                    printfa("指纹识别失败")  

            app.execPoc()  # 执行Poc

        if globals.get_value("Delete_database"):  # 重置数据库选项
            writeJsonToDB.reset()

    except KeyboardInterrupt:
        printfa("操作已取消", "warn")
    finally:
        globals.GlobalObjectStore.get_object("Msg").stop_listener()
        globals.GlobalObjectStore.get_object("Omongo").client.close()
        # printfa("数据库已断开", "message")
