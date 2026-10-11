"""Wild input for a genesis day: N random things from every source the studios know, into genesis/wild/.
usage (from inside the studio): python tools/wander.py [N]   (default 12)
Each draw picks a source at random (a picture, a sound, a passage, a living thing, the weather, news, a saying, an object, a place, an artist)."""
import sys, random, pathlib, datetime, string
root = pathlib.Path(__file__).resolve().parent.parent
src = (root / "tools" / "encounter.py").read_text(encoding="utf-8").replace("\nmain()", "")
enc = {"__file__": str(root / "tools" / "encounter.py")}; exec(src, enc)
n = int(sys.argv[1]) if len(sys.argv) > 1 else 12
studio = pathlib.Path.cwd().resolve()
while not (studio / "CHARTER.md").exists() and studio.parent != studio: studio = studio.parent
out = studio / "genesis" / "wild"; out.mkdir(parents=True, exist_ok=True)
sources = [enc[f] for f in ["commons_photo", "current_event", "inaturalist", "gutenberg", "met", "commons_audio", "weather", "wikiquote", "wikipedia", "living_artist"]]
got = 0
for i in range(n * 3):
    if got >= n: break
    f = random.choice(sources)
    stamp = datetime.date.today().isoformat() + "-" + "".join(random.choices(string.ascii_lowercase, k=3))
    try: body = f(out, stamp)
    except Exception: body = None
    if not body: continue
    (out / f"encounter-{stamp}.md").write_text(body, encoding="utf-8"); got += 1
    print(f"{got:2d}. {body.splitlines()[0][:90]}  -> genesis/wild/encounter-{stamp}.md")
print(f"{got} things arrived in genesis/wild/.")
