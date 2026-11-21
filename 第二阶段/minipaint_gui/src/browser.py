from config import BASE_URL, TIMEOUT_MS, VIEWPORT

def start_browser(p):
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport=VIEWPORT)
    page.goto(BASE_URL, timeout=TIMEOUT_MS)

    page.wait_for_selector("#canvas_minipaint", state="visible", timeout=TIMEOUT_MS)
    page.wait_for_timeout(1500)  # 再给编辑器一点初始化时间

    return browser, page