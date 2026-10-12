"""Deliver one unbidden encounter to an artist's inbox. Sources are public and picked at random; the orchestrator never chooses content.
usage: python tools/encounter.py <studio-path> [--p 0.5] [--feed museum|wide|objects|<feed>-bare]  (nothing delivered with probability 1-p; feed defaults to the studio's condition)
A `-bare` feed delivers the thing alone (the picture, the passage, the text), without title, source or metadata; a `-warm` feed tells it in a sentence, without catalogue fields. Every delivery's full record goes to runs/encounters.ndjson."""
import sys, json, random, re, ssl, urllib.request, datetime, pathlib
try:
    import certifi; CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    CTX = ssl.create_default_context()
UA = {"User-Agent": "orchestrator2/0.2 (art project; https://inannis.github.io/orchestrator2/)"}
def get(url, binary=False):
    url = urllib.request.quote(url, safe=":/?=&%#+,;@")
    r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30, context=CTX).read()
    return r if binary else r.decode("utf-8", "replace")

def met(inbox, stamp):
    # any object in the whole collection, every department alike; tried until one is public domain with an image
    ids = json.loads(get("https://collectionapi.metmuseum.org/public/collection/v1/objects"))["objectIDs"]
    for _ in range(25):
        try: o = json.loads(get(f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{random.choice(ids)}"))
        except Exception: continue
        if o.get("isPublicDomain") and o.get("primaryImageSmall"): break
    else: return None
    img = get(o["primaryImageSmall"], binary=True)
    (inbox / f"encounter-{stamp}.jpg").write_bytes(img)
    meta = {k: o.get(k) for k in ["title","artistDisplayName","objectDate","medium","dimensions","culture","department","classification","objectURL"] if o.get(k)}
    body = "\n".join(f"{k}: {v}" for k, v in meta.items())
    return f"An object, picked at random from the Metropolitan Museum's open collection. Image: `encounter-{stamp}.jpg`.\n\n{body}\n"

def gutenberg(inbox, stamp):
    for _ in range(8):
        i = random.randint(1, 70000)
        try: t = get(f"https://www.gutenberg.org/cache/epub/{i}/pg{i}.txt")
        except Exception: continue
        m = re.search(r"\*\*\* START OF.*?\*\*\*(.*?)\*\*\* END OF", t, re.S)
        if not m: continue
        body = m.group(1).strip()
        if len(body) < 3000: continue
        title = re.search(r"Title:\s*(.+)", t); author = re.search(r"Author:\s*(.+)", t)
        start = random.randint(0, max(0, len(body) - 2500))
        excerpt = body[start:start + 2500]
        (inbox / f"encounter-{stamp}-source.txt").write_text(body, encoding="utf-8")
        return (f"A passage, from a random page of a random Project Gutenberg text (#{i}). The whole text is in `encounter-{stamp}-source.txt`.\n\n"
                f"Title: {title.group(1).strip() if title else '?'}\nAuthor: {author.group(1).strip() if author else '?'}\n\n…{excerpt}…\n")
    return None

def artic(inbox, stamp):
    page = random.randint(1, 600)
    d = json.loads(get(f"https://api.artic.edu/api/v1/artworks/search?query[term][is_public_domain]=true&fields=id,title,artist_display,date_display,medium_display,image_id,classification_title,dimensions&limit=1&page={page}"))
    o = d["data"][0]
    imgline = "No image could be fetched from here; the URL below has it."
    if o.get("image_id"):
        try:
            img = get(f"https://www.artic.edu/iiif/2/{o['image_id']}/full/843,/0/default.jpg", binary=True)
            (inbox / f"encounter-{stamp}.jpg").write_bytes(img); imgline = f"Image: `encounter-{stamp}.jpg`."
        except Exception:
            pass
    meta = {k: o.get(k) for k in ["title","artist_display","date_display","medium_display","dimensions","classification_title"] if o.get(k)}
    body = "\n".join(f"{k}: {v}" for k, v in meta.items())
    return f"An artwork, picked at random from the Art Institute of Chicago's open collection. {imgline}\n\n{body}\nURL: https://www.artic.edu/artworks/{o['id']}\n"

def living_artist(inbox, stamp):
    cats = ["Category:21st-century_conceptual_artists","Category:21st-century_women_artists","Category:21st-century_sculptors","Category:21st-century_painters","Category:Installation_artists","Category:Performance_artists","Category:Sound_artists","Category:Video_artists","Category:21st-century_photographers","Category:Digital_artists","Category:Land_artists","Category:Textile_artists","Category:21st-century_poets"]
    cat = random.choice(cats)
    d = json.loads(get(f"https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle={cat}&cmlimit=500&cmnamespace=0&format=json"))
    members = [m["title"] for m in d["query"]["categorymembers"] if not m["title"].startswith(("List of", "Lists of", "Category:", "Template:"))]
    if not members: return None
    t = random.choice(members)
    sm = json.loads(get("https://en.wikipedia.org/api/rest_v1/page/summary/" + urllib.request.quote(t.replace(" ", "_"))))
    label = cat.replace('Category:', '').replace('_', ' ')
    return (f"An artist working now (or recently), picked at random from Wikipedia's {label}.\n\n"
            f"Name: {sm.get('title')}\nURL: {sm.get('content_urls',{}).get('desktop',{}).get('page')}\n\n{sm.get('extract')}\n")

def wikipedia(inbox, stamp):
    d = json.loads(get("https://en.wikipedia.org/api/rest_v1/page/random/summary"))
    return f"A random Wikipedia article.\n\nTitle: {d.get('title')}\nURL: {d.get('content_urls',{}).get('desktop',{}).get('page')}\n\n{d.get('extract')}\n"

def commons_photo(inbox, stamp):
    d = json.loads(get("https://commons.wikimedia.org/w/api.php?action=query&generator=random&grnnamespace=6&grnlimit=20&prop=imageinfo&iiprop=url|extmetadata|mime&iiurlwidth=1000&format=json"))
    for p in d["query"]["pages"].values():
        ii = p["imageinfo"][0]
        if ii["mime"] == "image/jpeg" and not re.search(r"DPLA|btv1b|pdf|page ?\d+|map|scan", p["title"], re.I): break
    else: return None
    (inbox / f"encounter-{stamp}.jpg").write_bytes(get(ii["thumburl"], binary=True))
    desc = re.sub(r"<[^>]+>", "", ii.get("extmetadata", {}).get("ImageDescription", {}).get("value", "")).strip()[:600]
    return f"A photograph, picked at random from Wikimedia Commons. Image: `encounter-{stamp}.jpg`.\n\n{p['title'][5:]}\n{desc}\n{ii['descriptionurl']}\n"

def current_event(inbox, stamp):
    day = datetime.date.today() - datetime.timedelta(days=random.randint(0, 2))
    t = f"Portal:Current_events/{day.year}_{day.strftime('%B')}_{day.day}"
    w = json.loads(get("https://en.wikipedia.org/w/api.php?action=parse&format=json&prop=wikitext&page=" + urllib.request.quote(t)))
    if "parse" not in w: return None
    items = [l.lstrip("*").strip() for l in w["parse"]["wikitext"]["*"].splitlines() if re.match(r"\*{2,}[^*]", l)]
    items = [i for i in items if len(i) > 80]
    if not items: return None
    i = random.choice(items)
    i = re.sub(r"\[https?://\S+ \(([^)]*)\)\]", r"(\1)", i)
    i = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", r"\1", i).replace("''", "")
    return f"Something that happened in the world this week, picked at random from Wikipedia's current events for {day.isoformat()}.\n\n{i}\n"

def inaturalist(inbox, stamp):
    o = json.loads(get(f"https://api.inaturalist.org/v1/observations?photos=true&quality_grade=research&per_page=1&order_by=observed_on&page={random.randint(1, 300)}"))
    r = o["results"][0]
    (inbox / f"encounter-{stamp}.jpg").write_bytes(get(r["photos"][0]["url"].replace("square", "large"), binary=True))
    tx = r.get("taxon") or {}
    return (f"A living thing, seen by someone this week and posted to iNaturalist, picked at random. Image: `encounter-{stamp}.jpg`.\n\n"
            f"{tx.get('preferred_common_name') or ''} ({tx.get('name')})\nSeen: {r.get('observed_on')}, {r.get('place_guess')}\nhttps://www.inaturalist.org/observations/{r['id']}\n")

def commons_audio(inbox, stamp):
    d = json.loads(get("https://commons.wikimedia.org/w/api.php?action=query&generator=random&grnnamespace=6&grnlimit=50&prop=imageinfo&iiprop=url|mime|extmetadata&format=json"))
    for p in d["query"]["pages"].values():
        ii = p["imageinfo"][0]
        if ii["mime"] in ("audio/ogg", "audio/mpeg", "audio/wav", "audio/x-wav", "audio/flac", "application/ogg"): break
    else: return None
    ext = pathlib.Path(ii["url"].split("?")[0]).suffix or ".ogg"
    (inbox / f"encounter-{stamp}{ext}").write_bytes(get(ii["url"], binary=True))
    desc = re.sub(r"<[^>]+>", "", ii.get("extmetadata", {}).get("ImageDescription", {}).get("value", "")).strip()[:500]
    return f"A sound, picked at random from Wikimedia Commons. File: `encounter-{stamp}{ext}`.\n\n{p['title'][5:]}\n{desc}\n{ii['descriptionurl']}\n"

def weather(inbox, stamp):
    places = json.loads(get("https://en.wikipedia.org/w/api.php?action=query&list=random&rnnamespace=0&rnlimit=20&format=json"))["query"]["random"]
    for pl in places:
        c = json.loads(get("https://en.wikipedia.org/w/api.php?action=query&prop=coordinates&format=json&titles=" + urllib.request.quote(pl["title"])))
        co = next(iter(c["query"]["pages"].values())).get("coordinates")
        if co: break
    else: return None
    lat, lon = co[0]["lat"], co[0]["lon"]
    w = json.loads(get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,precipitation,cloud_cover,wind_speed_10m,is_day&timezone=auto"))
    cur = w.get("current", {}); u = w.get("current_units", {})
    body = "\n".join(f"{k}: {v}{u.get(k, '')}" for k, v in cur.items() if k != "interval")
    return f"The weather right now somewhere, at a place picked at random from Wikipedia: {pl['title']} ({lat:.3f}, {lon:.3f}).\n\n{body}\n"

def wikiquote(inbox, stamp):
    for _ in range(6):
        t = json.loads(get("https://en.wikiquote.org/w/api.php?action=query&list=random&rnnamespace=0&rnlimit=1&format=json"))["query"]["random"][0]["title"]
        w = json.loads(get("https://en.wikiquote.org/w/api.php?action=parse&prop=wikitext&format=json&page=" + urllib.request.quote(t)))
        lines = [re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", r"\1", l[1:].strip()).replace("'''", "").replace("''", "")
                 for l in w.get("parse", {}).get("wikitext", {}).get("*", "").splitlines() if re.match(r"\*[^*:]", l)]
        lines = [l for l in lines if 40 < len(l) < 600 and not l.startswith(("{", "<"))]
        if lines: return f"Something someone said, picked at random from Wikiquote ({t}).\n\n{random.choice(lines)}\n"
    return None

FEEDS = {"museum": [met, artic, gutenberg, wikipedia, living_artist, living_artist],
         "world": [commons_photo, current_event, inaturalist, gutenberg, met, commons_audio, weather, wikiquote],
         "wide": [commons_photo, current_event, inaturalist, gutenberg, wikipedia, living_artist, met],
         "objects": [met, met, gutenberg]}

def bare(src, body, inbox, stamp):
    """The thing without its record: the picture, the passage, or the text alone. None if there is no thing."""
    if src in ("commons_photo", "inaturalist", "met", "artic"):
        return f"`encounter-{stamp}.jpg`\n" if (inbox / f"encounter-{stamp}.jpg").exists() else None
    if src == "gutenberg": return body[body.index("…"):] + f"\n(More of it: `encounter-{stamp}-source.txt`.)\n"
    return body.rstrip().split("\n\n")[-1] + "\n"

WARM_KEYS = ["title", "Title", "artistDisplayName", "artist_display", "objectDate", "date_display", "medium", "medium_display", "culture"]
def warm(body):
    """The thing told plainly: catalogue fields become one sentence, numbers and dimensions go, the link waits at the end."""
    out, kv, urls = [], {}, []
    for l in body.split("\n"):
        u = re.match(r"^(?:URL: )?(https?://\S+)$", l.strip())
        if u: urls.append(u.group(1)); continue
        m = re.match(r"^([A-Za-z_0-9]+): (.+)$", l)
        if m: kv[m.group(1)] = m.group(2); continue
        out.append(l)
    said = [kv[k] for k in WARM_KEYS if k in kv]
    rest = [f"{k.replace('_2m', '').replace('_10m', '').replace('_', ' ')} {v}" for k, v in kv.items() if k not in WARM_KEYS and k not in ("dimensions", "department", "classification", "classification_title", "objectURL", "time", "is_day")]
    text = "\n".join(out).rstrip()
    if said: text += "\n\n" + ", ".join(said) + "."
    if rest: text += "\n\n" + "; ".join(rest) + "."
    if urls: text += f"\n\nIf you want to find it again: {urls[0]}"
    return text.strip() + "\n"

def feed_of(studio):
    """The feed named by the studio's condition: registry.md row -> conditions.md row."""
    root = pathlib.Path(__file__).resolve().parent.parent
    sid = pathlib.Path(studio).resolve().name
    m = re.search(rf"^\| {sid} \|[^|]*\|[^|]*\| (\w+) \|", (root / "registry.md").read_text(encoding="utf-8"), re.M)
    if not m: return "museum"
    c = re.search(rf"^\| {m.group(1)} \|[^|]*\| ([\w-]+) \|", (root / "template" / "conditions.md").read_text(encoding="utf-8"), re.M)
    return c.group(1) if c else "museum"

def main():
    aid = sys.argv[1]; p = float(sys.argv[sys.argv.index("--p")+1]) if "--p" in sys.argv else 0.5
    if random.random() > p: print("nothing today"); return
    inbox = pathlib.Path(aid) / "inbox"; inbox.mkdir(exist_ok=True)
    stamp = datetime.date.today().isoformat() + "-" + "".join(random.choices("abcdefghjkmnpqrstuvwxyz", k=3))
    feed = sys.argv[sys.argv.index("--feed")+1] if "--feed" in sys.argv else feed_of(aid)
    is_warm = feed.endswith("-warm")
    base, is_bare = feed.removesuffix("-bare").removesuffix("-warm"), feed.endswith("-bare")
    for src in random.sample(FEEDS[base], len(FEEDS[base])):
        try:
            body = src(inbox, stamp)
        except Exception as e:
            body = None; print("skip", src.__name__, e)
        record = body
        if body and is_bare: body = bare(src.__name__, body, inbox, stamp)
        if body and is_warm: body = warm(body)
        if body: break
    else: print("no source available"); return
    log = pathlib.Path(__file__).resolve().parent.parent / "runs" / "encounters.ndjson"
    with open(log, "a", encoding="utf-8") as f:
        f.write(json.dumps({"studio": pathlib.Path(aid).resolve().name, "stamp": stamp, "feed": feed, "source": src.__name__, "record": record}) + "\n")
    head = "Something came today, from the world, by chance. Nobody chose it for you; do with it what you like, or nothing." if is_warm else "From: the world, at random. Nobody chose this for you. Nothing is expected."
    (inbox / f"encounter-{stamp}.md").write_text(head + "\n\n" + body, encoding="utf-8")
    print("delivered", stamp, feed, src.__name__)
main()
