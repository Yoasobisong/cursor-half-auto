import os
import platform
import json
import sys
import time
import random
from colorama import Fore, Style
from enum import Enum
from typing import Optional
from datetime import datetime
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

try:
    from src.core.exit_cursor import ExitCursor
    from src.core import go_cursor_help
    from src.core import patch_cursor_get_machine_id
    from src.core.reset_machine import MachineIDResetter
    from src.core import reset_appimage_machine
    from src.utils.logger import logging
    from src.utils.browser_utils import BrowserManager
    from src.core.email_verification import EmailVerificationHandler
    from src.utils.logo import print_logo
    from src.config.settings import Config
    from src.core.auth_manager import CursorAuthManager
    from src.utils.logger import AccountLogger
except ImportError:
    # 尝试使用相对导入
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from src.core.exit_cursor import ExitCursor
    from src.core import go_cursor_help
    from src.core import patch_cursor_get_machine_id
    from src.core.reset_machine import MachineIDResetter
    from src.core import reset_appimage_machine
    from src.utils.logger import logging
    from src.utils.browser_utils import BrowserManager
    from src.core.email_verification import EmailVerificationHandler
    from src.utils.logo import print_logo
    from src.config.settings import Config
    from src.core.auth_manager import CursorAuthManager
    from src.utils.logger import AccountLogger

os.environ["PYTHONVERBOSE"] = "0"
os.environ["PYINSTALLER_VERBOSE"] = "0"

# 定义 EMOJI 字典
EMOJI = {"ERROR": "❌", "WARNING": "⚠️", "INFO": "ℹ️"}


class VerificationStatus(Enum):
    """验证状态枚举"""

    PASSWORD_PAGE = "@name=password"
    CAPTCHA_PAGE = "@data-index=0"
    ACCOUNT_SETTINGS = "Account Settings"


class TurnstileError(Exception):
    """Turnstile 验证相关异常"""

    pass


def save_screenshot(tab, stage: str, timestamp: bool = True) -> None:
    """
    保存页面截图

    Args:
        tab: 浏览器标签页对象
        stage: 截图阶段标识
        timestamp: 是否添加时间戳
    """
    try:
        # 创建 screenshots 目录
        screenshot_dir = "screenshots"
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)

        # 生成文件名
        if timestamp:
            filename = f"turnstile_{stage}_{int(time.time())}.png"
        else:
            filename = f"turnstile_{stage}.png"

        filepath = os.path.join(screenshot_dir, filename)

        # 保存截图
        tab.get_screenshot(filepath)
        logging.debug(f"帅哥,截图已保存: {filepath}")
    except Exception as e:
        logging.warning(f"帅哥,截图保存失败: {str(e)}")


def check_verification_success(tab) -> Optional[VerificationStatus]:
    """
    检查验证是否成功

    Returns:
        VerificationStatus: 验证成功时返回对应状态，失败返回 None
    """
    for status in VerificationStatus:
        if tab.ele(status.value):
            logging.info(f"帅哥,验证成功 - 已到达{status.name}页面")
            return status
    return None


def handle_turnstile(tab, max_retries: int = 2, retry_interval: tuple = (1, 2)) -> bool:
    """
    处理 Turnstile 验证 - 等待用户按Enter继续

    Args:
        tab: 浏览器标签页对象
        max_retries: 最大重试次数 (不再使用)
        retry_interval: 重试间隔时间范围 (不再使用)

    Returns:
        bool: 验证是否成功
    """
    logging.info("帅哥,检测到 Turnstile 验证...")
    logging.info("帅哥,浏览器界面已显示，请手动操作浏览器完成验证后按 Enter 键继续...")
    save_screenshot(tab, "start")
    
    # 等待用户按下Enter键
    input("帅哥,完成验证后请按 Enter 键继续...")
    
    logging.info("帅哥,继续执行后续步骤")
    save_screenshot(tab, "success")
    return True
    
    # 原代码（已注释）
    """
    logging.info("帅哥,正在检测 Turnstile 验证...")
    save_screenshot(tab, "start")

    retry_count = 0

    try:
        while retry_count < max_retries:
            retry_count += 1
            logging.debug(f"帅哥,第 {retry_count} 次尝试验证")

            try:
                # 定位验证框元素
                challenge_check = (
                    tab.ele("@id=cf-turnstile", timeout=2)
                    .child()
                    .shadow_root.ele("tag:iframe")
                    .ele("tag:body")
                    .sr("tag:input")
                )

                if challenge_check:
                    logging.info("帅哥,检测到 Turnstile 验证框，开始处理...")
                    # 随机延时后点击验证
                    time.sleep(random.uniform(1, 3))
                    challenge_check.click()
                    time.sleep(2)

                    # 保存验证后的截图
                    save_screenshot(tab, "clicked")

                    # 检查验证结果
                    if check_verification_success(tab):
                        logging.info("帅哥,Turnstile 验证通过")
                        save_screenshot(tab, "success")
                        return True

            except Exception as e:
                logging.debug(f"帅哥,当前尝试未成功: {str(e)}")

            # 检查是否已经验证成功
            if check_verification_success(tab):
                return True

            # 随机延时后继续下一次尝试
            time.sleep(random.uniform(*retry_interval))

        # 超出最大重试次数
        logging.error(f"帅哥,验证失败 - 已达到最大重试次数 {max_retries}")
        logging.error(
            "帅哥,请前往开源项目查看更多信息：https://github.com/chengazhen/cursor-auto-free"
        )
        save_screenshot(tab, "failed")
        return False

    except Exception as e:
        error_msg = f"帅哥,Turnstile 验证过程发生异常: {str(e)}"
        logging.error(error_msg)
        save_screenshot(tab, "error")
        raise TurnstileError(error_msg)
    """


