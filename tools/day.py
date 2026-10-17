"""Run one artist's working day headless, end to end: first turn, one encounter draw, K private continuations, a ledger line.
usage: python tools/day.py <id> [--k K] [--model M] [--effort E] [--shape S] [--resume SESSION_ID] [--studio PATH] [--n N] [--enc-p P] [--feed F] [--no-window]
Shapes (how the day is kept going; see template/conditions.md): "plain" says only that the day is not over;
"return" also hands back one of the artist's own earlier files, drawn at random; "object" brings a new random object with every continuation.
Needs the claude CLI logged in (`claude auth login` or CLAUDE_CODE_OAUTH_TOKEN). Handbacks go to runs/days/, not to anyone's context."""
import sys, json, re, random, subprocess, pathlib, datetime, time, shutil, os
root = pathlib.Path(__file__).resolve().parent.parent
args = sys.argv[1:]; aid = args[0]
def opt(name, default=None):
    return args[args.index(name) + 1] if name in args else default
reg = (root / "registry.md").read_text(encoding="utf-8")
row = re.search(rf"^\| {aid} \| ([^|]+) \| ([\w.-]+) \| (\w+) \| [^|]+ \| (\d+) \|(?: (\w+) \|)?", reg, re.M)
studio = pathlib.Path(opt("--studio") or (root / row.group(1).strip())).resolve()
model = opt("--model") or (row.group(2) if row else "claude-sonnet-5-5")
effort = opt("--effort") or (row.group(5) if row and row.group(5) else "medium")
n = int(opt("--n") or ((int(row.group(4)) + (0 if "--resume" in args else 1)) if row else 1))
state_file = root / "runs" / "days" / f"{aid}.state.json"  # exists only while a day is unfinished; round.py resumes it
live_file = root / "runs" / "days" / f"{aid}.live.json"     # what this day is doing right now, for the control room
def live(status, **kw):
    try: live_file.write_text(json.dumps({"id": aid, "status": status, "n": n, "k": k, "updated": datetime.datetime.now().isoformat(timespec="seconds"), **kw}), encoding="utf-8")
    except Exception: pass
k = int(opt("--k") or random.randint(1, 6))
resume = opt("--resume")  # continue an interrupted day: --resume <session id> --k <continuations left>
cond = row.group(3) if row else None
crow = re.search(rf"^\| {cond} \| \w+ \| [\w-]+ \| (\w+) \| (\w+) \|", (root / "template" / "conditions.md").read_text(encoding="utf-8"), re.M) if cond else None
shape = opt("--shape") or (crow.group(1) if crow else "plain")
memory = crow.group(2) if crow else "own"
if shape == "long" and not opt("--k") and not opt("--resume"): k = random.randint(6, 9)  # long: more continuations, nothing else said
FLOOR = 20 * 60 if shape == "minimum" else 0  # minimum: the day goes on until it has lasted this long, never said
today = datetime.date.today().isoformat()
prompt = (root / "template" / "SESSION-PROMPT.md").read_text(encoding="utf-8").replace("{STUDIO}", studio.as_posix()).replace("{DATE}", today).replace("{N}", str(n))
if memory in ("rooms", "deskw") and n % 5 == 0:  # a studio day is for sorting, not making, so it is short
    prompt += "\n\nToday is a studio day."; k = min(k, 1)
GUIDE = None  # a guide read one movement per turn: GENESIS.md on the genesis day, REVIEW.md on a review day
if memory == "studio" and n % 5 == 0:  # the `studio` system's review day: reading the practice whole takes a day of its own
    prompt += "\n\nToday is a review day."; k = min(k, 2)
    if (studio / "REVIEW.md").exists(): GUIDE = "REVIEW.md"; prompt += " Read `REVIEW.md` and begin with its first movement."
GENESIS = shape == "genesis" and n == 1 and (studio / "GENESIS.md").exists()  # session 1 is the genesis day
if GENESIS:
    GUIDE = "GENESIS.md"; prompt += "\n\nToday is your genesis day. After the charter, read `GENESIS.md` and begin with its first movement."
