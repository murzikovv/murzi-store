"""Generate LICENSE.txt + README.md for templates that don't have them, then
this is paired with a zip step. Run: python scripts/gen_product_docs.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# folder, product, category, blurb
ITEMS = [
    ("04-mobile-app", "Tempo", "Mobile app landing",
     "A calm focus-app landing with glassy phone mockups, a live session ring and clean feature cards."),
    ("05-agency", "Vellum", "Creative agency / studio",
     "A brutalist studio site: oversized expanded type, a running marquee and a monochrome work grid."),
    ("06-fintech", "Quanta", "Fintech / payments",
     "A trust-first payments landing with a multi-currency account card, an animated balance chart and feature blocks."),
    ("07-event", "Pulse 2026", "Conference / event",
     "A high-energy event page with a speaker lineup, a day schedule and three ticket tiers."),
    ("08-course", "Cohort", "Online course / education",
     "A warm editorial course landing with a six-week curriculum, an instructor section and enrollment plans."),
    ("09-podcast", "Frequency", "Podcast",
     "A podcast site with a player-style hero, an episode list, a listen-anywhere row and animated waveforms."),
    ("10-dashboard", "Atlas", "Analytics dashboard / SaaS",
     "An analytics SaaS landing with a real app-shell product mockup, KPIs, a growth chart and clean pricing."),
    ("11-restaurant", "Saffron", "Restaurant / hospitality",
     "A warm-dark restaurant site with full-bleed food and interior photography, a short menu, a gallery and reservations."),
    ("12-ecommerce", "Lumen", "eCommerce / single product",
     "A quiet-luxury single-product brand page: hero, ingredient grid, the ritual, reviews and a shop block."),
    ("13-real-estate", "The Marin", "Real estate / property listing",
     "An architectural property listing with a full-bleed home tour, a facts row, a gallery and a viewing CTA."),
]

LICENSE = '''murzi/store — Single Commercial License
Template: "{product}" ({category})

Copyright (c) 2026 murzi.studio. All rights reserved.

WHAT YOU MAY DO
- Use this template for ONE end product (your own or a single client's),
  including commercial projects.
- Modify the files freely to fit that product.
- Deploy and host the result anywhere, with no attribution required.

WHAT YOU MAY NOT DO
- Resell, redistribute, sublicense, or give away the template files
  themselves (the source), modified or not.
- Include the template in another template, theme, kit, or marketplace.
- Use one purchase across multiple unrelated end products.

The product is the website you build with this file, not the source file.

Need a multi-use or extended license? Contact murzi.studio.

Fonts are loaded from Google Fonts under their respective open licenses.
Placeholder imagery (picsum.photos) is for demo only; replace before launch.
'''

README = '''# {product} — {category} template

{blurb}

**Live demo:** open `index.html` in any browser.

## What you get
- **One self-contained `index.html`** — no build step, no framework, no npm install.
- **Zero dependencies** except Google Fonts.
- Distinctive type and a committed colour palette; edit the `:root` tokens to rebrand.
- Reveal-on-scroll motion that respects `prefers-reduced-motion`, responsive at 375 / 768 / 1280px,
  semantic HTML and accessible contrast.

## Rebrand in minutes
1. **Colours** — edit the `:root` custom properties at the top of `<style>`.
2. **Fonts** — swap the Google Fonts `<link>` and the `--display` / `--body` variables.
3. **Copy & images** — replace the placeholder text and the `picsum.photos` image URLs.

## License
Single commercial license: use for **one** end product, modify freely, do not resell the source.
See `LICENSE.txt`. Extended licenses available on request.

---
Designed and built by **[murzi.studio](https://murzi.studio)**.
'''

for folder, product, category, blurb in ITEMS:
    d = ROOT / "templates" / folder
    (d / "LICENSE.txt").write_text(LICENSE.format(product=product, category=category), encoding="utf-8")
    (d / "README.md").write_text(README.format(product=product, category=category, blurb=blurb), encoding="utf-8")
    print(f"docs for {folder}")
print("done")