def get_cursor_session_token(tab, max_attempts=3, retry_interval=2):
    """
    获取Cursor会话token，带有重试机制
    :param tab: 浏览器标签页
    :param max_attempts: 最大尝试次数
    :param retry_interval: 重试间隔(秒)
    :return: session token 或 None
    """
    logging.info("帅哥,开始获取cookie")
    attempts = 0

    while attempts < max_attempts:
        try:
            cookies = tab.cookies()
            for cookie in cookies:
                if cookie.get("name") == "WorkosCursorSessionToken":
                    return cookie["value"].split("%3A%3A")[1]

            attempts += 1
            if attempts < max_attempts:
                logging.warning(
                    f"帅哥,第 {attempts} 次尝试未获取到CursorSessionToken，{retry_interval}秒后重试..."
                )
                time.sleep(retry_interval)
            else:
                logging.error(
                    f"帅哥,已达到最大尝试次数({max_attempts})，获取CursorSessionToken失败"
                )

        except Exception as e:
            logging.error(f"帅哥,获取cookie失败: {str(e)}")
            attempts += 1
            if attempts < max_attempts:
                logging.info(f"帅哥,将在 {retry_interval} 秒后重试...")
                time.sleep(retry_interval)

    return None


def update_cursor_auth(email=None, access_token=None, refresh_token=None):
    """
    更新Cursor的认证信息的便捷函数
    """
    auth_manager = CursorAuthManager()
    return auth_manager.update_auth(email, access_token, refresh_token)


def sign_up_account(browser, tab, sign_up_url, account, password, first_name, last_name, email_handler, settings_url):
    logging.info("帅哥,=== 开始注册账号流程 ===")
    logging.info(f"帅哥,正在访问注册页面: {sign_up_url}")
    tab.get(sign_up_url)

    try:
        if tab.ele("@name=first_name"):
            logging.info("帅哥,正在填写个人信息...")
            tab.actions.click("@name=first_name").input(first_name)
            logging.info(f"帅哥,已输入名字: {first_name}")
            time.sleep(random.uniform(1, 3))

            tab.actions.click("@name=last_name").input(last_name)
            logging.info(f"帅哥,已输入姓氏: {last_name}")
            time.sleep(random.uniform(1, 3))

            tab.actions.click("@name=email").input(account)
            logging.info(f"帅哥,已输入邮箱: {account}")
            time.sleep(random.uniform(1, 3))

            logging.info("帅哥,提交个人信息...")
            tab.actions.click("@type=submit")

    except Exception as e:
        logging.error(f"帅哥,注册页面访问失败: {str(e)}")
        return False

    handle_turnstile(tab)

    try:
        if tab.ele("@name=password"):
            logging.info("帅哥,正在设置密码...")
            tab.ele("@name=password").input(password)
            time.sleep(random.uniform(1, 3))

            logging.info("帅哥,提交密码...")
            tab.ele("@type=submit").click()
            logging.info("帅哥,密码设置完成，等待系统响应...")

    except Exception as e:
        logging.error(f"帅哥,密码设置失败: {str(e)}")
        return False

    if tab.ele("This email is not available."):
        logging.error("帅哥,注册失败：邮箱已被使用")
        return False

    handle_turnstile(tab)

    while True:
        try:
            if tab.ele("Account Settings"):
                logging.info("帅哥,注册成功 - 已进入账户设置页面")
                break
            if tab.ele("@data-index=0"):
                logging.info("帅哥,正在获取邮箱验证码...")
                code = email_handler.get_verification_code()
                if not code:
                    logging.error("帅哥,获取验证码失败")
                    return False

                logging.info(f"帅哥,成功获取验证码: {code}")
                logging.info("帅哥,正在输入验证码...")
                i = 0
                for digit in code:
                    tab.ele(f"@data-index={i}").input(digit)
                    time.sleep(random.uniform(0.1, 0.3))
                    i += 1
                logging.info("帅哥,验证码输入完成")
                break
        except Exception as e:
            logging.error(f"帅哥,验证码处理过程出错: {str(e)}")

    handle_turnstile(tab)
    wait_time = random.randint(3, 6)
    for i in range(wait_time):
        logging.info(f"帅哥,等待系统处理中... 剩余 {wait_time-i} 秒")
        time.sleep(1)

    logging.info("帅哥,正在获取账户信息...")
    tab.get(settings_url)
    try:
        usage_selector = (
            "css:div.col-span-2 > div > div > div > div > "
            "div:nth-child(1) > div.flex.items-center.justify-between.gap-2 > "
            "span.font-mono.text-sm\\/\\[0\\.875rem\\]"
        )
        usage_ele = tab.ele(usage_selector)
        if usage_ele:
            usage_info = usage_ele.text
            total_usage = usage_info.split("/")[-1].strip()
            logging.info(f"帅哥,账户可用额度上限: {total_usage}")
            logging.info(
                "帅哥,请前往开源项目查看更多信息：https://github.com/chengazhen/cursor-auto-free"
            )
    except Exception as e:
        logging.error(f"帅哥,获取账户额度信息失败: {str(e)}")

    logging.info("\n帅哥,=== 注册完成 ===")
    account_info = f"帅哥,Cursor 账号信息:\n邮箱: {account}\n密码: {password}"
    logging.info(account_info)
    time.sleep(5)
    return True


