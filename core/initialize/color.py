# pKcScan © 2024.7.11 by cer1cc is licensed under CC BY-NC-SA 4.0 
# 导入 colorama 模块用于控制台输出的颜色
from core.library import colorama_init
from core.library import colorama_Fore, colorama_Style

# 初始化 colorama，设置 autoreset=True 以便在每次输出后重置颜色设置
colorama_init(autoreset=True)

# 定义 Colored 类，用于提供各种颜色的字符串输出方法
class Colored:
    @staticmethod
    def magenta(s):
        # 返回亮紫色字符串
        return colorama_Style.BRIGHT + colorama_Fore.MAGENTA + s + colorama_Fore.RESET + colorama_Style.RESET_ALL

    @staticmethod
    def green(s):
        # 返回亮绿色字符串
        return colorama_Style.BRIGHT + colorama_Fore.GREEN + s + colorama_Fore.RESET + colorama_Style.RESET_ALL

    @staticmethod
    def white(s):
        # 返回白色字符串
        return colorama_Fore.WHITE + s + colorama_Fore.RESET + colorama_Style.RESET_ALL

    @staticmethod
    def cyan(s):
        # 返回亮青色字符串
        return colorama_Style.BRIGHT + colorama_Fore.CYAN + s + colorama_Fore.RESET + colorama_Style.RESET_ALL

    @staticmethod
    def cyan_fine(s):
        # 返回青色字符串
        return colorama_Fore.CYAN + s + colorama_Fore.RESET + colorama_Style.RESET_ALL

    @staticmethod
    def yellow(s):
        # 返回亮黄色字符串
        return colorama_Style.BRIGHT + colorama_Fore.YELLOW + s + colorama_Fore.RESET + colorama_Style.RESET_ALL

    @staticmethod
    def red(s):
        # 返回亮红色字符串
        return colorama_Style.BRIGHT + colorama_Fore.RED + s + colorama_Fore.RESET + colorama_Style.RESET_ALL
    
    @staticmethod
    def green_message():
        return colorama_Style.BRIGHT + colorama_Fore.GREEN + "[Message]" + colorama_Fore.RESET + colorama_Style.RESET_ALL

    @staticmethod
    def yel_info():
        # 返回亮黄色的 "[INFO]" 标签字符串
        return colorama_Style.BRIGHT + colorama_Fore.YELLOW + "[INFO]" + colorama_Fore.RESET + colorama_Style.RESET_ALL

    @staticmethod
    def red_warn():
        # 返回亮红色的 "[WARN]" 标签字符串
        return colorama_Style.BRIGHT + colorama_Fore.RED + "[WARN]" + colorama_Fore.RESET + colorama_Style.RESET_ALL
    
    @staticmethod
    def cyan_input():
        # 返回亮红色的 "[WARN]" 标签字符串
        return colorama_Style.BRIGHT + colorama_Fore.RED + "[input]" + colorama_Fore.RESET + colorama_Style.RESET_ALL
    
    @staticmethod
    def magenta_test():
        # 返回亮紫色字符串
        return colorama_Style.BRIGHT + colorama_Fore.MAGENTA + "[TEST]" + colorama_Fore.RESET + colorama_Style.RESET_ALL

# 创建 Colored 类的实例
color = Colored()

# 测试 Colored 类的输出
def test_colored():
    color = Colored()
    
    print(color.magenta("This is magenta"))
    print(color.green("This is green"))
    print(color.white("This is white"))
    print(color.cyan("This is cyan"))
    print(color.cyan_fine("This is cyan fine"))
    print(color.yellow("This is yellow"))
    print(color.red("This is red"))
    print(color.yel_info() + " This is an info message")
    print(color.red_warn() + " This is a warning message")

if __name__ == "__main__":
    test_colored()