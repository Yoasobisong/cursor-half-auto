import os
import sys

# 将项目根目录添加到系统路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.cursor_keep_alive import CursorKeepAlive
from src.utils.logger import AccountLogger
from src.utils.logo import print_logo

def main():
    try:
        print_logo()
        print("帅哥,欢迎使用 Cursor Auto Free")
        cursor_keep_alive = CursorKeepAlive()
        cursor_keep_alive.create_account()
    except Exception as e:
        logger = AccountLogger()
        logger.log_error(f"帅哥抱歉,出现了一个错误: {str(e)}")
        print(f"帅哥抱歉,发生错误: {str(e)}")
    finally:
        input("\n帅哥,程序执行完毕了,按回车键退出...")

if __name__ == "__main__":
    main()