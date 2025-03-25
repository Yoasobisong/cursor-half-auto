import os
import sys
import uuid
import logging
from colorama import Fore, Style, init

# 初始化colorama
init()

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
)

# 定义emoji常量
EMOJI = {
    "FILE": "📄",
    "BACKUP": "💾", 
    "SUCCESS": "✅",
    "ERROR": "❌",
    "INFO": "ℹ️",
    "RESET": "🔄",
}

def reset_machine_id():
    """重置AppImage版本Cursor的机器ID"""
    
    # AppImage版本的Cursor机器ID文件路径
    machine_id_path = os.path.expanduser("~/.config/Cursor/machineid")
    
    # 检查文件是否存在
    if not os.path.exists(machine_id_path):
        logging.error(f"{EMOJI['ERROR']} 帅哥,我找不到机器ID文件: {machine_id_path}")
        return False
    
    # 备份原始文件
    backup_path = f"{machine_id_path}.bak"
    try:
        with open(machine_id_path, 'r') as f:
            original_id = f.read().strip()
            
        with open(backup_path, 'w') as f:
            f.write(original_id)
        logging.info(f"{EMOJI['BACKUP']} 帅哥,我已经帮你备份好原始机器ID了: {original_id}")
    except Exception as e:
        logging.error(f"{EMOJI['ERROR']} 帅哥抱歉,备份机器ID失败了: {str(e)}")
        return False
    
    # 生成新的机器ID
    new_id = str(uuid.uuid4())
    
    # 写入新的机器ID
    try:
        with open(machine_id_path, 'w') as f:
            f.write(new_id)
        logging.info(f"{EMOJI['SUCCESS']} 帅哥,我已经帮你把机器ID重置为: {new_id}")
        return True
    except Exception as e:
        logging.error(f"{EMOJI['ERROR']} 帅哥抱歉,写入新机器ID失败了: {str(e)}")
        # 恢复备份
        try:
            with open(backup_path, 'r') as f:
                backup_id = f.read().strip()
            with open(machine_id_path, 'w') as f:
                f.write(backup_id)
            logging.info(f"{EMOJI['INFO']} 帅哥别担心,我已经恢复了原始机器ID")
        except:
            logging.error(f"{EMOJI['ERROR']} 帅哥对不起,连恢复原始机器ID都失败了")
        return False

if __name__ == "__main__":
    if reset_machine_id():
        logging.info(f"{EMOJI['SUCCESS']} 帅哥,AppImage版本Cursor机器ID重置成功了!")
    else:
        logging.error(f"{EMOJI['ERROR']} 帅哥抱歉,AppImage版本Cursor机器ID重置失败了!")