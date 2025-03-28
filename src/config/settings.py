from dotenv import load_dotenv
import os
import sys
from src.utils.logger import logging
import re

# 尝试加载.env文件
load_dotenv()

class Config:
    # 日志相关设置
    LOG_LEVEL = logging.INFO
    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    LOG_DIR = 'src/logs'
    
    # 浏览器相关设置
    HEADLESS = os.getenv('HEADLESS', 'false').lower() == 'true'
    USER_AGENT = os.getenv('USER_AGENT', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36')
    
    # 邮箱服务相关设置
    EMAIL_SERVICE = os.getenv('EMAIL_SERVICE', 'temp-mail')
    
    # 自动化相关设置
    WAIT_TIME = int(os.getenv('WAIT_TIME', '5'))
    RETRY_TIMES = int(os.getenv('RETRY_TIMES', '3'))
    
    # Cursor服务相关
    CURSOR_URL = os.getenv('CURSOR_URL', 'https://cursor.sh')
    def __init__(self):
        # 获取应用程序的根目录路径
        if getattr(sys, "frozen", False):
            # 如果是打包后的可执行文件
            application_path = os.path.dirname(sys.executable)
        else:
            # 如果是开发环境
            # 使用项目根目录而不是config目录
            application_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        # 指定 .env 文件的路径
        dotenv_path = os.path.join(application_path, ".env")

        if not os.path.exists(dotenv_path):
            raise FileNotFoundError(f"文件 {dotenv_path} 不存在，请在项目根目录创建.env文件")

        # 加载 .env 文件
        logging.info(f"从 {dotenv_path} 加载环境变量配置")
        load_dotenv(dotenv_path)

        self.imap = False
        self.temp_mail = os.getenv("TEMP_MAIL", "").strip().split("@")[0]
        self.temp_mail_epin = os.getenv("TEMP_MAIL_EPIN", "").strip()
        
        # 获取域名列表
        try:
            domain_str = os.getenv("DOMAIN", "[]").strip()
            
            # 如果不是以 [ 开头，说明是旧格式，需要转换
            if not domain_str.startswith("["):
                domain_str = f"['{domain_str}']"
            else:
                # 清理字符串
                # 1. 移除所有空格
                domain_str = domain_str.replace(" ", "")
                # 2. 移除多余的引号
                domain_str = domain_str.replace("''", "'")
                # 3. 确保每个域名都被引号包围
                if domain_str.startswith("[") and domain_str.endswith("]"):
                    # 移除首尾的 [] 
                    domains_temp = domain_str[1:-1]
                    # 按逗号分割
                    domains_list = domains_temp.split(",")
                    # 处理每个域名
                    cleaned_domains = []
                    for d in domains_list:
                        # 移除引号
                        d = d.strip("'").strip('"')
                        if d:  # 如果不是空字符串
                            cleaned_domains.append(d)
                    # 重新组装成正确的格式
                    domain_str = "['" + "','".join(cleaned_domains) + "']"
            
            try:
                self.domains = eval(domain_str)
            except:
                # 如果解析失败，尝试直接分割字符串
                domains_temp = domain_str.strip("[]").split(",")
                self.domains = [d.strip().strip("'").strip('"') for d in domains_temp if d.strip()]
            
            if not isinstance(self.domains, list):
                self.domains = [str(self.domains)]
            
            # 过滤掉空字符串
            self.domains = [d for d in self.domains if d.strip()]
            
            if len(self.domains) == 0:
                raise ValueError("没有配置域名")
            
            # 显示可用的域名列表
            print("\n可用的域名列表:")
            for i, domain in enumerate(self.domains, 1):
                print(f"{i}. {domain}")
                
            # 让用户选择域名
            while True:
                try:
                    choice = int(input("\n请选择域名 (输入数字): ").strip())
                    if 1 <= choice <= len(self.domains):
                        self.domain = self.domains[choice - 1]
                        break
                    else:
                        print("无效的选择，请重新输入")
                except ValueError:
                    print("请输入有效的数字")
                    
        except Exception as e:
            raise ValueError(f"域名配置错误: {str(e)}")

        # 如果临时邮箱为null则加载IMAP
        if self.temp_mail == "null":
            self.imap = True
            self.imap_server = os.getenv("IMAP_SERVER", "").strip()
            self.imap_port = os.getenv("IMAP_PORT", "").strip()
            
            # 获取IMAP用户和密码列表
            try:
                # 解析IMAP用户和密码列表
                imap_user_str = os.getenv("IMAP_USER", "[]").strip()
                imap_pass_str = os.getenv("IMAP_PASS", "[]").strip()
                
                # 如果不是以 [ 开头，说明是旧格式，需要转换
                if not imap_user_str.startswith("["):
                    imap_user_str = f"['{imap_user_str}']"
                if not imap_pass_str.startswith("["):
                    imap_pass_str = f"['{imap_pass_str}']"
                
                # 清理字符串
                def clean_list_str(s):
                    # 1. 移除注释（从#开始到行尾的内容）
                    s = re.sub(r'#.*$', '', s)
                    # 2. 移除所有空格和换行符
                    s = s.replace(' ', '').replace('\n', '')
                    # 3. 确保是列表格式
                    if not s.startswith('['):
                        s = f"['{s}']"
                    # 4. 规范化列表格式
                    s = s.replace('[', "['").replace(']', "']").replace(',', "','")
                    # 5. 修复可能的多余引号
                    s = s.replace("''", "'")
                    return s
                    
                imap_user_str = clean_list_str(imap_user_str)
                imap_pass_str = clean_list_str(imap_pass_str)
                
                self.imap_users = eval(imap_user_str)
                self.imap_passes = eval(imap_pass_str)
                
                if len(self.imap_users) != len(self.imap_passes):
                    raise ValueError("IMAP_USER 和 IMAP_PASS 的数量不匹配")
                
                if len(self.imap_users) == 0:
                    raise ValueError("没有配置IMAP账号")
                
                # 显示可用的账号列表
                print("\n可用的IMAP账号列表:")
                for i, user in enumerate(self.imap_users, 1):
                    print(f"{i}. {user}")
                    
                # 让用户选择账号
                while True:
                    try:
                        choice = int(input("\n请选择IMAP账号 (输入数字): ").strip())
                        if 1 <= choice <= len(self.imap_users):
                            self.imap_user = self.imap_users[choice - 1]
                            self.imap_pass = self.imap_passes[choice - 1]
                            print(f"帅哥,你选择了IMAP账号和密码: {self.imap_user}, {self.imap_pass}")
                            break
                        else:
                            print("无效的选择，请重新输入")
                    except ValueError:
                        print("请输入有效的数字")
                        
            except Exception as e:
                raise ValueError(f"IMAP配置错误: {str(e)}")
            
            self.imap_dir = os.getenv("IMAP_DIR", "inbox").strip()

        self.check_config()

    def get_temp_mail(self):
        return self.temp_mail

    def get_temp_mail_epin(self):
        return self.temp_mail_epin

    def get_domain(self):
        return self.domain

    def get_protocol(self):
        """获取邮件协议类型
        
        Returns:
            str: 'IMAP' 或 'POP3'
        """
        return os.getenv('IMAP_PROTOCOL', 'POP3')

    def get_imap(self):
        """获取IMAP配置信息"""
        if not self.imap:
            return False
        return {
            "imap_server": self.imap_server,
            "imap_port": self.imap_port,
            "imap_user": self.imap_user,
            "imap_pass": self.imap_pass,
            "imap_dir": self.imap_dir,
        }

    def check_config(self):
        """检查配置项是否有效

        检查规则：
        1. 如果使用 tempmail.plus，需要配置 TEMP_MAIL 和 DOMAIN
        2. 如果使用 IMAP，需要配置 IMAP_SERVER、IMAP_PORT、IMAP_USER、IMAP_PASS
        3. IMAP_DIR 是可选的
        """
        # 基础配置检查
        required_configs = {
            "domain": "域名",
        }

        # 检查基础配置
        for key, name in required_configs.items():
            if not self.check_is_valid(getattr(self, key)):
                raise ValueError(f"{name}未配置，请在 .env 文件中设置 {key.upper()}")

        # 检查邮箱配置
        if self.temp_mail != "null":
            # tempmail.plus 模式
            if not self.check_is_valid(self.temp_mail):
                raise ValueError("临时邮箱未配置，请在 .env 文件中设置 TEMP_MAIL")
        else:
            # IMAP 模式
            imap_configs = {
                "imap_server": "IMAP服务器",
                "imap_port": "IMAP端口",
                "imap_user": "IMAP用户名",
                "imap_pass": "IMAP密码",
            }

            for key, name in imap_configs.items():
                value = getattr(self, key)
                if value == "null" or not self.check_is_valid(value):
                    raise ValueError(
                        f"{name}未配置，请在 .env 文件中设置 {key.upper()}"
                    )

            # IMAP_DIR 是可选的，如果设置了就检查其有效性
            if self.imap_dir != "null" and not self.check_is_valid(self.imap_dir):
                raise ValueError(
                    "IMAP收件箱目录配置无效，请在 .env 文件中正确设置 IMAP_DIR"
                )

    def check_is_valid(self, value):
        """检查配置项是否有效

        Args:
            value: 配置项的值

        Returns:
            bool: 配置项是否有效
        """
        return isinstance(value, str) and len(str(value).strip()) > 0

    def print_config(self):
        if self.imap:
            logging.info(f"\033[32mIMAP服务器: {self.imap_server}\033[0m")
            logging.info(f"\033[32mIMAP端口: {self.imap_port}\033[0m")
            # 修改显示方式，使用相同长度的星号
            user_stars = '*' * 10
            pass_stars = '*' * 10
            logging.info(f"\033[32mIMAP用户名: {user_stars}\033[0m")
            logging.info(f"\033[32mIMAP密码: {pass_stars}\033[0m")
            logging.info(f"\033[32mIMAP收件箱目录: {self.imap_dir}\033[0m")
        if self.temp_mail != "null":
            logging.info(f"\033[32m临时邮箱: {self.temp_mail}@{self.domain}\033[0m")
        logging.info(f"\033[32m域名: {self.domain}\033[0m")


# 使用示例
if __name__ == "__main__":
    try:
        config = Config()
        print("环境变量加载成功！")
        config.print_config()
    except ValueError as e:
        print(f"错误: {e}")
