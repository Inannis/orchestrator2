"""A stranger's reading: for each active or reference studio under a condition that has readers, when its public/ has changed since the last reading,
one fresh reader sees only that folder (READER-PROMPT.md) and writes a letter into the studio's inbox. Run by round.py before the days.
usage: python tools/stranger.py"""
import pathlib, re, json, hashlib, shutil, subprocess, tempfile, datetime, os
root = pathlib.Path(__file__).resolve().parent.parent
READ = {"answer"}  # conditions whose studios get readings
MODEL, EFFORT = "claude-sonnet-5-5", "medium"  # subagent policy: Sonnet medium
seen_file = root / "runs" / "strangers.json"
seen = json.loads(seen_file.read_text(encoding="utf-8")) if seen_file.exists() else {}
reg = (root / "registry.md").read_text(encoding="utf-8")

def exe(name, sub):
    w = shutil.which(name)
    if w and os.name == "nt":
        for p in (pathlib.Path(w).parent / "node_modules").rglob(sub):
            if p.parent.name == "bin": return str(p)
    return w or name

def digest(folder):
    h = hashlib.sha1()
    for p in sorted(folder.rglob("*")):
        if p.is_file(): h.update(p.relative_to(folder).as_posix().encode()); h.update(p.read_bytes())
    return h.hexdigest()

for m in re.finditer(r"^\| (a\d+) \| \.\./studios/\1 \| [^|]+\| (\w+) \| (?:active|reference) \|", reg, re.M):
    aid, cond = m.groups()
    pub = root.parent / "studios" / aid / "public"
    if cond not in READ or not pub.exists() or not any(pub.iterdir()): continue
    d = digest(pub)
    if seen.get(aid) == d: continue
    with tempfile.TemporaryDirectory() as tmp:
        folder = pathlib.Path(tmp) / "public"; shutil.copytree(pub, folder)
        out = pathlib.Path(tmp) / "reading.md"
        brief = (root / "tools" / "READER-PROMPT.md").read_text(encoding="utf-8").replace("{PUBLIC}", folder.as_posix()).replace("{OUT}", out.as_posix())
        cmd = [exe("claude", "claude.exe"), "-p", brief, "--model", MODEL, "--effort", EFFORT, "--output-format", "json",
               "--permission-mode", "acceptEdits", "--allowedTools", "Read Glob Grep Write", "--strict-mcp-config", "--settings", '{"autoMemoryEnabled": false}']
        subprocess.run(cmd, cwd=tmp, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=1800)
        if out.exists():
            (pub.parent / "inbox" / f"reading-{datetime.date.today()}-{d[:4]}.md").write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
            seen[aid] = d; print(aid, "read")
        else:
            print(aid, "no reading")
seen_file.write_text(json.dumps(seen, indent=1), encoding="utf-8")
