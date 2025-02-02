# JustPressPrScrn

给群友瞎写的截屏工具。

## 适用平台

Windows

## 使用方法

- 安装后启动，按下 `print_screen` 键即可截图。
- 启动后会创建一个托盘，右键启用菜单，`设置`、`退出`都在那里。

## 二次开发

### 开发

- 开发版本 python=3.11
- 第三方库 `pip install dearpygui loguru keyboard pillow pystray`

### 打包

- 编译 `pip install nuitka`，使用参数 `python -m nuitka JustPressPrScrn.py --mode=standalone --include-data-dir=data=data --windows-disable-console`
- 再使用 `Inno Setup` 打包

# 感谢

- 使用了 Python 及其部分第三方库（见上）。
- 使用了 `Inno Setup`。
- 使用了[梦源字体](https://github.com/Pal3love/dream-han-cjk)。