"""Copy every active, reference or paused studio's public/ into docs/<id>/ for GitHub Pages. Run after each session, then commit and push."""
import pathlib, shutil, re
root = pathlib.Path(__file__).resolve().parent.parent
docs = root / "docs"; docs.mkdir(exist_ok=True)
reg = (root / "registry.md").read_text(encoding="utf-8")
ids = [m.group(1) for m in re.finditer(r"^\| (a\d+) \| \.\./studios/\1 \|.*\| (?:active|paused|reference)[^|]*\|", reg, re.M)]
for i in ids:
    src = root.parent / "studios" / i / "public"; dst = docs / i
    if dst.exists(): shutil.rmtree(dst)
    if src.exists(): shutil.copytree(src, dst)
    else: dst.mkdir()
    if not (dst / "index.html").exists():
        files = sorted(f.relative_to(dst).as_posix() for f in dst.rglob("*") if f.is_file())
        items = "\n".join(f'<li><a href="{f}">{f}</a></li>' for f in files) or "<li>(nothing public yet)</li>"
        (dst / "index.html").write_text(f"<!doctype html><meta charset=utf-8><title>{i}</title><p><small>Generated listing. The studio has not made a front page.</small></p><ul>{items}</ul>", encoding="utf-8")
links = "\n".join(f'<li><a href="{i}/">{i}</a></li>' for i in ids)
(docs / "index.html").write_text(f"<!doctype html><meta charset=utf-8><title>studios</title><ul>{links}</ul>", encoding="utf-8")
(docs / ".nojekyll").write_text("")
# never publish a credential: the artists inherit the environment, so check every published file for the secret values
import os
secrets = [v for k, v in os.environ.items() if k.startswith("CLOUDFLARE_") and len(v) >= 16]
for f in docs.rglob("*"):
    if f.is_file() and secrets:
        data = f.read_bytes()
        hit = [s for s in secrets if s.encode() in data]
        if hit:
            shutil.rmtree(f.parents[len(f.relative_to(docs).parts) - 2]) if len(f.relative_to(docs).parts) > 1 else f.unlink()
            raise SystemExit(f"STOPPED: a credential appears in {f.relative_to(docs)}; that studio's docs folder was removed. Do not commit.")
print("published", ids)
