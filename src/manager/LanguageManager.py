import json
from pathlib import Path


class LanguageManager:
    """
    语言管理器

    - get_language_dict(): 获取语言配置文件
    """

    def __init__(self):
        self.language = None

        self.get_language_dict()

    def get_language_dict(self, language="zh"):
        """
        获取当前语言词典

        @param
        - language: 选择的语言
        """
        self.language = language

        # 读取对应语言的词典
        language_file_path = Path(__file__).parent.parent.joinpath(f"languages/{self.language}.json")
        with open(language_file_path, "r", encoding="utf-8") as f:
            self.language_dict = json.load(f)


language_maneger = LanguageManager()
