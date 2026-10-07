"""Fork the reference: clone a studio at its current commit into a new id under a condition, and add it to the registry.
usage: python tools/fork.py <from-id> <new-id> <condition>
The clone keeps the whole history and session count; only the charter changes (to the condition's, with the new id),
plus the empty rooms a `rooms` condition furnishes. A note in inbox/ says the charter's studio paragraph has changed."""
import sys, re, shutil, subprocess, pathlib, datetime
root = pathlib.Path(__file__).resolve().parent.parent
src, aid, cond = sys.argv[1:4]
reg = root / "registry.md"; text = reg.read_text(encoding="utf-8")
srow = re.search(rf"^\| {src} \| [^|]+ \| ([\w.-]+) \| \w+ \| [^|]+ \| (\d+) \|", text, re.M)
row = re.search(rf"^\| {cond} \| ([\w-]+) \| [\w-]+ \| \w+ \| (\w+) \|", (root / "template" / "conditions.md").read_text(encoding="utf-8"), re.M)
if not (srow and row): sys.exit("unknown artist or condition")
studio = root.parent / "studios" / aid
subprocess.run(["git", "clone", "-q", str(root.parent / "studios" / src), str(studio)], check=True)
subprocess.run(["git", "-C", str(studio), "remote", "remove", "origin"], check=True)
charter, memory = row.group(1), row.group(2)
base = root / "template" / ("studio" if charter == "v5" else f"variants/{charter}") / "CHARTER.md"
(studio / "CHARTER.md").write_text(base.read_text(encoding="utf-8").replace("{ID}", aid), encoding="utf-8")
if memory == "rooms":
    for d in ["days", "found", "projects/active", "projects/resting", "projects/done", "projects/left"]:
        (studio / d).mkdir(parents=True, exist_ok=True); (studio / d / ".keep").touch()
if memory in ("desk", "deskw"):
    for d in ["days", "works"]:
        (studio / d).mkdir(parents=True, exist_ok=True); (studio / d / ".keep").touch()
if charter != "v5":
    (studio / "inbox" / f"note-{datetime.date.today()}-charter.md").write_text(
        "The part of your charter about how the studio is kept has changed. Everything you made and wrote is where you left it.\n", encoding="utf-8")
subprocess.run(["git", "-C", str(studio), "add", "-A"], check=True)
subprocess.run(["git", "-C", str(studio), "commit", "-qm", f"Forked from {src} under condition {cond}"], check=True)
lines = text.split("\n"); last = max(i for i, l in enumerate(lines) if re.match(r"\| a\d+ \| \.\./studios/", l))
lines.insert(last + 1, f"| {aid} | ../studios/{aid} | {srow.group(1)} | {cond} | active | {srow.group(2)} | medium |")
reg.write_text("\n".join(lines), encoding="utf-8")
print("forked", src, "->", aid, cond, "at session", srow.group(2))
