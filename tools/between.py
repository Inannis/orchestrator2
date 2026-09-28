"""Run each active studio's between/run.py once, if it has one. Output goes to the studio's between/log.
usage: python tools/between.py"""
import pathlib, re, subprocess, sys, datetime
root = pathlib.Path(__file__).resolve().parent.parent
ids = re.findall(r"^\| (a\d+) \| \.\./studios/\1 \|.*\| active \|", (root / "registry.md").read_text(encoding="utf-8"), re.M)
for i in ids:
    studio = root.parent / "studios" / i
    script = studio / "between" / "run.py"
    if not script.exists():
        continue
    stamp = datetime.datetime.now().isoformat(timespec="seconds")
    try:
        r = subprocess.run([sys.executable, "run.py"], cwd=script.parent, capture_output=True, text=True, timeout=120)
        out = (r.stdout or "") + (("\n[stderr]\n" + r.stderr) if r.stderr else "")
        status = f"exit {r.returncode}"
    except subprocess.TimeoutExpired:
        out, status = "", "timed out after 120s"
    log = script.parent / "log.txt"
    with log.open("a", encoding="utf-8") as f:
        f.write(f"--- {stamp} · {status}\n{out.rstrip()}\n")
    print(i, status)
