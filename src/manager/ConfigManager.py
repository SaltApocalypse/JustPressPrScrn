from pathlib import Path
import json
import locale


class ConfigManager:
    """
    配置管理器

    初始化时进行一次读取。

    - read_config(): 读取配置文件
    - write_config(): 写入配置文件（当前状态）
    """

    def __init__(self):
        self.config = None
        self.config_file_path = Path(__file__).parent.parent.joinpath("config.json")
        self.read_config()

    def read_config(self):
        """
        读取配置文件

        首次使用或配置文件丢失时，初始化配置文件
        """
        if not Path(self.config_file_path).exists():
            self.__init_default_config()

        with open(self.config_file_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)

    def write_config(self):
        """
        写入配置文件
        """
        with open(self.config_file_path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)

    def __init_default_config(self):
        """
        初始化设置为默认设置
        """
        self.config = {}

        self.config["general"] = {}
        self.config["general"]["language"] = "zh" if "Chinese" == locale.getlocale()[0] else "en"

        self.config["config"] = {}
        self.config["config"]["path_to_save"] = str(Path.home().joinpath("Pictures").joinpath("JustPressPrScrn"))
        self.config["config"]["hotkey"] = "print_screen" 

        self.write_config()


config_manager = ConfigManager()
