"""Lay out DESK.md in a studio with `desk` memory: yesterday's letter, works touched lately, works returned to most, the one left alone longest, what waits.
usage: python tools/desk.py <studio>   (run by day.py before each new day; the artist never writes the desk)
A work is a folder in works/ or, for loose files, everything sharing one name stem. Touches come from the studio's git history, counted in sessions (day.py ends each with an \"End of session\" commit)."""
import sys, re, subprocess, pathlib, collections
studio = pathlib.Path(sys.argv[1]).resolve()
works = studio / "works"

def key(rel):
    parts = rel.split("/")
    if len(parts) < 2 or parts[0] != "works": return None
    return parts[1] if len(parts) > 2 else re.sub(r"\..*$", "", parts[1])

log = subprocess.run(["git", "-C", str(studio), "log", "--name-only", "--format=@%s"], capture_output=True, text=True, encoding="utf-8").stdout
# sessions are counted newest first; one "End of session" commit closes each; older history (before day.py committed) counts commit by commit
touched = collections.defaultdict(set); session = 0; ends = 0
for line in log.splitlines():
    if line.startswith("@"):
        if line.startswith("@End of session"): ends += 1; session = ends
        elif ends >= 3 or not log.count("@End of session"): session += 1
    elif line and (k := key(line)): touched[k].add(session)
alive = {k for k in touched if (works / k).is_dir() or any(works.glob(k + ".*"))}
touched = {k: v for k, v in touched.items() if k in alive}

def notes(k):
    d = works / k
    cands = sorted(works.glob(k + ".md")) + sorted(works.glob(k + ".txt")) + (sorted(d.glob("*.md")) if d.is_dir() else [])
    for c in cands:
        lines = [l.strip() for l in c.read_text(encoding="utf-8", errors="replace").splitlines() if l.strip() and not l.startswith("#")]
        if lines: return " ".join(lines[:3])[:300]
    return ""

def item(k): return f"- `works/{k}`" + (f": {notes(k)}" if notes(k) else "")

out = ["# Desk", "", "Laid out this morning from the studio. Nobody writes here; it is made again tomorrow.", ""]
letters = sorted((studio / "days").glob("*.md")) if (studio / "days").is_dir() else []
if letters:
    out += ["## Yesterday's letter", "", letters[-1].read_text(encoding="utf-8", errors="replace").strip(), ""]
lately = sorted((k for k, v in touched.items() if min(v) <= 3), key=lambda k: min(touched[k]))[:8]
if lately: out += ["## Touched lately", ""] + [item(k) for k in lately] + [""]
most = [k for k in sorted(touched, key=lambda k: len(touched[k]), reverse=True) if len(touched[k]) > 1][:4]
if most: out += ["## Returned to most", ""] + [item(k) + f" ({len(touched[k])} sessions)" for k in most] + [""]
if touched:
    old = max(touched, key=lambda k: min(touched[k]))
    out += ["## Left alone longest", "", item(old) + f" (untouched for {min(touched[old])} sessions)", ""]
wait = [f"- `inbox/{p.name}`" for p in sorted((studio / "inbox").glob("*")) if p.is_file() and p.name != ".keep"]
wait += [f"- `requests/{p.name}`" for p in sorted((studio / "requests").glob("*")) if p.is_file() and p.name != ".keep"]
if wait: out += ["## Waiting", ""] + wait + [""]
(studio / "DESK.md").write_text("\n".join(out), encoding="utf-8")
print("desk", studio.name, len(lately), "lately,", len(wait), "waiting")
