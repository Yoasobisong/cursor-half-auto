# cursor-half-auto

自动化Cursor AI注册和免费使用的解决方案，支持浏览器可见模式。

## 特性

- 自动注册Cursor账号
- 浏览器可见模式，方便观察自动化过程
- 交互式Turnstile验证过程，支持用户手动验证
- 支持IMAP邮箱验证
- 自动重置机器码
  
## windows直接使用

 - release里已经发布了exe，只需要配置.env便可以直接使用
   
## 安装

```bash
# 克隆仓库
git clone https://github.com/Yoasobisong/cursor-half-auto.git
cd cursor-half-auto

# 安装依赖
pip install -r requirements.txt
```

## 使用方法

1. 复制`.env.example`文件并重命名为`.env`
2. 根据需要修改配置文件
3. 运行程序

```bash
python run.py
```

## 配置选项

在`.env`文件中可以配置以下选项：

- `DOMAIN`: Cloudflare域名
- `TEMP_MAIL`: 临时邮箱设置
- `IMAP_*`: IMAP邮箱设置
- `BROWSER_HEADLESS`: 浏览器无头模式设置(True/False)

## 验证过程

当程序遇到Turnstile验证时，将暂停执行并等待用户手动完成验证，完成后按Enter键继续程序执行。

## 贡献指南

欢迎提交Pull Request或Issues来改进这个项目。

## 许可证

MIT 