class EmailGenerator:
    def __init__(
        self,
        config=None,
        password="".join(
            random.choices(
                "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*",
                k=12,
            )
        ),
    ):
        self.config = config if config else Config()
        self.domain = self.config.get_domain()
        self.names = self.load_names()
        self.default_password = password
        self.default_first_name = self.generate_random_name()
        self.default_last_name = self.generate_random_name()

    def load_names(self):
        try:
            names_file = "src/data/names-dataset.txt"
            with open(names_file, "r") as file:
                return file.read().split()
        except FileNotFoundError:
            # 尝试其他可能的路径
            alternative_paths = ["names-dataset.txt", "../data/names-dataset.txt", "data/names-dataset.txt"]
            for path in alternative_paths:
                try:
                    with open(path, "r") as file:
                        return file.read().split()
                except FileNotFoundError:
                    continue
            
            # 如果所有路径都不存在，返回一些默认名称
            logging.warning("帅哥,无法找到名称数据集文件，使用默认名称")
            return ["john", "jane", "alex", "emma", "michael", "olivia", "william", "sophia"]

    def generate_random_name(self):
        """生成随机用户名"""
        return random.choice(self.names)

    def generate_email(self, length=4):
        """生成随机邮箱地址"""
        length = random.randint(0, length)  # 生成0到length之间的随机整数
        timestamp = str(int(time.time()))[-length:]  # 使用时间戳后length位
        return f"{self.default_first_name}{timestamp}@{self.domain}"

    def get_account_info(self):
        """获取完整的账号信息"""
        return {
            "email": self.generate_email(),
            "password": self.default_password,
            "first_name": self.default_first_name,
            "last_name": self.default_last_name,
        }


def get_user_agent():
    """获取user_agent"""
    try:
        # 使用JavaScript获取user agent
        browser_manager = BrowserManager()
        browser = browser_manager.init_browser()
        user_agent = browser.latest_tab.run_js("return navigator.userAgent")
        browser_manager.quit()
        return user_agent
    except Exception as e:
        logging.error(f"帅哥,获取user agent失败: {str(e)}")
        return None


def check_cursor_version():
    """检查Cursor版本"""
    try:
        # 尝试获取Cursor路径
        paths = patch_cursor_get_machine_id.get_cursor_paths()
        if paths is None:
            # 如果找不到路径，假设版本小于0.45
            logging.warning("帅哥，找不到Cursor安装路径，假设版本小于0.45")
            return False
            
        pkg_path, main_path = paths
        return patch_cursor_get_machine_id.check_cursor_version(pkg_path, main_path)
    except OSError:
        # 如果找不到Cursor安装路径，检查是否是AppImage版本
        logging.info("帅哥，未找到标准安装路径的Cursor，尝试查找AppImage版本...")
        appimage_path = os.path.expanduser("~/.config/Cursor/machineid")
        if os.path.exists(appimage_path):
            logging.info("帅哥，检测到AppImage版本的Cursor")
            return False  # 假设AppImage版本小于0.45
        else:
            logging.warning("帅哥，无法找到任何版本的Cursor，假设版本小于0.45")
            return False


