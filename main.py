# python=3.11
# pip install dearpygui loguru keyboard pillow pystray

from src.manager.LoggerManager import logger_manager
from src.manager.LanguageManager import language_maneger

from src.utils.Tray import Tray

if __name__ == "__main__":
    # load manager
    logger = logger_manager.logger
    language_dict = language_maneger.language_dict

    # load utils
    tray = Tray()
    tray.create_tray()

    # shutdown
    logger.info(language_dict.get("logger").get("jpp_unload"))
