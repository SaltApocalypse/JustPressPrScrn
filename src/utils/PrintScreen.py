from datetime import datetime
import keyboard
from pathlib import Path
from PIL import ImageGrab

from src.manager.ConfigManager import config_manager
from src.manager.LoggerManager import logger_manager
from src.manager.LanguageManager import language_maneger


class PrintScreen:
    def __init__(self):
        self.is_running = True
        self.config = config_manager.config
        self.logger = logger_manager.logger
        self.language_dict = language_maneger.language_dict

        self.hotkey = self.config.get("config").get("hotkey")
        self.hotkey_register()

    def print_screen_and_save(self):
        """
        截屏并保存，如果保存目录不存在则自动创建。
        """
        try:
            # 截图保存路径，如果不存在则尝试创建
            pictures_dir = Path(self.config.get("config").get("path_to_save"))

            if not Path.exists(pictures_dir):
                self.logger.info(self.language_dict.get("logger").get("pathtosave_does_not_exist"))
                try:
                    Path.mkdir(pictures_dir, parents=True, exist_ok=True)
                    self.logger.success(self.language_dict.get("logger").get("pathtosave_success_to_create"))
                # except PermissionError as e:
                except:
                    self.logger.error(self.language_dict.get("logger").get("pathtosave_failed"))

            # 添加时间戳，截图并保存
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = Path.joinpath(pictures_dir, f"screenshot_{timestamp}.png")

            screenshot = ImageGrab.grab()
            screenshot.save(file_path, "PNG")

            self.logger.info(self.language_dict.get("logger").get("print_screen_success"))

        except e:
            self.logger.error(self.language_dict.get("logger").get("print_screen_failed"))
            self.logger.error(e)

    def hotkey_register(self, hotkey: str = None):
        """
        注册快捷键

        @param
        - hotkey: 注册的快捷键
        """
        if hotkey is not None:
            self.hotkey = hotkey

        if self.hotkey is None:
            self.logger.error(self.language_dict.get("logger").get("hotkey_error"))
            return

        # 添加快捷键
        keyboard.add_hotkey(self.hotkey, self.print_screen_and_save, suppress=True)
        self.logger.debug(self.language_dict.get("logger").get("print_screen_loaded") + self.hotkey)

    def hotkey_unregister(self):
        if self.is_running:
            keyboard.remove_hotkey(self.hotkey)
            self.is_running = False
            self.logger.debug(self.language_dict.get("logger").get("print_screen_unload"))

    def hotkey_reregister(self, hotkey=None):
        """
        重新注册快捷键（先注销后注册）

        @param
        - hotkey: 注册的快捷键
        """
        self.hotkey_unregister()
        self.hotkey_register(hotkey)


print_screen = PrintScreen()
