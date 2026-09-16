"""Copy every active studio's public/ into docs/<id>/ for GitHub Pages. Run after each session, then commit and push."""
import pathlib, shutil, re
root = pathlib.Path(__file__).resolve().parent.parent
docs = root / "docs"; docs.mkdir(exist_ok=True)
reg = (root / "registry.md").read_text(encoding="utf-8")
ids = [m.group(1) for m in re.finditer(r"^\| (a\d+) \| \.\./studios/\1 \|.*\| active \|", reg, re.M)]
for i in ids:
    src = root.parent / "studios" / i / "public"; dst = docs / i
    if dst.exists(): shutil.rmtree(dst)
    if src.exists(): shutil.copytree(src, dst)
    else: dst.mkdir()
links = "\n".join(f'<li><a href="{i}/">{i}</a></li>' for i in ids)
(docs / "index.html").write_text(f"<!doctype html><meta charset=utf-8><title>studios</title><ul>{links}</ul>", encoding="utf-8")
(docs / ".nojekyll").write_text("")
print("published", ids)
