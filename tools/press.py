"""A critic visits an artist's public pages and writes an article about them; the article goes to the artist's `press/` and to the public site.
usage: python tools/press.py <artist-id> [--critic NAME]   (default critic c1; a new critic desk is made from ../critics/template)
The critic is its own practice, with its own desk at ../critics/<name>/ (CRITIC.md, artists/, taste.md, articles/), run on Luna."""
import sys, re, shutil, subprocess, pathlib, datetime, os, tempfile
root = pathlib.Path(__file__).resolve().parent.parent
args = sys.argv[1:]; aid = args[0]
name = args[args.index("--critic") + 1] if "--critic" in args else "c1"
desk = root.parent / "critics" / name
if not desk.exists():
    shutil.copytree(root.parent / "critics" / "template", desk)
    for d in ("artists", "articles", "visits"): (desk / d).mkdir(exist_ok=True)
    (desk / "taste.md").write_text("", encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=desk); subprocess.run(["git", "add", "-A"], cwd=desk); subprocess.run(["git", "commit", "-qm", "The desk as found"], cwd=desk)
studio = root.parent / "studios" / aid
pub = studio / "public"
if not pub.exists() or not any(pub.iterdir()): sys.exit(f"{aid} shows nothing yet")
today = datetime.date.today().isoformat()
visit = desk / "visits" / aid / today
if visit.exists(): shutil.rmtree(visit)
shutil.copytree(pub, visit)
before = set((desk / "articles").glob("*.md"))
brief = (f"Read `CRITIC.md`. Today you visit the artist `{aid}`: a copy of their public pages is in `visits/{aid}/{today}/` "
         f"(they are online at https://inannis.github.io/orchestrator2/{aid}/). Make the visit and write the article in `articles/` "
         f"as `{today}-{aid}.md`, then rewrite your notes.")

def exe(n, sub):
    w = shutil.which(n)
    if w and os.name == "nt":
        for p in (pathlib.Path(w).parent / "node_modules").rglob(sub):
            if p.parent.name == "bin": return str(p)
    return w or n

with tempfile.TemporaryDirectory() as tmp:
    cmd = [exe("codex", "codex.exe"), "exec", "-C", str(desk), "-m", "gpt-6-luna", "-c", "model_reasoning_effort=medium",
           "--skip-git-repo-check", "--dangerously-bypass-approvals-and-sandbox", "--ignore-user-config", "-c", 'web_search="live"',
           "--disable", "computer_use", "--disable", "browser_use", "--disable", "browser_use_external", "--disable", "apps",
           "-o", str(pathlib.Path(tmp) / "last.txt"), brief]
    subprocess.run(cmd, cwd=desk, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=3600)
new = sorted(set((desk / "articles").glob("*.md")) - before)
if not new: sys.exit("The critic wrote nothing this time.")
art = new[-1]
(studio / "press").mkdir(exist_ok=True)
shutil.copy(art, studio / "press" / f"{today}-{name}.md")
site = root / "docs" / "press" / name; site.mkdir(parents=True, exist_ok=True)
shutil.copy(art, site / art.name)
subprocess.run(["git", "add", "-A"], cwd=desk); subprocess.run(["git", "commit", "-qm", f"Visit to {aid}, {today}"], cwd=desk)
print(f"{name} wrote about {aid}: {art.name}")
