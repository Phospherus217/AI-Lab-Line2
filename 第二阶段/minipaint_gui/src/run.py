from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

from config import OUTPUT_DIR
from server import start_server, stop_server
from browser import start_browser
from actions import click_menu, fill_size, click_ok, activate_tool, export_png, draw_sketch
from verify import check_size, check_not_blank
from trace import Trace
from sketch_data import SKETCH, WEIGHTS

WIDTH, HEIGHT = 1200, 680


def main():
    run_dir = OUTPUT_DIR / f"run_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    run_dir.mkdir(parents=True, exist_ok=True)
    trace = Trace(run_dir)
    server = start_server()
    try:
        with sync_playwright() as p:
            browser, page = start_browser(p)

            # 1) 新建画布
            click_menu(page, "file", "new")
            fill_size(page, WIDTH, HEIGHT)
            click_ok(page)
            trace.add("new_canvas", True, size=[WIDTH, HEIGHT])

            # 2) 按坐标画线
            activate_tool(page, "brush")
            box = page.locator("#canvas_minipaint").bounding_box()
            draw_sketch(page, SKETCH, box, weights=WEIGHTS)
            page.screenshot(path=str(run_dir / "after_draw.png"))
            trace.add("draw_sketch", True,
                      lines=len(SKETCH),
                      points=sum(len(l) for l in SKETCH))

            # 3) 导出
            out_png = run_dir / "result.png"
            export_png(page, "result", out_png)
            trace.add("export", True, path=str(out_png))

            # 4) 校验
            size_res = check_size(out_png, (WIDTH, HEIGHT))
            blank_res = check_not_blank(out_png)
            trace.add("verify_size", **size_res)
            trace.add("verify_not_blank", **blank_res)

            ok = size_res["ok"] and blank_res["ok"]
            trace.save(ok)
            print("成功" if ok else "失败", size_res, blank_res)

            browser.close()
            return ok
    finally:
        stop_server(server)


if __name__ == "__main__":
    main()