if GUIDE and not resume: k = len(re.findall(r"^## ", (studio / GUIDE).read_text(encoding="utf-8"), re.M)) - 1
SESSION, step = None, [0]  # a session system: the condition's variant may hold session.json, organising every ordinary day turn by turn
crow_c = re.search(rf"^\| {cond} \| ([\w-]+) \|", (root / "template" / "conditions.md").read_text(encoding="utf-8"), re.M) if cond else None
sj = root / "template" / "variants" / crow_c.group(1) / "session.json" if crow_c else None
if not GUIDE and sj and sj.exists():
    SESSION = json.loads(sj.read_text(encoding="utf-8"))
    if "kinds" in SESSION:  # several kinds of day: the artist named tomorrow's in its letter ('Tomorrow: a research day')
        letter = studio / "NOW.md" if (studio / "NOW.md").exists() else studio / "days" / f"{n - 1:03d}.md"
        named = re.findall(r"Tomorrow:\s*an?\s+(\w+)\s+day", letter.read_text(encoding="utf-8", errors="replace"), re.I) if letter.exists() else []
        kind = named[-1].lower() if named and named[-1].lower() in SESSION["kinds"] else SESSION["default"]
        SESSION = SESSION["kinds"][kind]
    prompt += "\n\n" + SESSION["open"]
    if not resume: k = len(SESSION["steps"])
    else: step[0] = max(0, len(SESSION["steps"]) + 1 - k)  # a resumed day first finishes the cut turn, then takes the next step
if not resume and (studio / "press").is_dir():  # a critic's new article is announced once, in the day's opening
    seen_f = root / "runs" / "press-seen.json"; seen = json.loads(seen_f.read_text(encoding="utf-8")) if seen_f.exists() else {}
    new = sorted(f.name for f in (studio / "press").glob("*.md") if f.name not in seen.get(aid, []))
    if new:
        prompt += "\n\nA critic wrote about your work: " + ", ".join(f"`press/{f}`" for f in new) + "."
        seen[aid] = seen.get(aid, []) + new; seen_f.write_text(json.dumps(seen, indent=1), encoding="utf-8")
handed = set()  # files already handed back today: no repeats within a day

def own_file():
    """One thing the artist made, at random: an image, sound or text piece, never its memory, logs, notes or the orchestrator's files.
    Prefers work from earlier days and never repeats within a day."""
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
    fresh = [x for x in fs if x not in handed]
    earlier = [x for x in fresh if datetime.date.fromtimestamp((studio / x).stat().st_mtime).isoformat() < today]
    pick = random.choice(earlier or fresh or fs) if fs else None
    if pick: handed.add(pick)
    return pick

CONTINUE = "Go on from where you were."  # after a dropped connection: the same turn goes on, nothing else changes

def more(first_arrival):
    if SESSION:
        msg = SESSION["steps"][min(step[0], len(SESSION["steps"]) - 1)]; step[0] += 1
        return msg + (" Something arrived in inbox/." if first_arrival else "")
    if GUIDE: return f"The day is not over. Read the next movement in `{GUIDE}` and go on."
    if shape == "object" and not first_arrival:  # every continuation brings a new object (the first draw already did)
        feed = ["--feed", opt("--feed")] if opt("--feed") else []
        first_arrival = "delivered" in subprocess.run([sys.executable, str(root / "tools" / "encounter.py"), str(studio), "--p", "1"] + feed, capture_output=True, text=True).stdout
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

def codex_exe():
    """The native Codex binary under the npm shim (Windows), else `codex`."""
    w = shutil.which("codex")
    if w:
        for exe in (pathlib.Path(w).parent / "node_modules" / "@openai").rglob("codex.exe"):
            if exe.parent.name == "bin": return str(exe)
    return w or "codex"

STREAM = root / "runs" / "days" / f"{aid}.stream.jsonl"  # the day's events as they happen; tools/watch.py shows them in a window

