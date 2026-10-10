"""Show one artist's day as it happens, in its own console window (opened by day.py; closes a minute after the day ends).
usage: python tools/watch.py runs/days/<id>.stream.jsonl
Reads the events both CLIs write (claude stream-json, codex --json) and prints what the artist says and does."""
import sys, json, time, os, pathlib, textwrap
path = pathlib.Path(sys.argv[1]); pos = 0; W = 110

def short(x, n=160):
    x = " ".join(str(x).split()); return x if len(x) <= n else x[:n] + "…"

def say(prefix, text, width=W):
    for i, line in enumerate(textwrap.wrap(" ".join(str(text).split()), width - len(prefix)) or [""]):
        print((prefix if i == 0 else " " * len(prefix)) + line)

def show(ev):
    t = ev.get("type")
    if t == "day":
        os.system(f"title {ev['id']} session {ev['n']}" if os.name == "nt" else "")
        print(f"=== {ev['id']} · session {ev['n']} · {ev['model']} {ev['effort']} · K={ev['k']}{' · resumed' if ev.get('resumed') else ''} ===\n")
    elif t == "turn_end": print(f"\n--- end of turn {ev['turn']} of {ev['of']} ---\n")
    elif t == "end": print("\n=== day over" + (f": {ev['error']}" if ev.get("error") else "") + " ==="); return True
    elif t == "assistant":  # claude
        for c in ev.get("message", {}).get("content", []):
            if c.get("type") == "text" and c.get("text", "").strip(): say("  ", c["text"])
            elif c.get("type") == "tool_use":
                i = c.get("input", {}); arg = i.get("command") or i.get("file_path") or i.get("pattern") or i.get("url") or i.get("query") or ""
                print(f"  > {c.get('name')}: {short(arg)}")
    elif t == "result": print(f"  [turn result: {short(ev.get('result', ''), 300)}]")
    elif t == "item.completed":  # codex
        it = ev.get("item", {}); k = it.get("type")
        if k == "agent_message": say("  ", it.get("text", ""))
        elif k == "command_execution": print(f"  > shell: {short(it.get('command'))}  (exit {it.get('exit_code')})")
        elif k == "file_change": print("  > files: " + ", ".join(f"{c.get('kind')} {pathlib.Path(c.get('path', '')).name}" for c in it.get("changes", [])))
        elif k == "web_search": print(f"  > web: {short(it.get('query', ''))}")
        elif k == "reasoning" and it.get("text"): say("  · ", short(it["text"], 300))
    elif t in ("turn.failed", "error"): print(f"  ! {short(json.dumps(ev), 300)}")
    return False

done_at = None
while True:
    if path.exists():
        with open(path, encoding="utf-8", errors="replace") as f:
            if path.stat().st_size < pos: pos = 0  # a new day began
            f.seek(pos); chunk = f.read(); pos = f.tell()
        for line in chunk.splitlines():
            try: ev = json.loads(line)
            except json.JSONDecodeError: continue
            if show(ev): done_at = time.time()
        sys.stdout.flush()
    if done_at and time.time() - done_at > 60: break
    time.sleep(1)
