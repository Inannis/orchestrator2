"""A local control room: every artist, its condition and prompts, its runs, and a button that dispatches a working day.
usage: python tools/ui.py [--port 8765]   then open http://127.0.0.1:8765
Reads registry.md, template/conditions.md, runs/runs.ndjson, runs/days/, the studios' git. Dispatch runs tools/day.py, three at a time."""
import sys, json, re, subprocess, pathlib, datetime, time, threading, html
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
root = pathlib.Path(__file__).resolve().parent.parent
PORT = int(sys.argv[sys.argv.index("--port") + 1]) if "--port" in sys.argv else 8765
MAX = 3
running = {}  # id -> {"proc", "started", "k", "model"}
lock = threading.Lock()
MODELS = {"claude-sonnet-5": "Sonnet 5", "claude-opus-5-5": "Opus 5.5", "claude-opus-5": "Opus 5", "claude-haiku-4-5": "Haiku 4.5", "sonnet": "Sonnet (alias)", "haiku": "Haiku (alias)"}
EFFORTS = ["low", "medium", "high", "xhigh", "max"]
ENTRY = ["NOW.md", "STATE.md", "MEMORY.md", "STATUS.md", "journal.md", "notes.md", "memory/notes.md", "memory/journal.md", "memory/MEMORY.md"]

def read(p): return (root / p).read_text(encoding="utf-8")

def conditions():
    out = {}
    for m in re.finditer(r"^\| (\w+) \| (\w+) \| (\w+) \| (\w+) \| (.*) \|$", read("template/conditions.md"), re.M):
        if m.group(1) != "name": out[m.group(1)] = dict(charter=m.group(2), feed=m.group(3), shape=m.group(4), notes=m.group(5))
    return out

def runs():
    rs = []
    for l in read("runs/runs.ndjson").splitlines():
        l = l.strip()
        if l:
            try: rs.append(json.loads(l))
            except json.JSONDecodeError: pass
    return rs

def git(studio, *a):
    try: return subprocess.run(["git", "-C", str(studio), *a], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=10).stdout.strip()
    except Exception: return ""

def continuation_examples(shape):
    ex = ["The day is not over. Something arrived in inbox/.  (first continuation, if the world delivered: p=0.5)",
          "The day is not over.  (every other continuation; K is drawn privately, 1–6)"]
    if shape == "return":
        ex = [e.replace("over.", "over. … From your studio, at random: `<one of its own files>`.", 1) for e in ex]
    return ex

def state():
    conds = conditions(); rs = runs(); today = datetime.date.today().isoformat()
    prompt_t = read("template/SESSION-PROMPT.md")
    arts = []
    for m in re.finditer(r"^\| (a\d+) \| ([^|]+) \| ([\w.-]+) \| ([^|]+) \| ([^|]+) \| (\d+) \|(?: ([^|]+) \|)?", read("registry.md"), re.M):
        aid, path, model, cond, status, sessions, effort = [(x or "").strip() for x in m.groups()]
        studio = (root / path).resolve()
        mine = [r for r in rs if r.get("artist") == aid]
        first = git(studio, "log", "--reverse", "--format=%ad", "--date=short").splitlines()[:1]
        entry = next((e for e in ENTRY if (studio / e).exists()), None)
        words = len((studio / entry).read_text(encoding="utf-8", errors="replace").split()) if entry else None
        works = sum(1 for p in (studio / "works").rglob("*") if p.is_file()) if (studio / "works").exists() else None
        pub = sum(1 for p in (studio / "public").rglob("*") if p.is_file()) if (studio / "public").exists() else 0
        c = conds.get(cond, {})
        n = int(sessions) + 1
        with lock: run = running.get(aid)
        arts.append(dict(
            id=aid, model=model, model_label=MODELS.get(model, model), effort=effort or "–", condition=cond, status=status, sessions=int(sessions), cond=c,
            seeded=first[0] if first else None, runs=len(mine), last=mine[-1].get("date") if mine else None,
            minutes=round(sum(r.get("minutes") or 0 for r in mine)), last_note=(mine[-1].get("note") or "") if mine else "",
            entry=entry, entry_words=words, works=works, public=pub, head=git(studio, "log", "-1", "--format=%ad · %s", "--date=format:%Y-%m-%d %H:%M"),
            url=f"https://inannis.github.io/orchestrator2/{aid}/",
            prompt=prompt_t.replace("{STUDIO}", studio.as_posix()).replace("{DATE}", today).replace("{N}", str(n)),
            continuations=continuation_examples(c.get("shape", "plain")),
            running=None if not run else dict(since=run["started"], minutes=round((time.time() - run["t0"]) / 60, 1), k=run["k"])))
    return dict(artists=arts, models=MODELS, efforts=EFFORTS, conditions=conds, max=MAX, now=datetime.datetime.now().isoformat(timespec="seconds"),
                recent=list(reversed(rs[-12:])))

