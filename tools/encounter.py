"""Deliver one unbidden encounter to an artist's inbox. Sources are public and picked at random; the orchestrator never chooses content.
usage: python tools/encounter.py <studio-path> [--p 0.5]  (nothing delivered with probability 1-p)"""
import sys, json, random, re, ssl, urllib.request, datetime, pathlib
try:
    import certifi; CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    CTX = ssl.create_default_context()
UA = {"User-Agent": "orchestrator2/0.1 (art project)"}
def get(url, binary=False):
    r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30, context=CTX).read()
    return r if binary else r.decode("utf-8", "replace")

def met(inbox, stamp):
    ids = json.loads(get("https://collectionapi.metmuseum.org/public/collection/v1/search?hasImages=true&isPublicDomain=true&q=a"))["objectIDs"]
    for _ in range(8):
        o = json.loads(get(f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{random.choice(ids)}"))
        if o.get("primaryImageSmall"): break
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
    members = [m["title"] for m in d["query"]["categorymembers"]]
    if not members: return None
    t = random.choice(members)
    sm = json.loads(get("https://en.wikipedia.org/api/rest_v1/page/summary/" + urllib.request.quote(t.replace(" ", "_"))))
    label = cat.replace('Category:', '').replace('_', ' ')
    return (f"An artist working now (or recently), picked at random from Wikipedia's {label}.\n\n"
            f"Name: {sm.get('title')}\nURL: {sm.get('content_urls',{}).get('desktop',{}).get('page')}\n\n{sm.get('extract')}\n")

def wikipedia(inbox, stamp):
    d = json.loads(get("https://en.wikipedia.org/api/rest_v1/page/random/summary"))
    return f"A random Wikipedia article.\n\nTitle: {d.get('title')}\nURL: {d.get('content_urls',{}).get('desktop',{}).get('page')}\n\n{d.get('extract')}\n"

def main():
    aid = sys.argv[1]; p = float(sys.argv[sys.argv.index("--p")+1]) if "--p" in sys.argv else 0.5
    if random.random() > p: print("nothing today"); return
    inbox = pathlib.Path(aid) / "inbox"; inbox.mkdir(exist_ok=True)
    stamp = datetime.date.today().isoformat() + "-" + "".join(random.choices("abcdefghjkmnpqrstuvwxyz", k=3))
    for src in random.sample([met, artic, gutenberg, wikipedia, living_artist, living_artist], 6):
        try:
            body = src(inbox, stamp)
        except Exception as e:
            body = None; print("skip", src.__name__, e)
        if body: break
    else: print("no source available"); return
    (inbox / f"encounter-{stamp}.md").write_text("From: the world, at random. Nobody chose this for you. Nothing is expected.\n\n" + body, encoding="utf-8")
    print("delivered", stamp, src.__name__)
main()
