# -*- coding: utf-8 -*-
"""miniPaint 的选择器。

为什么要单独放：
· 页面改版、换语言时，只改这里
· 写测试的人一眼能看到“点的是什么”

这些 id 是用 Playwright 打开页面后 dump 出来的：
  page.evaluate("Array.from(document.querySelectorAll('[id]')).map(e=>e.id)")
"""

# 一级菜单（File / Edit / View / Image / Layer / Effects / Tools / Help）
MENU = {
    "file":   "#main_menu_0_0",
    "edit":   "#main_menu_0_1",
    "view":   "#main_menu_0_2",
    "image":  "#main_menu_0_3",
    "layer":  "#main_menu_0_4",
    "effects":"#main_menu_0_5",
    "tools":  "#main_menu_0_6",
    "help":   "#main_menu_0_7",
}

# 二级菜单项（点开 File 之后才可见）
MENU_ITEM = {
    "new":    "#main_menu_1_0",
    "open":   "#main_menu_1_2",
    "export": "#main_menu_1_5",
}

# 弹出对话框
POPUP = ".popup"
POPUP_OK = ".popup button[data-id=popup_ok]"
POPUP_CANCEL = ".popup button[data-id=popup_cancel]"
POPUP_CLOSE = ".popup button[data-id=popup_close]"

# New 对话框里的输入框
NEW_WIDTH = "#pop_data_width"
NEW_HEIGHT = "#pop_data_height"

# Export 对话框
EXPORT_NAME = "#pop_data_name"
EXPORT_TYPE_PNG = "#pop_data_type_poptmp0"

# 工具（左侧）
TOOL = {
    "brush": "#brush",
    "pencil": "#pencil",
    "rectangle": "#rectangle",   # 默认折叠，需要 JS 激活
    "text": "#text",
    "fill": "#fill",
    "crop": "#crop",
}

# 画布
CANVAS = "#canvas_minipaint"

# 右侧信息面板（读状态用）
INFO_SIZE_TEXT = "#info_base"     # 里面包含 "Size: 800 x 600 px"