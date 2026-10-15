"""A performer for a score: someone who has never met the artist reads only the score, performs it, and the studio gets the performance back.
usage: python tools/perform.py <score-file> [--out DIR] [--no-picture]
The performer (a fresh agent, Sonnet medium) decides what the score leaves open, as a real player, dancer or reader would, and writes
performance.json (what sounded, when), account.md (what they did and where the score resisted them) and scene.txt (the moment an audience would see).
The sounding events become performance.wav (instruments synthesised here); the scene becomes performance.png through the image model."""
import sys, json, re, shutil, subprocess, tempfile, pathlib, datetime, os
import numpy as np
from scipy.io import wavfile
root = pathlib.Path(__file__).resolve().parent.parent
args = sys.argv[1:]; score = pathlib.Path(args[0]).resolve()
out = pathlib.Path(args[args.index("--out") + 1]).resolve() if "--out" in args else score.parent / "performances" / f"{score.stem}-{datetime.datetime.now():%Y%m%d-%H%M}"
out.mkdir(parents=True, exist_ok=True)
SR = 44100
INSTRUMENTS = ["reed", "bowed", "plucked", "keys", "voice", "wind", "bell", "drum", "breath", "sine"]

BRIEF = f"""You are a performer. An artist you have never met has handed you a score: `{score.name}` in this folder. Read it, and anything it points to in this folder, and nothing else. Then perform it, in your own way: decide everything it leaves open the way a real musician, dancer, actor or reader would (tempo, breath, where you stand, how long a silence really lasts, what you do when it is unclear), and take its instructions seriously, including the ones you'd argue with.

Write three files here:
1. `performance.json`: what sounded, as a list of events: {{"t": start seconds, "dur": seconds, "instrument": one of {INSTRUMENTS}, "note": a pitch like "A4" or "C#3" (or "-" for unpitched), "dyn": loudness 0 to 1}}. Use the instrument nearest to what the score asks (a bayan or accordion is "reed", a violin "bowed", a guitar or oud "plucked", a sung or hummed line "voice", rain or breath "breath"). If nothing in it sounds, write an empty list.
2. `account.md`: what you did, moment by moment, as a performer tells it afterwards: what you chose and why, where the score helped, where it resisted you, what surprised you, how it felt to do. Plain words, at most 400 words. No advice to the artist.
3. `scene.txt`: one or two sentences describing what someone watching would have seen at the most telling moment: the room, the light, the bodies, the instruments. Concrete enough to paint.

Your last message can be short; the files are what count."""

def exe(name, sub):
    w = shutil.which(name)
    if w and os.name == "nt":
        for p in (pathlib.Path(w).parent / "node_modules").rglob(sub):
            if p.parent.name == "bin": return str(p)
    return w or name

def hz(note):
    m = re.match(r"^([A-Ga-g])([#b]?)(-?\d)$", str(note).strip())
    if not m: return None
    n = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}[m.group(1).upper()] + {"#": 1, "b": -1, "": 0}[m.group(2)]
    return 440.0 * 2 ** ((n + 12 * (int(m.group(3)) + 1) - 69) / 12)

