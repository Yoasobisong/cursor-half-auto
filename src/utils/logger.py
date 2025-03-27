import logging
import os
import sys
import traceback
from datetime import datetime

# 日志级别映射
LOG_LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}

# 配置日志格式
FORMAT = "%(message)s"
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# 配置控制台处理器
console_handler = logging.StreamHandler(sys.stdout)

# 设置格式
formatter = logging.Formatter(FORMAT, TIME_FORMAT)
console_handler.setFormatter(formatter)

# 配置根日志记录器
logging.basicConfig(
    level=logging.INFO,
    format=FORMAT,
    datefmt=TIME_FORMAT,
    handlers=[console_handler]
)

# 初始化主日志记录器
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

class AccountLogger:
    """账号信息日志类"""
    def __init__(self):
        # 创建专门用于账号信息的日志记录器
        self.logger = logging.getLogger('account_logger')
        self.logger.setLevel(logging.INFO)
        
        # 清除现有的处理器
        self.logger.handlers = []
        
        # 添加控制台处理器
        self.logger.addHandler(console_handler)
    
    def log_account(self, email, password):
        """记录账号信息"""
        self.logger.info(f"帅哥,这是你的账号信息 | Email: {email} | Password: {password}")
    
    def log_error(self, error_message):
        """记录错误信息"""
        self.logger.error(f"帅哥,出现错误了: {error_message}")

# 为测试而添加的代码
def main_task():
    """模拟主要任务，用于测试日志系统"""
    logging.info("帅哥,我正在启动主要任务...")
    try:
        # 模拟一个错误
        raise ValueError("Simulated error occurred.")
    except Exception as e:
        logging.error(f"帅哥,发生了{type(e).__name__}错误: {str(e)}")
        logging.debug(f"帅哥,这是详细的错误信息:\n{traceback.format_exc()}")
    finally:
        logging.info("帅哥,任务执行完成了.")

if __name__ == "__main__":
    logging.info("帅哥,应用程序已启动.")
    main_task()
    logging.info("帅哥,应用程序已退出.")
