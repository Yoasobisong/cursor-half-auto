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
FORMAT = "%(asctime)s - %(message)s"
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
        
        # 获取项目根目录
        if getattr(sys, 'frozen', False):
            # 如果是打包后的可执行文件
            root_dir = os.path.dirname(sys.executable)
        else:
            # 如果是开发环境
            root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # 创建日志目录（使用绝对路径）
        log_dir = os.path.join(root_dir, 'src', 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        # 创建文件处理器，使用当前日期作为文件名
        current_date = datetime.now().strftime("%Y%m%d")
        log_file = os.path.join(log_dir, f'accounts_{current_date}.log')
        
        try:
            file_handler = logging.FileHandler(log_file, encoding='utf-8', mode='a')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
            self.logger.info(f"日志文件路径: {log_file}")
        except Exception as e:
            self.logger.error(f"创建日志文件失败: {str(e)}")
            self.logger.error(f"尝试创建的路径: {log_file}")
    
    def log_account(self, email, password):
        """记录账号信息"""
        try:
            message = f"帅哥,这是你的账号信息 | Email: {email} | Password: {password}"
            self.logger.info(message)
            return message
        except Exception as e:
            self.logger.error(f"记录账号信息失败: {str(e)}")
            return None
    
    def log_error(self, error_message):
        """记录错误信息"""
        try:
            message = f"帅哥,出现错误了: {error_message}"
            self.logger.error(message)
            return message
        except Exception as e:
            print(f"记录错误信息失败: {str(e)}")
            return None

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