def env(n, a, r, sustain=1.0):
    e = np.full(n, sustain); a = min(int(a * SR), n // 2); r = min(int(r * SR), n - a)
    if a: e[:a] = np.linspace(0, sustain, a)
    if r: e[-r:] *= np.linspace(1, 0, r)
    return e

def voice_of(inst, f, dur, rng):
    n = max(int(dur * SR), 1); t = np.arange(n) / SR
    if inst == "plucked" and f:  # Karplus-Strong
        p = max(int(SR / f), 2); buf = rng.uniform(-1, 1, p); y = np.empty(n)
        for i in range(n):
            y[i] = buf[i % p]; buf[i % p] = 0.996 * 0.5 * (buf[i % p] + buf[(i + 1) % p])
        return y
    if inst in ("drum", "breath") or not f:
        noise = rng.normal(0, 1, n)
        if inst == "breath": return np.convolve(noise, np.ones(40) / 40, "same") * env(n, min(0.3, dur / 3), min(0.4, dur / 3))
        return noise * np.exp(-t * 18)
    vib = 1 + (0.004 * np.sin(2 * np.pi * 5.5 * t) if inst in ("bowed", "voice", "wind") else 0)
    ph = 2 * np.pi * f * np.cumsum(vib) / SR
    if inst == "reed":  # two slightly detuned reeds, square-ish, with bellows swell
        y = sum(np.sign(np.sin(ph * d)) * 0.5 + np.sin(ph * d * 2) * 0.2 for d in (1.0, 1.004))
        return np.convolve(y, np.ones(6) / 6, "same") * env(n, 0.06, 0.12) * (1 + 0.15 * np.sin(2 * np.pi * 0.8 * t))
    if inst == "bowed":
        y = sum(np.sin(ph * k) / k for k in range(1, 12))
        return y * env(n, 0.12, 0.2)
    if inst == "keys":
        y = sum(np.sin(ph * k * (1 + 0.0004 * k * k)) * np.exp(-t * (1.2 + k * 0.8)) / k for k in range(1, 8))
        return y * env(n, 0.005, 0.1)
    if inst == "voice":  # a sung "ah": harmonics weighted by two formants
        y = sum(np.sin(ph * k) * (np.exp(-((f * k - 730) / 180) ** 2) + 0.6 * np.exp(-((f * k - 1090) / 200) ** 2) + 0.05) for k in range(1, 24))
        return y * env(n, 0.08, 0.15)
    if inst == "wind":
        return (np.sin(ph) + 0.15 * np.sin(ph * 2) + 0.03 * rng.normal(0, 1, n)) * env(n, 0.05, 0.1)
    if inst == "bell":
        return sum(np.sin(ph * r) * np.exp(-t * (1.5 + i)) for i, r in enumerate((1, 2.76, 5.4, 8.93))) * env(n, 0.002, 0.05)
    return np.sin(ph) * env(n, 0.02, 0.05)

def render(events, path):
    rng = np.random.default_rng(7)
    end = max((e.get("t", 0) + e.get("dur", 0) for e in events), default=0) + 1.0
    mix = np.zeros(int(end * SR) + SR)
    for e in events:
        inst = e.get("instrument", "sine"); inst = inst if inst in INSTRUMENTS else "sine"
        y = voice_of(inst, hz(e.get("note", "-")), max(float(e.get("dur", 0.5)), 0.02), rng)
        y = y / (np.max(np.abs(y)) or 1) * float(e.get("dyn", 0.6))
        s = int(float(e.get("t", 0)) * SR); mix[s:s + len(y)] += y[:len(mix) - s]
    mix = mix / (np.max(np.abs(mix)) or 1) * 0.85
    wavfile.write(path, SR, (mix * 32767).astype(np.int16))

with tempfile.TemporaryDirectory() as tmp:
    tmp = pathlib.Path(tmp); shutil.copy(score, tmp / score.name)
    for ref in re.findall(r"[\w./-]+\.(?:png|jpg|svg|wav|md|txt)", score.read_text(encoding="utf-8", errors="replace")):
        p = (score.parent / ref).resolve()
        if p.is_file() and p != score: shutil.copy(p, tmp / p.name)
    cmd = [exe("claude", "claude.exe"), "-p", BRIEF, "--model", "claude-sonnet-5-5", "--effort", "medium", "--output-format", "json",
           "--permission-mode", "acceptEdits", "--allowedTools", "Read Glob Write", "--strict-mcp-config", "--settings", '{"autoMemoryEnabled": false}']
    subprocess.run(cmd, cwd=tmp, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=1800)
    for f in ("performance.json", "account.md", "scene.txt"):
        if (tmp / f).exists(): shutil.copy(tmp / f, out / f)
if not (out / "account.md").exists():
    sys.exit("The performer did not come this time.")
try: events = json.loads((out / "performance.json").read_text(encoding="utf-8")) if (out / "performance.json").exists() else []
except json.JSONDecodeError: events = []
if isinstance(events, dict): events = events.get("events", [])
if events: render(events, out / "performance.wav")
if "--no-picture" not in args and (out / "scene.txt").exists():
    subprocess.run([sys.executable, str(root / "tools" / "image.py"), (out / "scene.txt").read_text(encoding="utf-8").strip()[:900], str(out / "performance.png")], capture_output=True, timeout=300)
print(f"performed: {out}")
for f in ("account.md", "performance.wav", "performance.png", "performance.json", "scene.txt"):
    if (out / f).exists(): print(" ", f)
