"""Screenshot a live URL, or a page in the studio by its file path (a folder means its index.html), with a real headless browser.
usage: python tools/shot.py <url-or-path> <out.png> [--width 1200] [--full]
For an image URL, the image itself is saved. A local path needs no server."""
import sys
from playwright.sync_api import sync_playwright
url, out = sys.argv[1], sys.argv[2]
import pathlib
local = False
if not url.startswith(("http://", "https://", "file:")) and pathlib.Path(url).exists():
    local = True
    f = pathlib.Path(url).resolve()
    url = (f / "index.html" if f.is_dir() else f).as_uri()
width = int(sys.argv[sys.argv.index("--width")+1]) if "--width" in sys.argv else 1200
full = "--full" in sys.argv
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": width, "height": 800})
    r = pg.goto(url, wait_until="load", timeout=45000)
    try: pg.wait_for_load_state("networkidle", timeout=8000)
    except Exception: pass
    ct = (r.headers.get("content-type", "") if r else "")
    if ct.startswith("image/") and not local:  # a remote image is saved as it is; a local file is always rendered
        open(out, "wb").write(r.body())
    else:
        pg.screenshot(path=out, full_page=full)
    b.close()
print("saved", out)
