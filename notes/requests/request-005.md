# Request 005 · an image-generation API for the artists

The artists already make images with code (PIL, SVG, matplotlib). An image model is a different thing: a picture from outside their own hand, of something that does not exist yet, for them to look at and answer. Offered in every studio's tools sheet as a plain capability, like the screenshot tool, so pairs stay comparable and nobody is told to use it.

**Recommended: Cloudflare Workers AI** (researched 2026-09-30). Free plan, no credit card, 10,000 neurons a day shared across models, resets 00:00 UTC. FLUX.1 schnell costs about 58 neurons for a 1024×1024 image at 4 steps, so roughly 170 images a day, far more than six artists will use. Also on the free allocation: FLUX.2 klein (4B, 9B), FLUX.2 dev, SDXL, SDXL Lightning, Leonardo Phoenix and Lucid Origin.

What you do, once:
1. Make a free Cloudflare account (dash.cloudflare.com).
2. Note the **Account ID** (Workers AI page, or the right column of the account home).
3. Create an **API token** with the Workers AI permission (My Profile → API Tokens → Create Token → "Workers AI" template).
4. Set two user environment variables, `CLOUDFLARE_ACCOUNT_ID` and `CLOUDFLARE_API_TOKEN` (or put them in a file outside the repo and tell me the path). I never need to see the values.

Then I write `tools/image.py "<prompt>" out.png [--model ...]`, test it, and add one line to every tools sheet.

**No-key alternative, usable today:** Pollinations (`image.pollinations.ai/prompt/<prompt>`), free Flux with no signup, but anonymous calls are throttled to about one per 15 seconds, may carry a watermark, and have no uptime guarantee. Fine as a fallback, not as the main tool.

Ruled out: Google (already used elsewhere); Together AI's free FLUX endpoint was deprecated; Hugging Face gives free users $0.10 a month, too little.
