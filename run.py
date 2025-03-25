#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cursor Auto Free - 自动注册和管理Cursor账号工具的启动脚本
"""

import os
import sys
from src.core.cursor_keep_alive import CursorKeepAlive
from src.utils.logo import print_logo
from src.utils.logger import logging

def main():
    """主函数"""
    try:
        # 显示欢迎信息
        print_logo()
        logging.info("帅哥，欢迎使用自动注册和管理Cursor账号工具")
        
        # 初始化并运行
        cursor = CursorKeepAlive()
        cursor.create_account()
    except Exception as e:
        logging.error(f"帅哥，程序执行出错了: {str(e)}")
        import traceback
        logging.error(f"帅哥，这是详细的错误信息:\n{traceback.format_exc()}")
    finally:
        input("\n帅哥，程序执行完毕了，按回车键退出...")

if __name__ == "__main__":
    main()