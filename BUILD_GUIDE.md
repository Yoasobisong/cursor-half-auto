# Cursor Half Auto 构建指南

本指南提供多种方式来使用Cursor Half Auto，包括从源码运行、手动构建可执行文件以及通过GitHub Actions自动构建。

## 方法1：直接从源码运行（推荐给开发者）

### 前提条件
- Python 3.8+ 
- Git

### 步骤
1. 克隆仓库
```bash
git clone https://github.com/Yoasobisong/cursor-half-auto.git
cd cursor-half-auto
```

2. 安装依赖
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

3. 配置环境变量
```bash
cp .env.example .env
# 使用文本编辑器修改.env文件中的配置
```

4. 运行程序
```bash
python run.py
```

## 方法2：手动构建Windows可执行文件（适用于Windows用户）

### 前提条件
- Windows系统
- Python 3.8+
- Git

### 步骤
1. 克隆仓库
```bash
git clone https://github.com/Yoasobisong/cursor-half-auto.git
cd cursor-half-auto
```

2. 安装依赖
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install pyinstaller
```

3. 构建可执行文件
```bash
# 在Windows命令提示符中运行：
python -m PyInstaller --noconfirm --onefile --console ^
  --add-data "src/data;src/data" ^
  --add-data ".env.example;." ^
  --add-data "turnstilePatch;turnstilePatch" ^
  --add-data "src/main.py;src" ^
  --name "CursorAutoFree" ^
  --hidden-import=dotenv ^
  --hidden-import=requests ^
  --hidden-import=colorama ^
  --hidden-import=DrissionPage ^
  --hidden-import=selenium ^
  --hidden-import=webdriver_manager ^
  "run.py"
```

4. 创建启动脚本
```bash
# 在dist目录中创建启动程序.bat文件，内容如下：
@echo off
title Cursor Half Auto
echo 正在启动Cursor Half Auto...
CursorAutoFree.exe
pause
```

5. 复制配置文件
```bash
copy .env.example dist\.env
```

6. 运行程序
```bash
# 双击dist目录中的"启动程序.bat"文件
```

## 方法3：通过GitHub Actions自动构建（适用于所有用户）

该仓库配置了GitHub Actions，可以自动构建Windows可执行文件。

### 手动触发构建
1. 访问 https://github.com/Yoasobisong/cursor-half-auto/actions/workflows/build_windows.yml
2. 点击右上角的"Run workflow"按钮
3. 选择分支（通常是"main"）并点击"Run workflow"
4. 等待工作流完成
5. 在工作流运行页面下载构建产物（Artifacts）中的"CursorAutoFree_Windows"

### 从Release下载
如果已经有Release版本，可以直接从Release页面下载预构建的可执行文件：
1. 访问 https://github.com/Yoasobisong/cursor-half-auto/releases
2. 下载最新版本的"CursorAutoFree_Windows.zip"文件
3. 解压缩并运行"启动程序.bat"

## 问题排查

### 程序启动问题
- **问题: 缺少DLL文件**
  - 解决方案: 安装Visual C++ Redistributable Package

- **问题: 杀毒软件拦截**
  - 解决方案: 将程序添加到杀毒软件的白名单

### 运行时问题
- **问题: 浏览器无法启动**
  - 解决方案: 确保已安装Chrome或其他支持的浏览器

- **问题: turnstilePatch目录缺失**
  - 解决方案: 确保从release下载的压缩包完整解压，或从源码仓库重新获取

如需更多帮助，请在GitHub仓库中提交Issue。 