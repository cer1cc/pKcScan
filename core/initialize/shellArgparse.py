# pKcScan © 2024.7.11 by cer1cc is licensed under CC BY-NC-SA 4.0 
from core.library import argparse

def shellArgparse():
    parser = argparse.ArgumentParser(description='这是一个通过Poc检测漏洞的脚本')
    parser.add_argument('-u', type=str, help='传入目标Url')
    parser.add_argument('-r', action='store_true', help='将清空数据库')
    parser.add_argument('-f', type=str, help='将会直接使用该指纹,跳过指纹识别(但是该指纹必须存在)')
    parser.add_argument('-v', type=str, help='将会使用该Poc(但是该Poc必须存在)')
    parser.add_argument('-t', type=str, help='多线程线程数，默认为4')
    parser.add_argument('-p', type=str, help='暴力破解时将使用该payload, 例如 -r password-attacks+top100.txt,默认也会使用这个')
    parser.add_argument('-fp', type=str, help='查看该指纹对应的Poc, 例如-fp pikachu')

    parser.add_argument('--payload', action='store_true', help='查看全部Payload')
    parser.add_argument('--report', action='store_true', help='使用该选项就会生成日志(记录)')
    parser.add_argument('--fingerprint', action='store_true', help='查看全部指纹')
    parser.add_argument('--test', action='store_true', help='开启调试模式,将会看到更多信息')
    parser.add_argument('--testResponse', action='store_true', help='必须开启调试模式,查看响应包,例: --test --testResponse')

    return parser.parse_args()
