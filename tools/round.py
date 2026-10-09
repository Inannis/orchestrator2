"""Run tools/between.py once, finish any unfinished day, then a working day for each remaining artist, three at a time per provider (Anthropic, OpenAI).
usage: python tools/round.py [ids...] [--detach] [--resume-only]   (no ids: every active test arm in registry.md; references run only when named)
A day cut short (usage limit, crash, closed session) keeps runs/days/<id>.state.json and is resumed by the next round.
On a usage limit the round starts nothing new for that provider and says so in runs/round.json (runs/round-2.json if another round is running); continue by hand (control room or this script) after the reset.
--detach starts the round as its own process so it outlives the session or UI that launched it; output in runs/round-<time>.log."""
import sys, re, json, subprocess, pathlib, datetime, os, threading
from concurrent.futures import ThreadPoolExecutor
root = pathlib.Path(__file__).resolve().parent.parent
flags_ = {"--detach", "--resume-only"}
args = [a for a in sys.argv[1:] if a not in flags_]
status_file = root / "runs" / "round.json"
now = lambda: datetime.datetime.now().isoformat(timespec="seconds")

if "--detach" in sys.argv:
    log = root / "runs" / f"round-{datetime.datetime.now():%Y-%m-%d-%H%M}.log"
    flags = 0x00000008 | 0x00000200 if os.name == "nt" else 0  # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
    with log.open("w", encoding="utf-8") as out:
        p = subprocess.Popen([sys.executable, __file__, *[a for a in sys.argv[1:] if a != "--detach"]], cwd=root, stdout=out,
                             stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, creationflags=flags, start_new_session=(os.name != "nt"), close_fds=True)
    print(json.dumps({"detached": True, "pid": p.pid, "log": str(log)})); sys.exit()

reg = (root / "registry.md").read_text(encoding="utf-8")
active = re.findall(r"^\| (a\d+) \|.*\| active \|", reg, re.M)
def provider(i):
    m = re.search(rf"^\| {i} \| [^|]+ \| ([\w.-]+) \|", reg, re.M)
    return "openai" if m and m.group(1).startswith("gpt-") else "anthropic"
ids = args or active
jobs = []
for i in ids:
    st = root / "runs" / "days" / f"{i}.state.json"
    if st.exists():
        s = json.loads(st.read_text(encoding="utf-8"))
        if s.get("left", 0) > 0: jobs.append([i, "--resume", s["sid"], "--k", str(s["left"]), "--n", str(s["n"])]); continue
        st.unlink()
    if "--resume-only" not in sys.argv: jobs.append([i])

try: busy = json.loads(status_file.read_text(encoding="utf-8")).get("state") == "running"
except Exception: busy = False
if busy: status_file = root / "runs" / "round-2.json"
lock = threading.Lock(); stopping = set()
status = {"pid": os.getpid(), "started": now(), "state": "running", "reason": None,
          "jobs": {j[0]: {"status": "queued", "resume": len(j) > 1} for j in jobs}}
def save():
    status["updated"] = now(); status_file.write_text(json.dumps(status, indent=1), encoding="utf-8")
save()

def run(cmd):
    i = cmd[0]
    with lock:
        if provider(i) in stopping:
            status["jobs"][i]["status"] = "not started"; save(); return i, "not started (usage limit earlier in the round)"
        status["jobs"][i]["status"] = "running"; save()
    r = subprocess.run([sys.executable, str(root / "tools" / "day.py"), *cmd], capture_output=True, text=True, encoding="utf-8")
    out = (r.stdout.strip().splitlines() or [r.stderr.strip()[-300:]])[-1]
    try: res = json.loads(out)
    except json.JSONDecodeError: res = {"error": out}
    with lock:
        err = res.get("error")
        status["jobs"][i].update(status="stopped" if err else "done", turns=res.get("turns"), k=res.get("k"), error=err)
        if err and "limit" in err:
            stopping.add(provider(i)); status["reason"] = err
        save()
    return i, out

print(subprocess.run([sys.executable, str(root / "tools" / "between.py")], capture_output=True, text=True).stdout.strip() or "between: nothing to run", flush=True)
print(now(), "starting:", ", ".join(j[0] + (" (resume)" if len(j) > 1 else "") for j in jobs), flush=True)
pools = {p: ThreadPoolExecutor(3) for p in {provider(j[0]) for j in jobs}}
futures = [pools[provider(j[0])].submit(run, j) for j in jobs]
for f in futures:
    i, res = f.result(); print(now(), i, res, flush=True)
for p in pools.values(): p.shutdown()
status["state"] = f"stopped: usage limit ({', '.join(sorted(stopping))})" if stopping else "done"
save(); print(now(), "round", status["state"], flush=True)
