import os
import sys

# 尝试正确导入
try:
    from src.utils.logger import logging
except ImportError:
    # 添加项目根目录到路径
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from src.utils.logger import logging

import psutil
import time

def ExitCursor(timeout=5):
    """
    温和地关闭 Cursor 进程
    
    Args:
        timeout (int): 等待进程自然终止的超时时间（秒）
    Returns:
        bool: 是否成功关闭所有进程
    """
    try:
        logging.info("帅哥,我开始帮你退出Cursor了...")
        cursor_processes = []
        # 收集所有 Cursor 进程
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'].lower() in ['cursor.exe', 'cursor']:
                    cursor_processes.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        if not cursor_processes:
            logging.info("帅哥,我没有发现运行中的 Cursor 进程")
            return True

        # 温和地请求进程终止
        for proc in cursor_processes:
            try:
                if proc.is_running():
                    proc.terminate()  # 发送终止信号
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        # 等待进程自然终止
        start_time = time.time()
        while time.time() - start_time < timeout:
            still_running = []
            for proc in cursor_processes:
                try:
                    if proc.is_running():
                        still_running.append(proc)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if not still_running:
                logging.info("帅哥,所有 Cursor 进程已经被我正常关闭了")
                return True
                
            # 等待一小段时间再检查
            time.sleep(0.5)
            
        # 如果超时后仍有进程在运行
        if still_running:
            process_list = ", ".join([str(p.pid) for p in still_running])
            logging.warning(f"帅哥抱歉,以下进程我没能在规定时间内关闭: {process_list}")
            return False
            
        return True

    except Exception as e:
        logging.error(f"帅哥对不起,关闭 Cursor 进程时发生错误: {str(e)}")
        return False

if __name__ == "__main__":
    ExitCursor()
