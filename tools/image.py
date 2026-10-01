"""Make a picture with an image model (Cloudflare Workers AI, free daily allowance shared by every studio).
usage: python image.py "<prompt>" out.png [--model flux-1-schnell|flux-2-klein-4b|sdxl-lightning|dreamshaper] [--seed N] [--steps N]
Reads CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN from the environment. Prints the model, seed and file. Never prints credentials."""
import sys, os, json, base64, random, ssl, urllib.request, urllib.error
try:
    import certifi; CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    CTX = ssl.create_default_context()

MODELS = {"flux-1-schnell": "@cf/black-forest-labs/flux-1-schnell", "flux-2-klein-4b": "@cf/black-forest-labs/flux-2-klein-4b",
          "sdxl-lightning": "@cf/bytedance/stable-diffusion-xl-lightning", "dreamshaper": "@cf/lykon/dreamshaper-8-lcm"}
args = sys.argv[1:]
def opt(name, default=None):
    return args[args.index(name) + 1] if name in args else default
if len(args) < 2 or args[0].startswith("--"): sys.exit(__doc__)
prompt, out = args[0], args[1]
name = opt("--model", "flux-1-schnell"); model = MODELS.get(name, name)
seed = int(opt("--seed") or random.randint(0, 2**31 - 1))
acct, token = os.environ.get("CLOUDFLARE_ACCOUNT_ID"), os.environ.get("CLOUDFLARE_API_TOKEN")
if not acct or not token: sys.exit("No image model is reachable from here right now (credentials missing). Write it in requests/ if you need it.")

def call(body, multipart=False):
    url = f"https://api.cloudflare.com/client/v4/accounts/{acct}/ai/run/{model}"
    headers = {"Authorization": f"Bearer {token}", "User-Agent": "orchestrator2/0.1"}
    if multipart:
        b = "----o2" + str(random.randint(10**8, 10**9))
        data = "".join(f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n' for k, v in body.items()) + f"--{b}--\r\n"
        data = data.encode(); headers["Content-Type"] = f"multipart/form-data; boundary={b}"
    else:
        data = json.dumps(body).encode(); headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=180, context=CTX) as r:
        return r.headers.get("Content-Type", ""), r.read()

try:
    if "flux-2" in model:
        ctype, raw = call({"prompt": prompt, "seed": seed, "width": 1024, "height": 1024}, multipart=True)
    else:
        body = {"prompt": prompt}
        if "schnell" in model:
            body["steps"] = int(opt("--steps", 4)); seed = None
        else:
            body["seed"] = seed
            if opt("--steps"): body["num_steps"] = int(opt("--steps"))
        ctype, raw = call(body)
except urllib.error.HTTPError as e:
    msg = e.read().decode("utf-8", "replace")[:400]
    sys.exit(f"The image model refused or failed ({e.code}): {msg.replace(token, '***')}")

if "json" in ctype:
    d = json.loads(raw); img = (d.get("result") or {}).get("image") or d.get("image")
    if not img: sys.exit("No image came back: " + json.dumps(d)[:300])
    raw = base64.b64decode(img)
open(out, "wb").write(raw)
print(f"model: {name}  seed: {seed if seed is not None else 'not settable'}  file: {out}  ({len(raw)//1024} KB). Open it to see what came back.")