def reap():
    with lock:
        for aid in [a for a, r in running.items() if r["proc"].poll() is not None]:
            running.pop(aid)

def dispatch(aid, k=None, model=None, effort=None):
    reap()
    with lock:
        if aid in running: return False, f"{aid} is already working"
        if len(running) >= MAX: return False, f"{MAX} artists are already working; wait for one to finish"
        cmd = [sys.executable, str(root / "tools" / "day.py"), aid]
        if k: cmd += ["--k", str(int(k))]
        if model: cmd += ["--model", model]
        if effort: cmd += ["--effort", effort]
        p = subprocess.Popen(cmd, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        running[aid] = dict(proc=p, t0=time.time(), started=datetime.datetime.now().strftime("%H:%M"), k=k or "private")
    return True, f"{aid} dispatched"

def daylog(aid):
    logs = sorted((root / "runs" / "days").glob(f"{aid}-*.md"))
    return logs[-1].read_text(encoding="utf-8") if logs else "No headless day has run for this artist yet."

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def send(self, body, ctype="application/json", code=200):
        b = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(code); self.send_header("Content-Type", ctype + "; charset=utf-8"); self.send_header("Content-Length", str(len(b)))
        self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        u = urlparse(self.path); q = parse_qs(u.query)
        if u.path == "/": return self.send(PAGE, "text/html")
        if u.path == "/api/state": reap(); return self.send(json.dumps(state()))
        aid = (q.get("id") or [""])[0]
        if not re.fullmatch(r"a\d+", aid): return self.send('{"error":"bad id"}', code=400)
        if u.path == "/api/log": return self.send(json.dumps({"text": daylog(aid)}))
        if u.path == "/api/charter":
            row = re.search(rf"^\| {aid} \| ([^|]+) \|", read("registry.md"), re.M)
            p = (root / row.group(1).strip() / "CHARTER.md") if row else None
            return self.send(json.dumps({"text": p.read_text(encoding="utf-8") if p and p.exists() else "(none)"}))
        self.send('{"error":"not found"}', code=404)
    def do_POST(self):
        u = urlparse(self.path)
        if u.path != "/api/dispatch": return self.send('{"error":"not found"}', code=404)
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or "{}")
        aid = body.get("id", "")
        if not re.fullmatch(r"a\d+", aid): return self.send('{"error":"bad id"}', code=400)
        model, effort = body.get("model") or None, body.get("effort") or None
        if model and model not in MODELS: return self.send('{"error":"unknown model"}', code=400)
        if effort and effort not in EFFORTS: return self.send('{"error":"unknown effort"}', code=400)
        ok, msg = dispatch(aid, body.get("k") or None, model, effort)
        self.send(json.dumps({"ok": ok, "message": msg}), code=200 if ok else 409)

