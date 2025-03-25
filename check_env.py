#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
检查项目环境脚本
"""

import os
import sys
import importlib
import traceback

def check_module(module_name):
    """检查模块是否可以导入"""
    try:
        importlib.import_module(module_name)
        print(f"✅ 模块 '{module_name}' 导入成功")
        return True
    except ModuleNotFoundError:
        print(f"❌ 模块 '{module_name}' 不存在")
        return False
    except ImportError as e:
        print(f"❌ 模块 '{module_name}' 导入错误: {str(e)}")
        traceback.print_exc()
        return False

def check_file(file_path):
    """检查文件是否存在"""
    if os.path.exists(file_path):
        print(f"✅ 文件 '{file_path}' 存在")
        return True
    else:
        print(f"❌ 文件 '{file_path}' 不存在")
        return False

def check_directory(dir_path):
    """检查目录是否存在"""
    if os.path.isdir(dir_path):
        print(f"✅ 目录 '{dir_path}' 存在")
        return True
    else:
        print(f"❌ 目录 '{dir_path}' 不存在")
        return False

def check_environment():
    """检查项目环境"""
    print("=== 检查项目环境 ===")
    
    # 检查Python版本
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"Python版本: {python_version}")
    
    # 检查目录结构
    directories = [
        "src",
        "src/core",
        "src/utils",
        "src/config",
        "src/logs",
        "src/build",
        "src/data"
    ]
    
    print("\n检查目录结构:")
    for directory in directories:
        check_directory(directory)
    
    # 检查关键文件
    files = [
        "src/core/cursor_keep_alive.py",
        "src/utils/logger.py",
        "src/utils/logo.py",
        "src/config/settings.py",
        "run.py"
    ]
    
    print("\n检查关键文件:")
    for file in files:
        check_file(file)
    
    # 检查模块导入
    modules = [
        "src",
        "src.core",
        "src.utils",
        "src.config",
        "src.utils.logger",
        "src.utils.logo",
        "src.core.cursor_keep_alive"
    ]
    
    print("\n检查模块导入:")
    for module in modules:
        check_module(module)
    
    # 检查依赖包
    dependencies = [
        "colorama",
        "dotenv",
        "requests"
    ]
    
    print("\n检查依赖包:")
    for dependency in dependencies:
        check_module(dependency)
    
    print("\n环境检查完成")

if __name__ == "__main__":
    check_environment() 