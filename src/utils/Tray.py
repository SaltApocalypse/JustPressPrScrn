from pathlib import Path
from PIL import Image
import pystray
import threading

from src.gui.MainGUI import MainGUI
from src.manager.LanguageManager import language_maneger
from src.manager.LoggerManager import logger_manager
from src.utils.PrintScreen import print_screen


class Tray:
    def __init__(self):
        """
        Windows 托盘

        此外，Tray 类实例将会作为程序的存活标志：`self.is_running`
        """
        self.is_running = True
        self.language_dict = language_maneger.language_dict
        self.logger = logger_manager.logger
        self.print_screen = print_screen
        self.maingui_thread = None

        self.logger.debug(self.language_dict.get("logger").get("tray_loaded"))

    def create_tray(self):
        """
        创建系统托盘图标
        """
        icon_path = Path(__file__).parent.parent.parent.joinpath("data/assets/icons/icon.png")
        icon_image = Image.open(icon_path)

        # 创建托盘菜单项
        msg = self.language_dict.get("tray").get("menu")
        menu = (
            pystray.MenuItem(msg.get("print_screen"), self.print_screen.print_screen_and_save),
            pystray.MenuItem(msg.get("config"), self.start_gui),
            pystray.MenuItem(msg.get("exit"), self.stop),
        )

        self.logger.info(self.language_dict.get("logger").get("jpp_loaded"))

        # 设置 tray
        self.icon = pystray.Icon(self.language_dict.get("title").get("tray"), icon_image, self.language_dict["title"].get("tray"), menu)
        # 设置其双击事件
        # TODO: 设置其双击事件
        # self.icon.on_double_click = self.start_gui

        self.icon.run()

    def start_gui(self):
        """
        创建一个专门用于 MainGUi 的线程并启用设置界面。
        """
        # 只要当前不存在，就可以创建（初次创建 或者 上一个 MainGUI 线程已结束）
        if self.maingui_thread is None or not self.maingui_thread.is_alive():

            def gui_thread():
                self.main_gui = MainGUI()
                self.main_gui.start_dpg()

            self.maingui_thread = threading.Thread(target=gui_thread, daemon=True)
            self.maingui_thread.start()

        else:
            self.logger.warning(self.language_dict.get("logger").get("maingui_alive"))

    def stop(self):
        self.logger.debug(self.language_dict.get("logger").get("jpp_exit"))

        # 注销 print_screen
        self.print_screen.hotkey_unregister()
        del self.print_screen

        # 注销 tray
        self.is_running = False
        self.icon.stop()
        self.logger.debug(self.language_dict.get("logger").get("tray_unload"))


# tray = Tray()
