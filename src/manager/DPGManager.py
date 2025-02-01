from pathlib import Path
from dearpygui import dearpygui as dpg


class DPGManager:
    """
    DPG管理器

    - registry_assets(): 注册资源
    """

    def __init__(self):
        pass

    def registry_assets(self):
        """
        注册资源

        - 注册字体
        - 注册字体颜色
        """
        # ========== 注册字体 ==========
        font_path = Path(__file__).parent.parent.joinpath("assets/fonts/DreamHanSans-W14.ttc")
        with dpg.font_registry():
            with dpg.font(font_path, 16) as chinese_font:
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Simplified_Common)
                dpg.bind_font(chinese_font)

        # ========== 注册字体颜色  ==========
        # TODO:


dpg_manager = DPGManager()