def streamed(cmd, env=None):
    """Run one CLI turn with its events appended to STREAM (a file, not a pipe: a job the artist leaves running
    in the background would hold a pipe open and stall the day). Returns (events written by this turn, stderr)."""
    import tempfile
    start = STREAM.stat().st_size if STREAM.exists() else 0
    with open(STREAM, "a", encoding="utf-8") as o, tempfile.TemporaryFile("w+", encoding="utf-8") as e:
        subprocess.run(cmd, cwd=studio, stdout=o, stderr=e, stdin=subprocess.DEVNULL, timeout=5400, env=env)
        e.seek(0); err = e.read()
    with open(STREAM, encoding="utf-8", errors="replace") as f:
        f.seek(start); return f.read(), err

def mark(**ev):
    with open(STREAM, "a", encoding="utf-8") as f: f.write(json.dumps(ev) + "\n")

def codex_turn(text, sid=None):
    """One Codex turn (models named gpt-*): no sandbox (user), its own CODEX_HOME if CODEX_STUDIO_HOME is set.
    Returns the same shape as a claude -p result: result, session_id, usage, is_error."""
    import tempfile
    env = dict(os.environ)
    if os.environ.get("CODEX_STUDIO_HOME"): env["CODEX_HOME"] = os.environ["CODEX_STUDIO_HOME"]
    with tempfile.TemporaryDirectory() as tmp:
        last = pathlib.Path(tmp) / "last.txt"
        common = ["--json", "-m", model, "-c", f"model_reasoning_effort={effort}", "--skip-git-repo-check",
                  # the user's Codex config (plugins, computer use, browser, MCP) stays out of a studio; web search stays in
                  "--ignore-user-config", "-c", 'web_search="live"', "--disable", "computer_use", "--disable", "browser_use", "--disable", "browser_use_external", "--disable", "apps",
                  "--dangerously-bypass-approvals-and-sandbox", "-o", str(last)]
        cmd = [codex_exe(), "exec", "resume", sid] + common + [text] if sid else [codex_exe(), "exec", "-C", str(studio)] + common + [text]
        out, err = streamed(cmd, env)
        result = last.read_text(encoding="utf-8", errors="replace").strip() if last.exists() else ""
    d = {"session_id": sid, "usage": {}, "total_cost_usd": 0, "result": result}
    for line in out.splitlines():
        try: ev = json.loads(line)
        except json.JSONDecodeError: continue
        if ev.get("type") == "thread.started": d["session_id"] = ev.get("thread_id")
        elif ev.get("type") == "turn.completed":
            u = ev.get("usage") or {}; d["usage"] = {"input_tokens": u.get("input_tokens", 0), "output_tokens": u.get("output_tokens", 0)}
        elif ev.get("type") in ("turn.failed", "error"):
            d["is_error"] = True; d["result"] = json.dumps(ev)[:1500]
    if not result and not d.get("is_error"): d["is_error"] = True; d["result"] = (out + err)[-2000:]
    return d

def turn(text, sid=None):
    if model.startswith("gpt-"): return codex_turn(text, sid)
    cmd = [CLAUDE, "-p", text, "--model", model, "--output-format", "stream-json", "--verbose", "--effort", effort, "--permission-mode", "acceptEdits",
           "--allowedTools", TOOLS, "--settings", '{"autoMemoryEnabled": false}', "--strict-mcp-config"]  # no MCP servers in a studio
    if sid: cmd += ["--resume", sid]
    out, err = streamed(cmd)
    for line in reversed(out.splitlines()):
        try: ev = json.loads(line)
        except json.JSONDecodeError: continue
        if ev.get("type") == "result": return ev
    return {"is_error": True, "result": (out + err)[-2000:]}

