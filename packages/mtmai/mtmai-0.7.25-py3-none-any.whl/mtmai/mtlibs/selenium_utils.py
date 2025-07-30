"""
项目参考:
    https://github.com/SeleniumHQ/docker-selenium
"""

import atexit
import os
import subprocess
import time
from pathlib import Path

import selenium
from loguru import logger
from selenium.webdriver.chrome.options import Options

from mtmai.core.config import settings
from mtmai.mtlibs.httpUtils import download_file
from mtmai.mtlibs.mtutils import is_in_gitpod

selenium_server_jar_bin = str(
    Path(settings.storage_dir).joinpath("seleniumselenium-server.jar")
)
selenium_version = "4.24.0"
selenium_server_port = 4444


async def install_selenium_server():
    if not Path(selenium_server_jar_bin).exists():
        jar_url = f"https://github.com/SeleniumHQ/selenium/releases/download/selenium-{selenium_version}/selenium-server-{selenium_version}.jar"
        await download_file(jar_url, selenium_server_jar_bin)


async def install_selenium():
    try:
        # Install Selenium and its dependencies
        subprocess.run(["pip", "install", "selenium", "webdriver_manager"], check=True)

        # Create necessary directories
        directories = [
            "/opt/selenium",
            "/opt/selenium/assets",
            "/opt/selenium/secrets",
            "/var/run/supervisor",
            "/var/log/supervisor",
            os.environ.get("SEL_DOWNLOAD_DIR", "/tmp/selenium"),
            f"{os.environ['HOME']}/.mozilla",
            f"{os.environ['HOME']}/.vnc",
            f"{os.environ['HOME']}/.pki/nssdb",
        ]
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)

        # Initialize NSSDB with an empty password
        subprocess.run(
            [
                "certutil",
                "-d",
                f"sql:{os.environ['HOME']}/.pki/nssdb",
                "-N",
                "--empty-password",
            ],
            check=True,
        )

        # Create config file
        Path("/opt/selenium/config.toml").touch()

        # Set permissions
        sel_user = os.environ.get("SEL_USER", "seluser")
        sel_group = os.environ.get("SEL_GROUP", "seluser")
        subprocess.run(
            [
                "chown",
                "-R",
                f"{sel_user}:{sel_group}",
                "/opt/selenium",
                "/var/run/supervisor",
                "/var/log/supervisor",
                "/etc/passwd",
                os.environ["HOME"],
            ],
            check=True,
        )
        subprocess.run(
            [
                "chmod",
                "-R",
                "775",
                "/opt/selenium",
                "/var/run/supervisor",
                "/var/log/supervisor",
                "/etc/passwd",
                os.environ["HOME"],
            ],
            check=True,
        )

        # Download Selenium server
        authors = os.environ.get("AUTHORS", "SeleniumHQ")
        release = os.environ.get("RELEASE", "4.10.0")
        version = os.environ.get("VERSION", "4.10.0")
        await download_file(
            f"https://github.com/{authors}/selenium/releases/download/{release}/selenium-server-{version}.jar",
            "/opt/selenium/selenium-server.jar",
        )

        # Set group permissions
        subprocess.run(
            [
                "chgrp",
                "-R",
                "0",
                "/opt/selenium",
                os.environ["HOME"],
                "/opt/selenium/assets",
                "/var/run/supervisor",
                "/var/log/supervisor",
            ],
            check=True,
        )
        subprocess.run(
            [
                "chmod",
                "-R",
                "g=u",
                "/opt/selenium",
                os.environ["HOME"],
                "/opt/selenium/assets",
                "/var/run/supervisor",
                "/var/log/supervisor",
            ],
            check=True,
        )

        # Set ACLs
        for path in [
            "/opt",
            "/opt/selenium",
            os.environ["HOME"],
            "/opt/selenium/assets",
            "/var/run/supervisor",
            "/var/log/supervisor",
        ]:
            subprocess.run(["setfacl", "-Rm", f"u:{sel_user}:rwx", path], check=True)
            subprocess.run(["setfacl", "-Rm", f"g:{sel_group}:rwx", path], check=True)

        logger.info("Selenium and necessary components installed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"An error occurred during installation: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")


def is_desktop_environment():
    # Check for common desktop environment variables
    desktop_vars = [
        "XDG_CURRENT_DESKTOP",
        "GNOME_DESKTOP_SESSION_ID",
        "KDE_FULL_SESSION",
        "DESKTOP_SESSION",
    ]
    return any(var in os.environ for var in desktop_vars)


def is_x11_running():
    try:
        # Check if X11 is running
        subprocess.run(
            ["xset", "q"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def is_in_display():
    """是否处于图形界面环境中"""
    return is_desktop_environment() or is_x11_running()


async def start_selenium_server():
    logger.info("Starting Selenium server ...")
    logger.info("settings.storage_dir: %s", settings.storage_dir)
    logger.info("selenium_server_jar_bin: %s", selenium_server_jar_bin)
    logger.info("selenium_version: %s", selenium_version)
    logger.info("selenium_server_port: %s", selenium_server_port)
    logger.info("is_in_display: %s", is_in_display())

    await install_selenium_server()
    if not is_in_display():
        logger.info("当前非图形界面，通过 $DISPLAY 环境变量指定图形界面")
        if is_in_gitpod():
            """特定环境下自动配置"""
            os.environ["DISPLAY"] = ":1"

    extra_envs = {
        # "DISPLAY": ":1",
        # "JAVA_OPTS": "-Dwebdriver.chrome.whitelistedIps=",
        # "SE_NODE_MAX_SESSIONS": "8",
        # "SE_NODE_OVERRIDE_MAX_SESSIONS": "true",
        # "SE_NODE_SESSION_TIMEOUT": "300",
        # "SE_OPTS": "--log-level INFO"
    }

    selenium_command = [
        "java",
        "-jar",
        selenium_server_jar_bin,
        "standalone",
        "--selenium-manager",
        "true",
    ]
    env = os.environ.copy()
    env.update(extra_envs)
    selenium_process = subprocess.Popen(
        selenium_command,
        # env=env
    )

    atexit.register(lambda: selenium_process.terminate())

    # time.sleep(7)
    # logger.info(
    #     f"🚀 Selenium server started successfully!, port : {selenium_server_port}"
    # )

    # Monitor the Selenium server process
    while True:
        if selenium_process.poll() is not None:
            logger.error("Selenium server process has terminated unexpectedly.")
            break
        time.sleep(1)


def test_selenium():
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait

    driver = start_selenium_server()
    if driver:
        try:
            driver.get("https://www.bing.com")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            logger.info("Successfully accessed Bing.com")
            return True
        except Exception as e:
            logger.error(f"Failed to access Bing.com: {e}")
            return False
        finally:
            driver.quit()
    else:
        logger.error("Failed to start Selenium")
        return False


def get_chrome_path():
    # 方法1: 使用 find 命令查找
    try:
        result = subprocess.run(
            [
                "find",
                "/home/gitpod/.cache/ms-playwright",
                "-name",
                "chrome",
                "-type",
                "f",
                "-executable",
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0 and result.stdout.strip():
            paths = result.stdout.strip().split("\n")
            # 优先选择 chrome-linux 目录下的 chrome
            for path in paths:
                if "chrome-linux" in path:
                    return path
            # 如果没有找到 chrome-linux 目录下的，返回第一个
            if paths:
                return paths[0]
    except Exception:
        pass

    # 方法2: 根据日志中的路径模式直接构建路径
    try:
        home_dir = str(Path.home())
        playwright_dir = os.path.join(home_dir, ".cache", "ms-playwright")

        if not os.path.exists(playwright_dir):
            return None

        # 查找最新版本的 Chromium
        latest_version = None
        latest_version_num = 0

        for entry in os.listdir(playwright_dir):
            if entry.startswith("chromium-"):
                try:
                    version_num = int(entry.replace("chromium-", ""))
                    if version_num > latest_version_num:
                        latest_version_num = version_num
                        latest_version = entry
                except ValueError:
                    continue

        if latest_version:
            chrome_path = os.path.join(
                playwright_dir, latest_version, "chrome-linux", "chrome"
            )
            if os.path.exists(chrome_path):
                return chrome_path

    except Exception:
        pass

    return None


driver = None


def get_selenium_driver():
    os.environ["DISPLAY"] = ":1"

    global driver
    if driver is None:
        chrome_dir = get_chrome_path()
        if not chrome_dir:
            raise ValueError("cant find chrome dir")
        options = Options()
        options.add_argument("--window-size=1920x1080")
        options.add_argument("--verbose")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        # options.binary_location = chrome_dir
        options.binary_location = chrome_dir

        driver = selenium.webdriver.Chrome(options=options)
    return driver
