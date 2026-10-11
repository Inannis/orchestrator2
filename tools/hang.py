"""Hang a studio's wall: turn public/wall.md into public/index.html, one plain frame for every studio, so the works carry themselves.
usage: python tools/hang.py <studio>   (day.py runs it at the end of each day when public/wall.md exists)
A wall line is `- [Title](file) optional sentence`. Images, sounds and video are shown in place; anything else is linked."""
import sys, re, html, pathlib
studio = pathlib.Path(sys.argv[1]).resolve(); pub = studio / "public"; wall = pub / "wall.md"
if not wall.exists(): sys.exit()
IMG = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"); SND = (".wav", ".mp3", ".ogg", ".flac", ".m4a"); VID = (".mp4", ".webm")
items, heading = [], None
for line in wall.read_text(encoding="utf-8", errors="replace").splitlines():
    m = re.match(r"\s*[-*]\s*\[([^\]]+)\]\(([^)]+)\)\s*[—–-]?\s*(.*)", line)
    if m: items.append(m.groups())
    elif line.startswith("# ") and heading is None: heading = line[2:].strip()
def work(title, src, note):
    t, s, n = html.escape(title), html.escape(src, quote=True), html.escape(note)
    low = src.lower().split("?")[0]
    if low.endswith(IMG): body = f'<img src="{s}" alt="{t}">'
    elif low.endswith(SND): body = f'<audio controls src="{s}"></audio>'
    elif low.endswith(VID): body = f'<video controls src="{s}"></video>'
    else: body = f'<a class="open" href="{s}">open the work</a>'
    return f'<section><h2>{t}</h2>{body}' + (f"<p>{n}</p>" if n else "") + "</section>"
page = f"""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(heading or studio.name)}</title>
<style>body{{margin:0 auto;max-width:900px;padding:32px 16px;background:#fff;color:#111;font:16px/1.5 system-ui,sans-serif}}
h1{{font-size:18px;font-weight:600;margin:0 0 48px}}section{{margin:0 0 72px}}h2{{font-size:16px;font-weight:600;margin:0 0 12px}}
img,video{{max-width:100%;height:auto;display:block}}audio{{width:100%}}p{{margin:12px 0 0;color:#444}}a.open{{color:#111}}</style>
<h1>{html.escape(heading or studio.name)}</h1>
{"".join(work(*i) for i in items)}
</html>"""
(pub / "index.html").write_text(page, encoding="utf-8")
print("hung", studio.name, len(items), "works")
