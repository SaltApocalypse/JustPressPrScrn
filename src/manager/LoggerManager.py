import sys
from datetime import datetime
from pathlib import Path
import traceback
from loguru import logger

# NOTE: 避免嵌套引用，并提供那种多次调用的方法


class LoggerManager:
    """
    日志管理器

    初始化时创建日志管理器 logger 并接管了未处理的异常追踪。
    """

    def __init__(self):
        self.log_path = Path(__file__).parent.parent.joinpath("logs")
        self.__init_log_folder(self.log_path)  # 如果不存在目标文件夹则创建
        self.log_name = f"log_{datetime.now():%y-%m-%d}.log"

        # logger 配置
        self.logger = logger
        self.logger.add(
            self.log_path.joinpath(self.log_name),
            format="{time:YY-MM-DD HH:mm:ss} {level} {message}",
            rotation="00:00",
            retention="7 days",
            compression="zip",
        )
        # 日志输出等级
        self.logger.add(sys.stdout, format="{time:YYMMDD HH:mm:ss} {level} {message}")  # DEBUG
        # self.logger.add(sys.stdout, level="INFO", format="{time:YYMMDD HH:mm:ss} {level} {message}") # Release

        # 针对未处理的异常捕获
        sys.excepthook = self.__exception_handler

    def __init_log_folder(self, folder):
        """
        检查是否存在 logs 文件夹，如果不存在则创建
        """
        folder = Path(folder)
        if not folder.exists():
            Path.mkdir(folder, parents=True, exist_ok=True)

    def __exception_handler(self, exc_type, exc_value, exc_tb):
        """
        捕获未处理的异常
        """
        if issubclass(exc_type, KeyboardInterrupt):
            # 如果是按下 Ctrl+C 的中断，保持程序正常退出
            sys.__excepthook__(exc_type, exc_value, exc_tb)
        else:
            logger.error("".join(traceback.format_exception(exc_type, exc_value, exc_tb)))


logger_manager = LoggerManager()
