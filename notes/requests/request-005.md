# Request 005 · an image-generation API for the artists

Every practice here makes its images with code (PIL, SVG, matplotlib) and most of its work in prose. Form and aesthetic language are the thinnest parts of the practice definition after desire. An image model is the largest capability change available: it would let an artist make a picture of something that does not exist yet, look at it, and make another.

What I need: an API key for one image-generation model, and a monthly spend cap you are comfortable with. Any of these would do; pick by price or preference: OpenAI `gpt-image-1`, Google Imagen via the Gemini API, Black Forest Labs FLUX, Stability. Put the key in an environment variable (for example `IMAGE_API_KEY`) or a file outside the repo, and tell me which. I will write a small wrapper in `tools/`, offer it in the tools sheet as a capability, and test it on one pair first as a hypothesis, not on everyone.

Not urgent; nothing waits on it. If you would rather not spend on it, say so and I will close this.
