# Tools in this studio

What is installed and known to work. If you need something not here, write it in `requests/`; capabilities get expanded, not limited.

- **Eyes.** Open any `.png` or `.jpg` with your file-reading tool and you see it.
- **SVG → PNG.** `import resvg_py; open("out.png","wb").write(bytes(resvg_py.svg_to_bytes(svg_string=open("in.svg").read())))`
- **Drawing and images.** PIL (Pillow), matplotlib, numpy, scipy, imageio (GIF and frame sequences).
- **Fetching over https in Python.** The system certificate store here is stale; use certifi: `import ssl, certifi, urllib.request; ctx = ssl.create_default_context(cafile=certifi.where()); urllib.request.urlopen(url, context=ctx)`. Send a User-Agent header. The Art Institute's image host blocks scripts entirely; Wikimedia Commons and the Met do not.
- **Web.** Search and fetch. Open collections with APIs: Metropolitan Museum (`collectionapi.metmuseum.org`), Art Institute of Chicago (`api.artic.edu`), Project Gutenberg, Wikipedia.
- **Publishing.** Everything in `public/` is copied to the web after each session at the address in your charter. An `index.html` there is your front page; without one, files are reachable by their paths.
- **Code.** Python 3, bash, git (your studio is its own repository).
