"""Lay out DESK.md in a studio with `desk` memory: yesterday's letter, works touched lately, works returned to most, the one left alone longest, what waits.
usage: python tools/desk.py <studio>   (run by day.py before each new day; the artist never writes the desk)
A work is a folder in works/ or, for loose files, everything sharing one name stem. Touches come from the studio's git history."""
import sys, re, subprocess, pathlib, collections
studio = pathlib.Path(sys.argv[1]).resolve()
works = studio / "works"

def key(rel):
    parts = rel.split("/")
    if len(parts) < 2 or parts[0] != "works": return None
    return parts[1] if len(parts) > 2 else re.sub(r"\..*$", "", parts[1])

log = subprocess.run(["git", "-C", str(studio), "log", "--name-only", "--format=@%ad", "--date=short"], capture_output=True, text=True, encoding="utf-8").stdout
days = collections.defaultdict(set); date = None
for line in log.splitlines():
    if line.startswith("@"): date = line[1:]
    elif line and (k := key(line)): days[k].add(date)
alive = {k for k in days if (works / k).is_dir() or any(works.glob(k + ".*"))}
days = {k: v for k, v in days.items() if k in alive}

def notes(k):
    d = works / k
    cands = sorted(d.glob("*.md")) if d.is_dir() else sorted(works.glob(k + ".md")) + sorted(works.glob(k + ".txt"))
    for c in cands:
        lines = [l.strip() for l in c.read_text(encoding="utf-8", errors="replace").splitlines() if l.strip() and not l.startswith("#")]
        if lines: return " ".join(lines[:3])[:300]
    return ""

def item(k): return f"- `works/{k}`" + (f": {notes(k)}" if notes(k) else "")

out = ["# Desk", "", "Laid out this morning from the studio. Nobody writes here; it is made again tomorrow.", ""]
letters = sorted((studio / "days").glob("*.md")) if (studio / "days").is_dir() else []
if letters:
    out += ["## Yesterday's letter", "", letters[-1].read_text(encoding="utf-8", errors="replace").strip(), ""]
recent_dates = sorted({d for v in days.values() for d in v})[-3:]
lately = sorted((k for k, v in days.items() if v & set(recent_dates)), key=lambda k: max(days[k]), reverse=True)[:8]
if lately: out += ["## Touched lately", ""] + [item(k) for k in lately] + [""]
most = [k for k in sorted(days, key=lambda k: len(days[k]), reverse=True) if len(days[k]) > 1][:4]
if most: out += ["## Returned to most", ""] + [item(k) + f" ({len(days[k])} days)" for k in most] + [""]
if days:
    old = min(days, key=lambda k: max(days[k]))
    out += ["## Left alone longest", "", item(old) + f" (last touched {max(days[old])})", ""]
wait = [f"- `inbox/{p.name}`" for p in sorted((studio / "inbox").glob("*")) if p.is_file() and p.name != ".keep"]
wait += [f"- `requests/{p.name}`" for p in sorted((studio / "requests").glob("*")) if p.is_file() and p.name != ".keep"]
if wait: out += ["## Waiting", ""] + wait + [""]
(studio / "DESK.md").write_text("\n".join(out), encoding="utf-8")
print("desk", studio.name, len(lately), "lately,", len(wait), "waiting")
