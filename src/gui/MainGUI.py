import dearpygui.dearpygui as dpg

from src.manager.ConfigManager import config_manager
from src.manager.DPGManager import dpg_manager
from src.manager.LanguageManager import language_maneger
from src.manager.LoggerManager import logger_manager

from src.gui.ConfigureGUI import ConfigureGUI


class MainGUI:
    def __init__(self):

        self.config = config_manager.config
        self.dpg_manager = dpg_manager
        self.language_dict = language_maneger.language_dict
        self.logger = logger_manager.logger

        # ========== manager 初始化 ==========
        self.is_running = False
        self.config_gui = ConfigureGUI()

        self.logger.debug(self.language_dict.get("logger").get("maingui_loaded"))

    def start_dpg(self):
        if not self.is_running:
            # ========== dpg 创建上下文 ==========
            dpg.create_context()
            # ========== 载入配置 ==========
            self.dpg_manager.registry_assets()  # 载入资源
            # ========== 创建窗体 ==========
            self.config_gui_id = self.config_gui.create_windows(self.language_dict["title"].get("main_window"))

            # ========== dpg 初始化 ==========
            dpg.create_viewport(title=f"{self.config_gui_id}", width=600, height=400)
            dpg.setup_dearpygui()
            dpg.show_viewport()
            dpg.set_primary_window(f"{self.config_gui_id}", True)

            # ========== dpg 运行中 ==========
            self.is_running = True
            dpg.start_dearpygui()

            # ========== dpg 运行结束 ==========
            dpg.destroy_context()
            self.is_running = False
            self.logger.debug(self.language_dict.get("logger").get("maingui_unload"))
