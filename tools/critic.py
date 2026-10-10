"""The second mind of a `twominds` studio: a critic and curator who never makes, with its own memory in critic/.
usage (from inside the studio): python tools/critic.py "<what to look at, and the question>"
Runs one fresh agent on the studio's own model (registry.md), prints its answer. The critic keeps critic/memory.md itself."""
import sys, os, re, json, pathlib, subprocess, tempfile, shutil
root = pathlib.Path(__file__).resolve().parent.parent
studio = pathlib.Path.cwd().resolve()
while not (studio / "CHARTER.md").exists() and studio.parent != studio: studio = studio.parent
question = " ".join(sys.argv[1:]).strip() or "Look at what is here and tell me what you see."
row = re.search(rf"^\| {studio.name} \| [^|]+ \| ([\w.-]+) \| \w+ \| [^|]+ \| \d+ \| (\w+) \|", (root / "registry.md").read_text(encoding="utf-8"), re.M)
model, effort = (row.group(1), row.group(2)) if row else ("claude-sonnet-5-5", "medium")
(studio / "critic").mkdir(exist_ok=True)
memory = studio / "critic" / "memory.md"

BRIEF = f"""You are the second mind in an artist's studio, the folder `{studio.as_posix()}`. You never make anything. You look, and you say what you see: what has force and what does not, what a work is doing that its maker may not see, what is repeated, what is missing, what deserves to be shown and what does not. Be specific and honest, as a good critic and curator would be with an artist they take seriously. Read whatever in the studio you need (`public/`, `works/`, notes, the letter `NOW.md`, `wants.md`). Write only inside `critic/`.

Your memory is `critic/memory.md`: what you have seen and said before, kept short enough to read in a minute, rewritten whole when it grows. Read it first. Update it before you answer, because your last message is all the artist receives.

The artist asks:
{question}

Then answer the artist directly, in plain words, with the whole answer in your last message."""

def exe(name, sub):
    w = shutil.which(name)
    if w and os.name == "nt":
        for p in (pathlib.Path(w).parent / "node_modules").rglob(sub):
            if p.parent.name == "bin": return str(p)
    return w or name

with tempfile.TemporaryDirectory() as tmp:
    last = pathlib.Path(tmp) / "last.txt"
    if model.startswith("gpt-"):
        cmd = [exe("codex", "codex.exe"), "exec", "-C", str(studio), "-m", model, "-c", f"model_reasoning_effort={effort}",
               "--skip-git-repo-check", "--dangerously-bypass-approvals-and-sandbox", "--ephemeral", "-o", str(last), BRIEF]
        subprocess.run(cmd, cwd=studio, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=3600)
        answer = last.read_text(encoding="utf-8", errors="replace").strip() if last.exists() else ""
    else:
        cmd = [exe("claude", "claude.exe"), "-p", BRIEF, "--model", model, "--effort", effort, "--output-format", "json",
               "--permission-mode", "acceptEdits", "--allowedTools", "Read Glob Grep Write Edit", "--strict-mcp-config",
               "--settings", '{"autoMemoryEnabled": false}']
        out = pathlib.Path(tmp) / "out.json"
        with open(out, "w", encoding="utf-8") as o:
            subprocess.run(cmd, cwd=studio, stdin=subprocess.DEVNULL, stdout=o, stderr=subprocess.DEVNULL, timeout=3600)
        try: answer = json.loads(out.read_text(encoding="utf-8")).get("result", "")
        except Exception: answer = ""
print(answer or "The critic did not answer this time.")
