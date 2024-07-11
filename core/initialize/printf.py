# pKcScan © 2024.7.11 by cer1cc is licensed under CC BY-NC-SA 4.0 
# 该脚本用于统一管理输出，并形成报告(日志)
import os
import errno
import threading
import queue
# 从 core.initialize 导入 color 对象
from core.initialize.color import color
from core.initialize import globals

def printToConsole(msg, color_name='normal'):
    """
    打印消息到控制台，并根据指定的颜色进行着色
    :param msg: 要打印的消息
    :param color_name: 指定的颜色名称，默认为 'normal'
    """
    if not isinstance(msg, str):
        try:
            msg = str(msg)
        except Exception as e:
            print("Error converting message to string:", e)
            return

    if color_name == 'magenta':
        print(color.magenta(msg))
    elif color_name == 'green':
        print(color.green(msg))
    elif color_name == 'white':
        print(color.white(msg))
    elif color_name == 'cyan':
        print(color.cyan(msg))
    elif color_name == 'cyan_fine':
        print(color.cyan_fine(msg))
    elif color_name == 'yellow':
        print(color.yellow(msg))
    elif color_name == 'red':
        print(color.red(msg))
    elif color_name == 'info':
        print(color.yel_info() + " " + msg)
    elif color_name == 'warn':
        print(color.red_warn() + " " + msg)
    elif color_name == 'message':
        print(color.green_message() + " " + msg)
    elif color_name == 'input':
        print(color.cyan_input() + " " + msg)
    elif color_name == 'test':
        print(color.magenta_test() + " " + msg) 
    else:
        print(msg)


def printToFile(msg, file_path=None):
    """
    将消息写入文件
    :param msg: 要写入的消息
    :param file_path: 文件路径，默认为 Report_Path
    """
    if file_path is None:
        file_path = globals.get_value("Report_Path")

    if not isinstance(msg, str):
        try:
            msg = str(msg)
        except Exception as e:
            print("Error converting message to string:", e)
            return

    try:
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(msg + '\n')
    except FileNotFoundError:
        # 如果文件不存在，创建文件并写入消息
        try:
            os.makedirs(os.path.dirname(file_path))
        except OSError as e:
            if e.errno != errno.EEXIST:
                # 如果创建文件夹失败，打印错误信息
                print("Failed to create directory:", os.path.dirname(file_path))
                print("Error:", e)
                return
        # 创建文件后再次尝试写入消息
        try:
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(msg + '\n')
        except Exception as e:
            # 如果写入消息失败，打印错误信息
            print("Failed to write to file:", file_path)
            print("Error:", e)

def clear_file(file_path=None):
    """
    清空文件内容
    :param file_path: 文件路径，默认为 Report_Path
    """
    if file_path is None:
        file_path = globals.get_value("Report_Path")

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            pass  # 只打开文件并立即关闭，以清空内容
    except FileNotFoundError:
        # 如果文件不存在，创建文件夹
        try:
            os.makedirs(os.path.dirname(file_path))
        except OSError as e:
            if e.errno != errno.EEXIST:
                # 如果创建文件夹失败，打印错误信息
                print("Failed to create directory:", os.path.dirname(file_path))
                print("Error:", e)
                return
        # 创建文件后再次尝试清空文件内容
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                pass
        except Exception as e:
            # 如果清空文件内容失败，打印错误信息
            print("Failed to clear file:", file_path)
            print("Error:", e)


def printfa(msg, color_name='normal'):
    """
    打印消息到控制台和文件，并根据指定的颜色进行着色
    :param msg: 要打印的消息
    :param color_name: 指定的颜色名称，默认为 'normal'
    """
    printToConsole(msg, color_name)
    printToFile(msg, globals.get_value("Report_Path"))


class MultiThreadCommunication:
    def __init__(self):
        """
        初始化多线程通信类，创建消息队列和监听线程。
        """
        self.message_queue = queue.Queue()  # 创建一个线程安全的队列用于线程间通信
        self.listener_thread = threading.Thread(target=self._listener)  # 创建监听线程
        self.listener_thread.daemon = True  # 将监听线程设置为守护线程

    def start_listener(self):
        """
        启动监听线程。
        """
        self.listener_thread.start()  # 启动监听线程

    def _listener(self):
        """
        监听线程的目标函数，不断从消息队列中获取消息并打印。
        """
        msgs = []
        while True:
            message = self.message_queue.get()  # 从队列中获取消息
            if message.get("key") == "system" and message.get("msg") == "STOP":
                self.prints(msgs)
                break
            msgs.append(message)  # 添加消息到列表
    
    def prints(self, msgs):
        for msg in msgs:
            for key, msgstr in msg.items():
                printfa(msgstr, key)


    def send_message(self, message):
        """
        发送消息到队列。
        
        参数:
        message (dict): 包含键和值的消息字典。
        """
        self.message_queue.put(message)  # 将消息放入队列


    def stop_listener(self):
        """
        停止监听线程。
        """
        self.send_message({"key": "system", "msg": "STOP"})  # 发送 "STOP" 消息，通知监听线程停止
        self.listener_thread.join()  # 等待监听线程结束

# 示例发送线程函数
def sender_function(comm):
    """
    发送线程的目标函数，执行任务并发送消息到队列。

    参数:
    comm (MultiThreadCommunication): 多线程通信类实例。
    """
    import time
    for i in range(10):
        time.sleep(1)  # 模拟任务执行
        message = f"Message {i}"
        print(f"Sender sending: {message}")
        comm.send_message(message)  # 发送消息到队列
    comm.stop_listener()  # 任务完成后，停止监听线程
