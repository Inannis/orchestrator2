"""Screenshot a live URL (or save an image URL) with a real headless browser.
usage: python tools/shot.py <url> <out.png> [--width 1200] [--full]
For an image URL, the image itself is saved."""
import sys
from playwright.sync_api import sync_playwright
url, out = sys.argv[1], sys.argv[2]
width = int(sys.argv[sys.argv.index("--width")+1]) if "--width" in sys.argv else 1200
full = "--full" in sys.argv
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": width, "height": 800})
    r = pg.goto(url, wait_until="load", timeout=45000)
    try: pg.wait_for_load_state("networkidle", timeout=8000)
    except Exception: pass
    ct = (r.headers.get("content-type", "") if r else "")
    if ct.startswith("image/"):
        open(out, "wb").write(r.body())
    else:
        pg.screenshot(path=out, full_page=full)
    b.close()
print("saved", out)
