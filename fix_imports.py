#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
修复项目导入路径的工具脚本
"""

import os
import re
import glob

# 定义导入映射关系 (old_import -> new_import)
IMPORT_MAP = {
    'from logger import': 'from src.utils.logger import',
    'import logger': 'from src.utils import logger',
    'from logo import': 'from src.utils.logo import',
    'import logo': 'from src.utils import logo',
    'from browser_utils import': 'from src.utils.browser_utils import',
    'import browser_utils': 'from src.utils import browser_utils',
    'from get_email_code import': 'from src.core.email_verification import',
    'import get_email_code': 'from src.core import email_verification',
    'from config import': 'from src.config.settings import',
    'import config': 'from src.config import settings',
    'from exit_cursor import': 'from src.core.exit_cursor import',
    'import exit_cursor': 'from src.core import exit_cursor',
    'from reset_machine import': 'from src.core.reset_machine import',
    'import reset_machine': 'from src.core import reset_machine',
    'from reset_appimage_machine import': 'from src.core.reset_appimage_machine import',
    'import reset_appimage_machine': 'from src.core import reset_appimage_machine',
    'from patch_cursor_get_machine_id import': 'from src.core.patch_cursor_get_machine_id import',
    'import patch_cursor_get_machine_id': 'from src.core import patch_cursor_get_machine_id',
    'from go_cursor_help import': 'from src.core.go_cursor_help import',
    'import go_cursor_help': 'from src.core import go_cursor_help',
    'from cursor_auth_manager import': 'from src.core.auth_manager import',
    'import cursor_auth_manager': 'from src.core import auth_manager'
}

def fix_imports_in_file(file_path):
    """修复单个文件中的导入路径"""
    print(f"正在处理: {file_path}")
    
    # 读取文件内容
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  读取文件失败: {str(e)}")
        return False
    
    # 替换导入路径
    original_content = content
    for old_import, new_import in IMPORT_MAP.items():
        content = content.replace(old_import, new_import)
    
    # 如果内容有变化，写回文件
    if content != original_content:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  已更新导入路径")
            return True
        except Exception as e:
            print(f"  写入文件失败: {str(e)}")
            return False
    else:
        print(f"  无需更新")
        return True

def fix_all_imports():
    """修复项目中所有Python文件的导入路径"""
    # 获取所有Python文件
    python_files = []
    for root_dir in ['src']:
        for py_file in glob.glob(f'{root_dir}/**/*.py', recursive=True):
            python_files.append(py_file)
    
    # 修复每个文件的导入
    success_count = 0
    fail_count = 0
    for file_path in python_files:
        if fix_imports_in_file(file_path):
            success_count += 1
        else:
            fail_count += 1
    
    # 输出统计信息
    print(f"\n处理完成")
    print(f"成功修复文件: {success_count}")
    print(f"处理失败文件: {fail_count}")

if __name__ == "__main__":
    fix_all_imports() 