def reset_machine_id(greater_than_0_45):
    # 先检查是否是AppImage版本
    appimage_path = os.path.expanduser("~/.config/Cursor/machineid")
    if os.path.exists(appimage_path):
        logging.info("帅哥,检测到AppImage版本的Cursor，使用专用重置方法...")
        return reset_appimage_machine.reset_machine_id()
    
    # 原有的重置逻辑
    if greater_than_0_45:
        # 提示请手动执行脚本 https://github.com/chengazhen/cursor-auto-free/blob/main/patch_cursor_get_machine_id.py
        go_cursor_help.go_cursor_help()
    else:
        MachineIDResetter().reset_machine_ids()


def print_end_message():
    logging.info("\n\n\n\n\n")
    logging.info("=" * 30)
    logging.info("帅哥,所有操作已完成")
    print_logo()


class CursorKeepAlive:
    def __init__(self):
        self.logger = AccountLogger()
        self.greater_than_0_45 = check_cursor_version()
        self.browser_manager = None
        self.config = Config()  # 创建一个Config实例

    def create_account(self):
        logging.info("\n帅哥,=== handsome boy please choose ===")
        # ExitCursor()

        # 提示用户选择操作模式
        print("\n帅哥,handsome boy please 操作模式:")
        print("1. 仅重置机器码")
        print("2. 完整注册流程")

        while True:
            try:
                choice = int(input("请输入选项 (1 或 2): ").strip())
                if choice in [1, 2]:
                    break
                else:
                    print("无效的选项,请重新输入")
            except ValueError:
                print("请输入有效的数字")

        if choice == 1:
            # 仅执行重置机器码
            reset_machine_id(self.greater_than_0_45)
            logging.info("帅哥,机器码重置完成")
            print_end_message()
            sys.exit(0)

        logging.info("帅哥,正在初始化浏览器...")

        # 获取user_agent
        user_agent = get_user_agent()
        if not user_agent:
            logging.error("帅哥,获取user agent失败，使用默认值")
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

        # 剔除user_agent中的"HeadlessChrome"
        user_agent = user_agent.replace("HeadlessChrome", "Chrome")

        self.browser_manager = BrowserManager()
        browser = self.browser_manager.init_browser(user_agent)

        # 获取并打印浏览器的user-agent
        user_agent = browser.latest_tab.run_js("return navigator.userAgent")

        logging.info("\n帅哥,=== 帅哥这是你的配置信息配置信息 ===")
        login_url = "https://authenticator.cursor.sh"
        sign_up_url = "https://authenticator.cursor.sh/sign-up"
        settings_url = "https://www.cursor.com/settings"
        mail_url = "https://tempmail.plus"

        logging.info("帅哥,正在生成随机账号信息...")

        email_generator = EmailGenerator(config=self.config)  # 传入已有的Config实例
        first_name = email_generator.default_first_name
        last_name = email_generator.default_last_name
        account = email_generator.generate_email()
        password = email_generator.default_password

        logging.info(f"帅哥,这是生成的邮箱账号: {account}")

        logging.info("帅哥,正在初始化邮箱验证模块...")
        email_handler = EmailVerificationHandler(account, config=self.config)

        auto_update_cursor_auth = True

        tab = browser.latest_tab

        tab.run_js("try { turnstile.reset() } catch(e) { }")

        logging.info("\n帅哥,=== 开始注册流程 ===")
        logging.info(f"帅哥,正在访问登录页面: {login_url}")
        tab.get(login_url)

        if sign_up_account(self.browser_manager, tab, sign_up_url, account, password, first_name, last_name, email_handler, settings_url):
            logging.info("帅哥,正在获取会话令牌...")
            token = get_cursor_session_token(tab)
            if token:
                logging.info("帅哥,正在更新认证信息...")
                update_cursor_auth(
                    email=account, access_token=token, refresh_token=token
                )
                logging.info(
                    "帅哥,请前往开源项目查看更多信息：https://github.com/chengazhen/cursor-auto-free"
                )
                logging.info("帅哥,正在重置机器码...")
                reset_machine_id(self.greater_than_0_45)
                logging.info("帅哥,所有操作已完成")
                print_end_message()
                self.logger.log_account(account, password)
            else:
                logging.error("帅哥,获取会话令牌失败，注册流程未完成")

    def handle_error(self, error):
        self.logger.log_error(str(error))
        import traceback
        logging.error(traceback.format_exc())
        
    def cleanup(self):
        if self.browser_manager:
            self.browser_manager.quit()


if __name__ == "__main__":
    print_logo()
    cursor_keep_alive = CursorKeepAlive()
    try:
        cursor_keep_alive.create_account()
    except Exception as e:
        cursor_keep_alive.handle_error(e)
    finally:
        cursor_keep_alive.cleanup()
        input("\n帅哥,程序执行完毕，按回车键退出...")
