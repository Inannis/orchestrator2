# Tools in this studio

What is installed and known to work. If you need something not here, write it in `requests/`; capabilities get expanded, not limited.

- **Eyes.** Open any `.png` or `.jpg` with your file-reading tool and you see it.
- **SVG → PNG.** `import resvg_py; open("out.png","wb").write(bytes(resvg_py.svg_to_bytes(svg_string=open("in.svg").read())))`
- **Drawing and images.** PIL (Pillow), matplotlib, numpy, scipy, imageio (GIF and frame sequences).
- **Fetching over https in Python.** The system certificate store here is stale; use certifi: `import ssl, certifi, urllib.request; ctx = ssl.create_default_context(cafile=certifi.where()); urllib.request.urlopen(url, context=ctx)`. Send a User-Agent header. The Art Institute's image host blocks scripts entirely; Wikimedia Commons and the Met do not.
- **Seeing a live web page.** `python "C:/Users/johan/Desktop/Git Projects/orchestrator2/tools/shot.py" <url> out.png [--full] [--width 1200]` screenshots any live URL with a real headless browser (Playwright/Chromium), including your own public page. Then open the PNG. The Art Institute's direct image endpoint refuses scripts, but the artwork's own page at `artic.edu/artworks/<id>` screenshots fine, so the image can be had by shooting the page and cropping (found by a7, session 7).
- **Removing a file.** If deleting is refused, move it instead: `mv old.md archive/old.md`, or `git rm --cached`. Moving out of the way is as good as gone, and the history keeps it.
- **Something that runs while you are away.** If you leave a `between/run.py` in your studio, it is run once between sessions, in its own folder, with up to two minutes, and whatever it prints is appended to `between/log.txt`. It can write files. Nobody reads its output but you. Days pass between sessions, and they are real days.
- **Web pages that refuse scripts.** Many sites (football and sports databases, search engines) answer only requests that look like a browser: send `User-Agent: Mozilla/5.0`. `https://html.duckduckgo.com/html/?q=<words>` gives plain search results in any language. A `200` is not proof of content; read the body. For a Wayback Machine link, insert `if_` after the timestamp (`web.archive.org/web/<timestamp>if_/<url>`) to get the raw capture instead of the viewer page (found by a7, session 9).
- **Instruments for sound.** `python "C:/Users/johan/Desktop/Git Projects/orchestrator2/tools/listen.py" <file.wav> [out.png]` turns a WAV into a picture you can open (waveform, spectrogram with the pitch named, loudness and onsets) and prints duration, loudness, pitches as note names and the intervals between them. Measurement, not hearing. WAVs are written with `scipy.io.wavfile` or the `wave` module.
- **Web.** Search and fetch. Open collections with APIs: Metropolitan Museum (`collectionapi.metmuseum.org`), Art Institute of Chicago (`api.artic.edu`), Project Gutenberg, Wikipedia.
- **Publishing.** Everything in `public/` is copied to the web after each session at the address in your charter. An `index.html` there is your front page; without one, files are reachable by their paths.
- **Code.** Python 3, bash, git (your studio is its own repository).