def wait_for_reset(msg):
    """On 'You've hit your session limit · resets 6pm (Europe/Berlin)', sleep until then plus two minutes. False if unparseable or over six hours."""
    m = re.search(r"resets (\d{1,2})(?::(\d{2}))?\s*(am|pm)\s*\(([^)]+)\)", msg)
    if not m: return False
    from zoneinfo import ZoneInfo
    tz = ZoneInfo(m.group(4)); now = datetime.datetime.now(tz)
    at = now.replace(hour=int(m.group(1)) % 12 + (12 if m.group(3) == "pm" else 0), minute=int(m.group(2) or 0), second=0, microsecond=0)
    if at <= now: at += datetime.timedelta(days=1)
    secs = (at - now).total_seconds() + 120
    if secs > 6 * 3600: return False
    print(f"{aid}: usage limit, waiting {secs / 60:.0f} min", file=sys.stderr, flush=True)
    time.sleep(secs); return True

if not resume and memory in ("rooms", "desk", "deskw", "studio", "project") and (studio / "NOW.md").exists():
    (studio / "days").mkdir(exist_ok=True)
    (studio / "NOW.md").replace(studio / "days" / f"{n - 1:03d}.md")
if not resume and memory in ("desk", "deskw"):
    subprocess.run([sys.executable, str(root / "tools" / "desk.py"), str(studio)])
commit_error = None
t0 = time.time(); turns = 0; cost = 0.0; tok = 0; enc = "none"; err = None; waits = 0
STREAM.write_text("", encoding="utf-8"); mark(type="day", id=aid, n=n, model=model, effort=effort, k=k, resumed=bool(resume))
if os.name == "nt" and "--no-window" not in args:  # a console window that shows the day as it happens; it closes when the day ends
    subprocess.Popen([sys.executable, str(root / "tools" / "watch.py"), str(STREAM)], creationflags=subprocess.CREATE_NEW_CONSOLE)
msgs = [prompt] if not resume else [CONTINUE]  # a resumed day finishes its cut turn first
sid = resume
with log.open("w", encoding="utf-8") as f:
    f.write(f"# {aid} session {n} · {today} · {model} · effort {effort} · K={k}\n\n")
    total = (k + 1 if not resume else k) + (40 if FLOOR else 0)
    for i in range(total):
        live("running", turn=i + 1, turns=total, resumed=bool(resume), since=datetime.datetime.fromtimestamp(t0).isoformat(timespec="seconds"))
        d = turn(msgs[-1], sid)
        while d.get("is_error") and "limit" in str(d.get("result", "")) and waits < 3 and "--wait" in args and wait_for_reset(str(d.get("result", ""))):
            waits += 1; sid = d.get("session_id") or sid
            f.write(f"## (usage limit; waited for the reset, same day continues)\n\n"); f.flush()
            d = turn(CONTINUE if sid else msgs[-1], sid)
        sid = d.get("session_id", sid); cost += d.get("total_cost_usd") or 0
        u = d.get("usage") or {}; tok += sum(u.get(x, 0) or 0 for x in ["input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"])
        sent = "(session prompt)" if (i == 0 and not resume) else msgs[-1]
        f.write(f"## turn {i + 1}\n\n> {sent}\n\n{d.get('result', '')}\n\n"); f.flush()
        mark(type="turn_end", turn=i + 1, of=total, prompt=sent)
        retries = 0
        while d.get("is_error") and "limit" not in str(d.get("result", "")) and retries < 6:  # a dropped connection: the same turn continues
            time.sleep([30, 60, 120, 240, 480, 600][retries]); retries += 1; sid = d.get("session_id") or sid
            f.write("## (connection dropped; the same turn continued)\n\n"); f.flush()
            d = turn(CONTINUE if sid else msgs[-1], sid)
            sid = d.get("session_id", sid)
        if d.get("is_error"):
            err = str(d.get("result", ""))[:300]
            sid = d.get("session_id") or sid
            if row and not opt("--studio") and sid and not (resume and "limit" not in err):  # resume a cut day once; a resumed day that drops again ends (a broken conversation would block the artist)
                state_file.write_text(json.dumps({"n": n, "sid": sid, "left": total - i, "k": k, "date": today}), encoding="utf-8")
                if turns == 0 and not resume:
                    fresh = (root / "registry.md").read_text(encoding="utf-8")
                    (root / "registry.md").write_text(re.sub(rf"^(\| {aid} \|(?:[^|]*\|){{4}}) \d+ \|", lambda m: f"{m.group(1)} {n} |", fresh, flags=re.M), encoding="utf-8")
            break
        turns += 1
        if row and not opt("--studio"):
            left = (k - i) if not resume else (k - i - 1)
            state_file.write_text(json.dumps({"n": n, "sid": sid, "left": left, "k": k, "date": today}), encoding="utf-8")
            if turns == 1 and not resume:
                fresh = (root / "registry.md").read_text(encoding="utf-8")
                (root / "registry.md").write_text(re.sub(rf"^(\| {aid} \|(?:[^|]*\|){{4}}) \d+ \|", lambda m: f"{m.group(1)} {n} |", fresh, flags=re.M), encoding="utf-8")
        if i >= (k if not resume else k - 1) and time.time() - t0 >= FLOOR: break
        if i == 0 and not resume and not GUIDE:
            e = subprocess.run([sys.executable, str(root / "tools" / "encounter.py"), str(studio), "--p", opt("--enc-p", "0.5")] + (["--feed", opt("--feed")] if opt("--feed") else []), capture_output=True, text=True).stdout
            m = re.search(r"delivered \S+ \S+ (\w+)", e)
            enc = m.group(1) if m else "none"
            msgs.append(more(bool(m)))
        else:
            msgs.append(more(False))

