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
FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# 设置日志目录
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
ACCOUNT_LOG_DIR = LOG_DIR  # 账号日志与普通日志使用相同目录

# 确保日志目录存在
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 配置日志处理器
log_path = os.path.join(LOG_DIR, f"{datetime.now().strftime('%Y-%m-%d')}.log")
file_handler = logging.FileHandler(log_path, encoding="utf-8")
console_handler = logging.StreamHandler(sys.stdout)

# 设置格式
formatter = logging.Formatter(FORMAT, TIME_FORMAT)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# 配置根日志记录器
logging.basicConfig(
    level=logging.INFO,
    format=FORMAT,
    datefmt=TIME_FORMAT,
    handlers=[file_handler, console_handler]
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
        
        # 创建账号日志文件
        account_log_file = os.path.join(ACCOUNT_LOG_DIR, f"accounts_{datetime.now().strftime('%Y%m%d')}.log")
        account_handler = logging.FileHandler(account_log_file, encoding="utf-8")
        
        # 设置简洁的格式
        account_formatter = logging.Formatter("%(asctime)s - %(message)s")
        account_handler.setFormatter(account_formatter)
        
        # 添加处理器
        self.logger.addHandler(account_handler)
    
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
    logging.info(f"帅哥,日志系统已初始化,日志目录在: {os.path.abspath(LOG_DIR)}")
    logging.info("帅哥,应用程序已启动.")
    main_task()
    logging.info("帅哥,应用程序已退出.")
