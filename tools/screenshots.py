"""Take screenshots of the built site. Run with a Python that has playwright installed:
   python tools/screenshots.py"""
import pathlib, threading, http.server, functools
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 8765), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()
shots = [("index.html", "home.png", 1440, 900, True), ("clubs/newcastle-united.html", "club.png", 1280, 900, True),
         ("index.html", "home-mobile.png", 390, 844, False), ("calculator.html?club=liverpool", "calculator.png", 1280, 900, True)]
with sync_playwright() as p:
    b = p.chromium.launch()
    for path, out, w, h, full in shots:
        pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
        pg.goto(f"http://127.0.0.1:8765/{path}"); pg.wait_for_load_state("networkidle")
        if out == "home.png": pg.click("thead button[data-k='2']")  # demo: sort by cheapest season ticket
        pg.screenshot(path=str(ROOT / "screenshots" / out), full_page=full)
        print("saved", out)
    b.close()
srv.shutdown()