if turns and (studio / "public" / "wall.md").exists():  # a `wall` studio: the front page is hung from the wall, the same plain frame for all
    subprocess.run([sys.executable, str(root / "tools" / "hang.py"), str(studio)], capture_output=True)
if turns and (studio / ".git").exists():  # whatever the artist left uncommitted is kept; git is the studio's history (desk.py reads it)
    excl = studio / ".git" / "info" / "exclude"; excl.parent.mkdir(exist_ok=True)  # browser profiles and caches a tool left behind are not history
    pats = ["*-profile/", ".*-profile/", "*profile*/Default/", "__pycache__/", "*.tmp", ".cache/"]
    have = excl.read_text(encoding="utf-8") if excl.exists() else ""
    if any(p not in have for p in pats): excl.write_text(have + "\n" + "\n".join(p for p in pats if p not in have) + "\n", encoding="utf-8")
    for p in studio.rglob("*"):  # a file named after a Windows device (nul.png, con.txt) blocks every commit: rename it
        if ".git" not in p.parts and re.match(r"^(con|prn|aux|nul|com\d|lpt\d)(\..*)?$", p.name, re.I):
            try: os.rename("\\\\?\\" + str(p), "\\\\?\\" + str(p.with_name("_" + p.name)))
            except OSError: pass
    added = subprocess.run(["git", "-C", str(studio), "add", "-A"], capture_output=True, text=True)
    committed = subprocess.run(["git", "-C", str(studio), "commit", "-qm", f"End of session {n}, as left"], capture_output=True, text=True)
    if added.returncode or (committed.returncode and "nothing to commit" not in committed.stdout + committed.stderr):
        commit_error = (added.stderr + committed.stderr).strip()[-300:]
line = {"run": f"{aid}-{n:03d}", "artist": aid, "n": n, "date": today, "model": model, "effort": effort, "condition": cond, "shape": shape,
        "minutes": round((time.time() - t0) / 60), "turns": turns, "k": k, "encounter": enc, "tokens": tok, "cost_usd": round(cost, 2),
        "error": err, "session_id": sid, "resumed": bool(resume), "note": None}
if commit_error: line["commit_error"] = commit_error  # the studio's history failed to record this day
if row and not opt("--studio") and turns:
    with (root / "runs" / "runs.ndjson").open("a", encoding="utf-8") as f: f.write(json.dumps(line) + "\n")
if not err and state_file.exists(): state_file.unlink()
limit = bool(err and "limit" in err)
mark(type="end", error=err)
live("stopped" if err else "done", turns_done=turns, error=err, limit=limit, reset=(re.search(r"resets ([^·]+?\))", err or "") or [None, None])[1] if limit else None,
     resumable=state_file.exists())
print(json.dumps(line))
