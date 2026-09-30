"""Run one artist's working day headless, end to end: first turn, one encounter draw, K private continuations, a ledger line.
usage: python tools/day.py <id> [--k K] [--model M] [--effort E] [--shape S] [--resume SESSION_ID] [--studio PATH] [--n N]
Shapes (how the day is kept going; see template/conditions.md): "plain" says only that the day is not over;
"return" also hands back one of the artist's own earlier files, drawn at random.
Needs the claude CLI logged in (`claude auth login` or CLAUDE_CODE_OAUTH_TOKEN). Handbacks go to runs/days/, not to anyone's context."""
import sys, json, re, random, subprocess, pathlib, datetime, time, shutil, os
root = pathlib.Path(__file__).resolve().parent.parent
args = sys.argv[1:]; aid = args[0]
def opt(name, default=None):
    return args[args.index(name) + 1] if name in args else default
reg = (root / "registry.md").read_text(encoding="utf-8")
row = re.search(rf"^\| {aid} \| ([^|]+) \| ([\w.-]+) \| (\w+) \| [^|]+ \| (\d+) \|(?: (\w+) \|)?", reg, re.M)
studio = pathlib.Path(opt("--studio") or (root / row.group(1).strip())).resolve()
model = opt("--model") or (row.group(2) if row else "claude-sonnet-5")
effort = opt("--effort") or (row.group(5) if row and row.group(5) else "medium")
n = int(opt("--n") or ((int(row.group(4)) + (0 if "--resume" in args else 1)) if row else 1))
k = int(opt("--k") or random.randint(1, 6))
resume = opt("--resume")  # continue an interrupted day: --resume <session id> --k <continuations left>
cond = row.group(3) if row else None
crow = re.search(rf"^\| {cond} \| \w+ \| \w+ \| (\w+) \|", (root / "template" / "conditions.md").read_text(encoding="utf-8"), re.M) if cond else None
shape = opt("--shape") or (crow.group(1) if crow else "plain")
today = datetime.date.today().isoformat()
prompt = (root / "template" / "SESSION-PROMPT.md").read_text(encoding="utf-8").replace("{STUDIO}", studio.as_posix()).replace("{DATE}", today).replace("{N}", str(n))
def own_file():
    """One thing the artist made, at random: an image, sound or text piece, never its memory, logs, notes or the orchestrator's files."""
    skip_dirs = {"reference", "inbox", "requests", ".git", "log", "logs", "journal", "memory", "notes", "between", "__pycache__", "sketches"}
    skip_names = {"CHARTER.md", "NOW.md", "STATE.md", "MEMORY.md", "STATUS.md", "journal.md", "notes.md", "threads.md", "README.md", "index.html", ".gitignore"}
    exts = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".wav", ".txt", ".md", ".html")
    fs = []
    for p in studio.rglob("*"):
        rel = p.relative_to(studio)
        if not p.is_file() or p.name in skip_names or not p.name.lower().endswith(exts): continue
        if any(part in skip_dirs for part in rel.parts[:-1]): continue
        fs.append(rel.as_posix())
    if not fs and (studio / "public" / "index.html").exists(): fs = ["public/index.html"]
    return random.choice(fs) if fs else None

def more(first_arrival):
    base = "The day is not over." + (" Something arrived in inbox/." if first_arrival else "")
    if shape == "return":
        f = own_file()
        if f: base += f" From your studio, at random: `{f}`."
    return base

TOOLS = "Bash Read Write Edit Glob Grep WebFetch WebSearch"
out = root / "runs" / "days"; out.mkdir(parents=True, exist_ok=True)
log = out / (f"{aid}-{n:03d}.md" if not opt("--resume") else f"{aid}-{n:03d}-resumed.md")

def claude_exe():
    """The native CLI binary; on Windows `claude` is a .cmd wrapper that subprocess cannot start and cmd.exe would mangle."""
    w = shutil.which("claude")
    if w and w.lower().endswith((".cmd", ".ps1")) or (w and os.name == "nt"):
        exe = pathlib.Path(w).parent / "node_modules" / "@anthropic-ai" / "claude-code" / "bin" / "claude.exe"
        if exe.exists(): return str(exe)
    return w or "claude"
CLAUDE = claude_exe()

def turn(text, sid=None):
    cmd = [CLAUDE, "-p", text, "--model", model, "--output-format", "json", "--effort", effort, "--permission-mode", "acceptEdits",
           "--allowedTools", TOOLS, "--settings", '{"autoMemoryEnabled": false}']
    if sid: cmd += ["--resume", sid]
    r = subprocess.run(cmd, cwd=studio, capture_output=True, text=True, encoding="utf-8", timeout=5400)
    try: return json.loads(r.stdout)
    except json.JSONDecodeError: return {"is_error": True, "result": (r.stdout + r.stderr)[-2000:]}

t0 = time.time(); turns = 0; cost = 0.0; tok = 0; enc = "none"; err = None
msgs = [prompt] if not resume else [more(False)]
sid = resume
with log.open("w", encoding="utf-8") as f:
    f.write(f"# {aid} session {n} · {today} · {model} · effort {effort} · K={k}\n\n")
    for i in range(k + 1 if not resume else k):
        d = turn(msgs[-1], sid)
        sid = d.get("session_id", sid); cost += d.get("total_cost_usd") or 0
        u = d.get("usage") or {}; tok += sum(u.get(x, 0) or 0 for x in ["input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"])
        sent = "(session prompt)" if (i == 0 and not resume) else msgs[-1]
        f.write(f"## turn {i + 1}\n\n> {sent}\n\n{d.get('result', '')}\n\n"); f.flush()
        if d.get("is_error"):
            err = str(d.get("result", ""))[:300]; break
        turns += 1
        if i == k: break
        if i == 0 and not resume:
            e = subprocess.run([sys.executable, str(root / "tools" / "encounter.py"), str(studio), "--p", "0.5"], capture_output=True, text=True).stdout
            m = re.search(r"delivered \S+ \S+ (\w+)", e)
            enc = m.group(1) if m else "none"
            msgs.append(more(bool(m)))
        else:
            msgs.append(more(False))

line = {"run": f"{aid}-{n:03d}", "artist": aid, "n": n, "date": today, "model": model, "effort": effort, "condition": cond, "shape": shape,
        "minutes": round((time.time() - t0) / 60), "turns": turns, "k": k, "encounter": enc, "tokens": tok, "cost_usd": round(cost, 2),
        "error": err, "session_id": sid, "resumed": bool(resume), "note": None}
if row and not opt("--studio") and (turns or tok):
    with (root / "runs" / "runs.ndjson").open("a", encoding="utf-8") as f: f.write(json.dumps(line) + "\n")
    if not resume:
      fresh = (root / "registry.md").read_text(encoding="utf-8")
      new = re.sub(rf"^(\| {aid} \|(?:[^|]*\|){{4}}) \d+ \|", lambda m: f"{m.group(1)} {n} |", fresh, flags=re.M)
      (root / "registry.md").write_text(new, encoding="utf-8")
print(json.dumps(line))
