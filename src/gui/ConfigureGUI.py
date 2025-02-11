from pathlib import Path
import subprocess
import tkinter
from tkinter import filedialog
import dearpygui.dearpygui as dpg
import keyboard

from src.manager.ConfigManager import config_manager
from src.manager.LanguageManager import language_maneger
from src.manager.LoggerManager import logger_manager

from src.utils.PrintScreen import print_screen


class ConfigureGUI:

    def __init__(
        self,
    ):
        """
        配置构造函数，同时加载读取的配置信息。
        """
        self.config_manager = config_manager
        self.config = config_manager.config
        self.logger = logger_manager.logger
        self.language_dict = language_maneger.language_dict
        self.print_screen = print_screen

    def create_windows(self, window_id: any = "DefaultWindowId") -> any:
        """
        构建窗体

        Args:
            window_id (any): 窗体的ID

        Returns:
            any: 窗体的ID
        """
        self.window_id = window_id

        with dpg.window(tag=self.window_id):
            # 欢迎
            with dpg.group():
                msg = self.language_dict.get("config").get("welcome")
                dpg.add_text(default_value=msg.get("msg_welcome"))

            dpg.add_separator()

            # 保存路径设置
            with dpg.group():
                msg = self.language_dict.get("config").get("path_to_save")
                dpg.add_text(default_value=msg.get("title"))

                # 方法1 手动写入路径
                dpg.add_text(default_value=msg.get("msg_method_1"))
                self.folder_path_input = dpg.add_input_text(
                    tag="folder_path_input",
                    label=msg.get("input_hint"),
                    default_value=self.config.get("config").get("path_to_save"),
                    callback=self.folder_path_input_callback,
                )
                # 监听更新事件，当 tag = "folder_path_input" 失去焦点（用户编辑完毕）后保存输入内容
                with dpg.item_handler_registry(tag="folder_path_save_handler"):
                    dpg.add_item_deactivated_after_edit_handler(callback=self.folder_path_save_callback)
                dpg.bind_item_handler_registry("folder_path_input", "folder_path_save_handler")

                self.folder_path_input_checker = dpg.add_text(
                    default_value="",
                )

                # 方法2 选择文件夹
                dpg.add_text(default_value=msg.get("msg_method_2"))
                self.folder_path_button = dpg.add_button(
                    tag="folder_path_button",
                    label=msg.get("button_hint"),
                    callback=self.folder_path_button_callback,
                )
                dpg.add_text(default_value="")

                # 打开本地图片文件夹
                self.open_folder_button = dpg.add_button(
                    tag="open_folder_button",
                    label=msg.get("button_open_folder"),
                    callback=self.open_folder_button_callback,
                )

            dpg.add_separator()

            # 快捷键设置
            with dpg.group():
                msg = self.language_dict.get("config").get("hotkey")
                dpg.add_text(default_value=msg.get("title"))
                self.msg_current_hotkey = dpg.add_text(default_value=str(msg.get("msg_current_hotkey") + self.config.get("config").get("hotkey")))
                self.hotkey_button = dpg.add_button(
                    label=msg.get("button_hint"),
                    tag="hotkey_button",
                    callback=self.hotkey_button_callback,
                )
                self.hotkey_button_checker = dpg.add_text(
                    default_value="",
                )
            """
            dpg.add_separator()
            
            # 保存成功提示
            with dpg.group():
                msg = self.language_dict.get("config").get("feedback_when_saved")
                dpg.add_text(default_value=msg.get("title"))
                dpg.add_checkbox(label=msg.get("checkbox_hint"), default_value=True)
            """

        return self.window_id

    def folder_path_input_callback(self, sender):
        """
        folder_path_input 的修改回调

        在输入的时候检测路径是否存在，如果路径不存在会提示“将自动创建”
        """
        path = Path(dpg.get_value(sender))
        dpg.set_value(self.folder_path_input_checker, self.language_dict.get("config").get("path_to_save").get("input_error") if not path.exists() else "")

    def folder_path_save_callback(self):
        """
        folder_path_input 的失去焦点回调（触发保存）
        """
        new_path = dpg.get_value(self.folder_path_input)
        self.config.get("config")["path_to_save"] = new_path
        self.config_manager.write_config()

    def folder_path_button_callback(self):
        """
        folder_path_button 的触发回调

        调用系统的文件夹选择
        """
        root = tkinter.Tk()
        root.withdraw()
        folder_path = filedialog.askdirectory(title=self.language_dict.get("config").get("path_to_save").get("button_hint"))
        dpg.set_value(self.folder_path_input, folder_path)

        self.config.get("config")["path_to_save"] = folder_path
        self.folder_path_save_callback()

    def open_folder_button_callback(self):
        """
        open_folder_button 的触发回调

        打开本地文件夹
        """
        path = Path(self.config.get("config").get("path_to_save"))
        if not path.exists():
            self.logger.warning(self.language_dict.get("openfolder_does_not_exist"))
        subprocess.run(["explorer", path])

    def hotkey_button_callback(self):
        """
        hotkey_button 的触发回调
        """
        self.start_keyboard_listener()

    def start_keyboard_listener(self):
        self.pressed_keys = set()  # 当前按下的键
        self.latest_shortcut = ""  # 最新的组合键
        self.is_listening = False  # 标记监听状态
        self.listener_hook = None  # 当前监听器

        # 启用监听
        self.listener_hook = keyboard.hook(self.on_key_event)
        self.is_listening = True
        dpg.set_value(self.hotkey_button_checker, self.language_dict.get("config").get("hotkey").get("msg_new_hotkey_wait"))
        self.logger.debug(self.language_dict.get("logger").get("hotkey_record"))

    def on_key_event(self, event):
        if event.event_type == keyboard.KEY_DOWN:
            self.pressed_keys.add(event.name)
            self.latest_shortcut = "+".join(self.pressed_keys)
            dpg.set_value(self.hotkey_button_checker, str(self.language_dict.get("config").get("hotkey").get("msg_new_hotkey") + self.latest_shortcut))
        elif event.event_type == keyboard.KEY_UP:
            if event.name in self.pressed_keys:
                self.pressed_keys.remove(event.name)
            if not self.pressed_keys:
                self.stop_keyboard_listener()

    def stop_keyboard_listener(self):
        if self.is_listening:
            # 解除键盘监听
            keyboard.unhook(self.listener_hook)
            self.listener_hook = None
            self.is_listening = False
            # 更新 dpg 显示
            dpg.set_value(self.msg_current_hotkey, str(self.language_dict.get("config").get("hotkey").get("msg_current_hotkey") + self.latest_shortcut))
            dpg.set_value(self.hotkey_button_checker, str(self.language_dict.get("config").get("hotkey").get("msg_new_hotkey_saved") + self.latest_shortcut))
            # 更细配置数据
            self.config.get("config")["hotkey"] = self.latest_shortcut
            self.config_manager.write_config()
            # 热重载
            self.print_screen.hotkey_reregister(self.latest_shortcut)
            # 快捷键更新完毕
            self.logger.debug(self.language_dict.get("logger").get("hotkey_record_end"))
