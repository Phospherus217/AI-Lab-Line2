import time

import locator as L


def click_menu(page, menu: str, item: str) -> None:
    page.click(L.MENU[menu])
    page.wait_for_timeout(300)
    page.click(L.MENU_ITEM[item])
    page.wait_for_timeout(500)


def fill_size(page, width: int, height: int) -> None:
    page.fill(L.NEW_WIDTH, str(width))
    page.fill(L.NEW_HEIGHT, str(height))


def click_ok(page) -> None:
    page.click(L.POPUP_OK)
    page.wait_for_timeout(800)


def activate_tool(page, name: str) -> None:
    selector = L.TOOL[name]
    page.evaluate(
        "(sel) => document.querySelector(sel).click()",
        selector,
    )
    page.wait_for_timeout(300)


def drag_on_canvas(page, x1: float, y1: float, x2: float, y2: float) -> None:
    page.mouse.move(x1, y1)
    page.mouse.down()
    page.mouse.move(x2, y2, steps=20)
    page.mouse.up()
    page.wait_for_timeout(600)


def export_png(page, name: str, save_path) -> None:
    click_menu(page, "file", "export")

    page.fill(L.EXPORT_NAME, name)
    page.check(L.EXPORT_TYPE_PNG)

    with page.expect_download(timeout=30_000) as dl_info:
        page.click(L.POPUP_OK)

    download = dl_info.value
    download.save_as(str(save_path))
    page.wait_for_timeout(500)


def draw_sketch(page, lines, box, weights=None, verbose: bool = True) -> None:
    """按归一化坐标（0~1000）画折线。

    lines  ：[[(x,y),...], ...]
    box    ：画布 bounding_box()
    weights：与 lines 对应（2 粗 / 1 中 / 0 细），None 表示全一样
    """
    total = len(lines)
    t0 = time.time()
    last = t0

    for i, line in enumerate(lines):
        pts = [
            (box["x"] + x / 1000 * box["width"],
             box["y"] + y / 1000 * box["height"])
            for x, y in line
        ]
        w = 0 if weights is None else weights[i]
        passes = {2: 3, 1: 2, 0: 1}[w]   # 2→描3遍(粗) 1→2遍(中) 0→1遍(细)

        for k in range(passes):
            off = 0.8 * k      # k=0→0, k=1→0.8, k=2→1.6，每一遍都错开
            moved = [(x + off, y + off) for x, y in pts]
            page.mouse.move(*moved[0])
            page.mouse.down()
            for p in moved[1:]:
                page.mouse.move(*p, steps=1)
            page.mouse.up()

        now = time.time()
        if verbose and (now - last >= 2.0 or i == total - 1):
            done = now - t0
            pct = (i + 1) / total * 100
            eta = done / (i + 1) * (total - i - 1) if i + 1 else 0
            print(f"[{i+1}/{total}] {pct:5.1f}%  已用 {done:5.1f}s  预计剩余 {eta:5.0f}s", flush=True)
            last = now
