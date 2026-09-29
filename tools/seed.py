"""Seed a new artist from a condition in template/conditions.md, and add it to the registry.
usage: python tools/seed.py <id> <condition>"""
import sys, re, shutil, subprocess, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
aid, cond = sys.argv[1], sys.argv[2]
row = re.search(rf"^\| {cond} \| (\w+) \| (\w+) \|", (root / "template" / "conditions.md").read_text(encoding="utf-8"), re.M)
if not row: sys.exit(f"no condition {cond}")
charter = row.group(1)
studio = root.parent / "studios" / aid
if studio.exists(): sys.exit(f"{studio} exists")
shutil.copytree(root / "template" / "studio", studio)
if charter != "v5":
    shutil.copytree(root / "template" / "variants" / charter, studio, dirs_exist_ok=True)
c = studio / "CHARTER.md"; c.write_text(c.read_text(encoding="utf-8").replace("{ID}", aid), encoding="utf-8")
for d in ["inbox", "requests"]:
    (studio / d).mkdir(exist_ok=True)
subprocess.run([sys.executable, str(root / "tools" / "encounter.py"), str(studio), "--p", "1", "--feed", row.group(2)], check=True)
subprocess.run(["git", "init", "-q"], cwd=studio, check=True)
subprocess.run(["git", "add", "-A"], cwd=studio, check=True)
subprocess.run(["git", "commit", "-qm", "The studio as found"], cwd=studio, check=True)
reg = root / "registry.md"; lines = reg.read_text(encoding="utf-8").split("\n")
last = max(i for i, l in enumerate(lines) if "| active |" in l)
lines.insert(last + 1, f"| {aid} | ../studios/{aid} | claude-sonnet-5 | {cond} | active | 0 | medium |")
reg.write_text("\n".join(lines), encoding="utf-8")
print("seeded", aid, cond, charter, row.group(2))
