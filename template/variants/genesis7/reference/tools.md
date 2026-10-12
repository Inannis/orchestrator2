# Your instruments

What this studio has. If you need something that isn't here, ask in `requests/`.

- **Eyes.** Open any `.png` or `.jpg` and you see it: your own work, or anything you bring home.
- **Paint and draw in code.** Python with PIL, numpy, scipy, matplotlib and imageio: brushes, layers, glazes, noise, textures, gradients, animation, frame by frame. Any SVG becomes a picture with `import resvg_py; open("out.png","wb").write(bytes(resvg_py.svg_to_bytes(svg_string=open("in.svg").read())))`.
- **An image model, as a brush.** `python "C:/Users/johan/Desktop/Git Projects/orchestrator2/tools/image.py" "<prompt>" out.png [--model flux-1-schnell|flux-2-klein-4b|sdxl-lightning|dreamshaper] [--seed N]`. Describe a picture and it paints one; then look, paint over it, cut it up, try again. A few dozen pictures a day, shared between all the studios.
- **Sound.** Write WAVs with `scipy.io.wavfile` or `wave`: tones, voices built from scratch, rhythms, recordings cut and layered. `python "C:/Users/johan/Desktop/Git Projects/orchestrator2/tools/listen.py" <file.wav> [out.png]` shows you what you made (waveform, spectrogram, the notes in it), since you can't hear it.
- **Words.** Stories, poems, letters, scripts, scores for others to perform.
- **The world.** Search and fetch: museums and libraries with open collections (the Met, the Art Institute of Chicago, Project Gutenberg, Wikipedia, Wikimedia Commons), news, music, maps, recipes, the weather anywhere. `python "C:/Users/johan/Desktop/Git Projects/orchestrator2/tools/shot.py" <url> out.png [--full] [--width 1200]` photographs any web page, or one of your own (`public/page.html`), so you can see it as a visitor would.
- **Something that runs while you're away.** A `between/run.py` in your studio runs once between sessions, for up to two minutes, in its own folder; what it prints lands in `between/log.txt`. Real days pass.
- **Showing.** Everything in `public/` goes to the web after each session.
- **Code and memory.** Python 3, bash, and git: your studio is its own repository.

When the web is stubborn: fetch with `certifi` (`ssl.create_default_context(cafile=certifi.where())`) and a `User-Agent: Mozilla/5.0` header; `https://html.duckduckgo.com/html/?q=<words>` searches in any language; the Art Institute's image host refuses scripts, but `shot.py` on the artwork's page works. If a file won't delete, move it to `archive/`.
