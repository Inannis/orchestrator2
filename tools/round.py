"""Run tools/between.py once, then a working day for several artists, three at a time, each through tools/day.py.
usage: python tools/round.py a9 a10 a11 [...]   (no ids: every active artist in registry.md)"""
import sys, re, subprocess, pathlib
from concurrent.futures import ThreadPoolExecutor
root = pathlib.Path(__file__).resolve().parent.parent
ids = sys.argv[1:] or re.findall(r"^\| (a\d+) \|.*\| active \|", (root / "registry.md").read_text(encoding="utf-8"), re.M)
def day(i):
    r = subprocess.run([sys.executable, str(root / "tools" / "day.py"), i], capture_output=True, text=True, encoding="utf-8")
    return i, (r.stdout.strip().splitlines() or [r.stderr.strip()[-300:]])[-1]
# what runs while they are away runs once before the round, so a studio's between/run.py sees the real gap
print(subprocess.run([sys.executable, str(root / "tools" / "between.py")], capture_output=True, text=True).stdout.strip() or "between: nothing to run", flush=True)
with ThreadPoolExecutor(3) as ex:
    for i, res in ex.map(day, ids):
        print(i, res, flush=True)
