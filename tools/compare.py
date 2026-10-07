"""Build a blind comparison: each studio's public/ (at HEAD or a given commit) copied into a lettered folder, letters shuffled.
usage: python tools/compare.py <out_dir> <id>[@commit] ...   writes <out_dir>/<letter>/, <out_dir>/key.json, prints the folder list for COMPARE-READER-PROMPT.md"""
import sys, json, random, string, subprocess, pathlib, io, tarfile
root = pathlib.Path(__file__).resolve().parent.parent
out = pathlib.Path(sys.argv[1]).resolve()
specs = sys.argv[2:]
letters = list(string.ascii_uppercase[:len(specs)])
random.shuffle(letters)
key = {}
for spec, letter in zip(specs, letters):
    aid, _, rev = spec.partition("@")
    studio = root.parent / "studios" / aid
    tar = subprocess.run(["git", "-C", str(studio), "archive", "--format=tar", rev or "HEAD", "public"], capture_output=True, check=True).stdout
    dest = out / letter
    dest.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(tar)) as t:
        for m in t.getmembers():
            if m.isfile():
                p = dest / pathlib.Path(m.name).relative_to("public")
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(t.extractfile(m).read())
    key[letter] = spec
(out / "key.json").write_text(json.dumps(dict(sorted(key.items())), indent=1))
print("\n".join(f"- {l}: {out / l}" for l in sorted(key)))