PAGE = r"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Studio Control</title>
<style>
:root{--bg:#f6f4ef;--card:#fffdf8;--ink:#1d1b18;--mute:#6f6a61;--line:#e3ded3;--acc:#2f5d50;--acc2:#b4532a;--run:#c9a227}
@media (prefers-color-scheme:dark){:root{--bg:#161513;--card:#1f1d1a;--ink:#ece8df;--mute:#9b958a;--line:#34312b;--acc:#7fb8a4;--acc2:#e08a5f;--run:#e0c050}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 ui-sans-serif,system-ui,-apple-system,Segoe UI,sans-serif}
header{padding:20px 24px 8px;display:flex;align-items:baseline;gap:16px;flex-wrap:wrap}h1{font-size:20px;margin:0;font-weight:650}
.sub{color:var(--mute);font-size:13px}main{padding:8px 24px 40px;max-width:1300px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:14px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.card.paused{opacity:.62}.top{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.id{font:600 18px ui-monospace,Menlo,Consolas,monospace}.tag{font-size:12px;border:1px solid var(--line);border-radius:99px;padding:1px 8px;color:var(--mute)}
.tag.c{color:var(--acc);border-color:var(--acc)}.tag.run{color:var(--run);border-color:var(--run)}
dl{display:grid;grid-template-columns:auto 1fr;gap:2px 12px;margin:10px 0;font-size:13px}dt{color:var(--mute)}dd{margin:0}
details{margin-top:8px;font-size:13px}summary{cursor:pointer;color:var(--acc)}
pre{white-space:pre-wrap;background:var(--bg);border:1px solid var(--line);border-radius:6px;padding:8px;font:12px/1.45 ui-monospace,Menlo,Consolas,monospace;max-height:340px;overflow:auto}
.row{display:flex;gap:8px;align-items:center;margin-top:10px;flex-wrap:wrap}
button{background:var(--acc);color:var(--card);border:0;border-radius:6px;padding:6px 12px;font-weight:600;cursor:pointer}
button[disabled]{opacity:.4;cursor:default}button.ghost{background:none;color:var(--acc);border:1px solid var(--line)}
input,select{background:var(--bg);color:var(--ink);border:1px solid var(--line);border-radius:6px;padding:5px 6px;font-size:13px}
input{width:64px}a{color:var(--acc)}table{border-collapse:collapse;width:100%;font-size:13px}td,th{border-bottom:1px solid var(--line);padding:5px 8px;text-align:left;vertical-align:top}
th{color:var(--mute);font-weight:500}h2{font-size:15px;margin:28px 0 10px}.msg{font-size:13px;color:var(--acc2)}
.note{color:var(--mute);font-size:12.5px;margin-top:6px}
@media (max-width:600px){header,main{padding-left:16px;padding-right:16px}.grid{grid-template-columns:1fr}}
</style></head><body>
<header><h1>Studio Control</h1><span class="sub" id="meta"></span><span class="msg" id="msg"></span></header>
<main><div class="grid" id="grid"></div>
<h2>Conditions</h2><table id="conds"></table>
<h2>Recent days</h2><table id="recent"></table></main>
<script>
const $=s=>document.querySelector(s), esc=s=>String(s??'').replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
let open={};
async function load(){
  const s=await (await fetch('/api/state')).json(); const busy=s.artists.filter(a=>a.running).length;
  $('#meta').textContent=`${busy}/${s.max} working · ${s.now.replace('T',' ')}`;
  $('#grid').innerHTML=s.artists.map(a=>{const c=a.cond||{}; const paused=!a.status.startsWith('active');
    return `<div class="card ${paused?'paused':''}"><div class="top"><span class="id">${a.id}</span>
      <span class="tag c">${esc(a.condition)}</span><span class="tag" title="${esc(a.model)}">${esc(a.model_label)} · ${esc(a.effort)}</span><span class="tag">${esc(a.status)}</span>
      ${a.running?`<span class="tag run">working since ${a.running.since} · ${a.running.minutes} min · K ${a.running.k}</span>`:''}</div>
      <dl><dt>charter · feed · shape</dt><dd>${esc(c.charter||'?')} · ${esc(c.feed||'?')} · ${esc(c.shape||'?')}</dd>
      <dt>seeded</dt><dd>${esc(a.seeded)}</dd><dt>sessions</dt><dd>${a.sessions} (ledger: ${a.runs} runs, ${a.minutes} min, last ${esc(a.last||'–')})</dd>
      <dt>handoff</dt><dd>${a.entry?`${esc(a.entry)} · ${a.entry_words} words`:'–'}</dd><dt>works · public</dt><dd>${a.works??'–'} · ${a.public} files · <a href="${a.url}" target="_blank">site</a></dd>
      <dt>last commit</dt><dd>${esc(a.head)}</dd></dl>
      ${a.last_note?`<div class="note">${esc(a.last_note.slice(0,260))}${a.last_note.length>260?'…':''}</div>`:''}
      <details data-k="p-${a.id}" ${open['p-'+a.id]?'open':''}><summary>Prompts for session ${a.sessions+1}</summary><pre>${esc(a.prompt)}</pre><pre>${a.continuations.map(esc).join('\n')}</pre></details>
      <details data-k="c-${a.id}" data-fetch="charter" data-id="${a.id}" ${open['c-'+a.id]?'open':''}><summary>Charter</summary><pre>…</pre></details>
      <details data-k="l-${a.id}" data-fetch="log" data-id="${a.id}" ${open['l-'+a.id]?'open':''}><summary>Latest headless day</summary><pre>…</pre></details>
      <div class="row"><button ${a.running||paused||busy>=s.max?'disabled':''} onclick="go('${a.id}')">Dispatch a day</button>
      <label class="sub">K <input id="k-${a.id}" placeholder="private"></label>
      <label class="sub">model <select id="m-${a.id}">${Object.entries(s.models).filter(([id])=>!['sonnet','haiku'].includes(id)).map(([id,l])=>`<option value="${id===a.model?'':id}" ${id===a.model?'selected':''}>${esc(l)} · ${esc(id)}${id===a.model?' (registry)':''}</option>`).join('')}</select></label>
      <label class="sub">effort <select id="e-${a.id}">${s.efforts.map(e=>`<option value="${e===a.effort?'':e}" ${e===a.effort?'selected':''}>${e}${e===a.effort?' (registry)':''}</option>`).join('')}</select></label></div></div>`}).join('');
  document.querySelectorAll('details').forEach(d=>{d.ontoggle=()=>{open[d.dataset.k]=d.open; if(d.open&&d.dataset.fetch) fill(d)}; if(d.open&&d.dataset.fetch) fill(d)});
  $('#conds').innerHTML='<tr><th>name</th><th>charter</th><th>feed</th><th>shape</th><th>notes</th></tr>'+Object.entries(s.conditions).map(([n,c])=>`<tr><td>${esc(n)}</td><td>${esc(c.charter)}</td><td>${esc(c.feed)}</td><td>${esc(c.shape)}</td><td>${esc(c.notes)}</td></tr>`).join('');
  $('#recent').innerHTML='<tr><th>run</th><th>date</th><th>model · effort</th><th>min</th><th>turns</th><th>note</th></tr>'+s.recent.map(r=>`<tr><td>${esc(r.run)}</td><td>${esc(r.date)}</td><td>${esc(r.model)}${r.effort?' · '+esc(r.effort):''}</td><td>${esc(r.minutes)}</td><td>${esc(r.turns)}</td><td>${esc((r.note||r.error||'').slice(0,200))}</td></tr>`).join('');
}
async function fill(d){const r=await (await fetch(`/api/${d.dataset.fetch}?id=${d.dataset.id}`)).json(); d.querySelector('pre').textContent=r.text}
async function go(id){const k=$('#k-'+id).value, model=$('#m-'+id).value, effort=$('#e-'+id).value;
  const r=await fetch('/api/dispatch',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id,k,model,effort})});
  $('#msg').textContent=(await r.json()).message; load()}
load(); setInterval(load,15000);
</script></body></html>"""

if __name__ == "__main__":
    print(f"Studio Control on http://127.0.0.1:{PORT}")
    ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
