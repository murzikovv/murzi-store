#!/usr/bin/env python3
"""Generate vertical Pinterest pins (1000x1500 @2x) for murzi/store products.
Each pin embeds the product preview in a browser frame on the brand palette.
Run:  python marketing/pinterest/build_pins.py
"""
import base64, os, pathlib, sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "marketing" / "pinterest"
OUT.mkdir(parents=True, exist_ok=True)

# slug, preview file, tag, headline (HTML), benefit line, price label
PINS = [
    ("store", "beacon.png", "The store",
     "Website templates<br>that don't look<br><em>like templates</em>",
     "16 hand-built, one-file websites. Open, edit the text, ship in minutes.", "from ★ 490"),
    ("clinic", "clinic.png", "Clinic · medical",
     "A clinic site that<br><em>books consultations</em>",
     "For aesthetic, surgery & dental clinics. Treatments, doctors, booking form.", "★ 790"),
    ("fitness", "fitness.png", "Fitness · gym",
     "A gym site built<br>to <em>fill classes</em>",
     "Cinematic hero, real weekly schedule, memberships, free-trial CTA.", "★ 690"),
    ("home-services", "home-services.png", "Home services",
     "Win more jobs<br>with <em>one page</em>",
     "For plumbers, electricians & remodelers. Quote form + sticky call bar.", "★ 690"),
    ("tracker", "tracker.png", "Budget tracker",
     "Your whole budget<br>in <em>one Excel file</em>",
     "Type income & expenses — the dashboard and charts update themselves.", "★ 490"),
    ("pitch-deck", "pitch-deck.png", "Pitch deck",
     "A seed deck<br>investors <em>take seriously</em>",
     "12 editable PowerPoint slides. Problem, market, traction, the ask.", "★ 590"),
]

def b64(path):
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode()

TPL = """<!doctype html><html><head><meta charset=utf-8>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
<style>
  *{{margin:0;box-sizing:border-box}}
  :root{{--bg:#0c0e12;--bg2:#14171d;--ink:#f3f5f7;--soft:#9aa3b2;--lime:#c6f23a;--limeink:#1a2406}}
  html,body{{width:1000px;height:1500px}}
  body{{background:radial-gradient(120% 80% at 80% -10%, #1a2412 0%, var(--bg) 55%);color:var(--ink);
    font-family:'Space Grotesk',sans-serif;padding:70px 64px;display:flex;flex-direction:column;overflow:hidden}}
  .top{{display:flex;align-items:center;justify-content:space-between}}
  .logo{{font-weight:700;font-size:30px;letter-spacing:-.01em}}
  .logo b{{color:var(--lime)}}
  .tag{{font-family:'JetBrains Mono',monospace;font-size:18px;letter-spacing:.12em;text-transform:uppercase;
    color:var(--lime);border:1px solid rgba(198,242,58,.4);border-radius:99px;padding:9px 18px}}
  h1{{font-size:78px;line-height:1.0;font-weight:700;letter-spacing:-.02em;margin-top:54px}}
  h1 em{{font-style:normal;color:var(--lime)}}
  .benefit{{color:var(--soft);font-size:27px;line-height:1.4;margin-top:26px;max-width:24ch}}
  .frame{{margin-top:auto;background:var(--bg2);border:1px solid rgba(255,255,255,.1);border-radius:18px 18px 0 0;
    box-shadow:0 -10px 80px -30px rgba(198,242,58,.35);overflow:hidden;transform:rotate(-1.4deg);margin-bottom:-2px}}
  .bar{{display:flex;gap:9px;padding:16px 18px;background:#0f1318;border-bottom:1px solid rgba(255,255,255,.07)}}
  .bar i{{width:13px;height:13px;border-radius:50%;background:#2c323c;display:block}}
  .frame img{{width:100%;display:block}}
  .foot{{position:absolute;left:64px;right:64px;bottom:48px;display:flex;align-items:center;justify-content:space-between;z-index:2}}
  .price{{font-weight:700;font-size:30px}}
  .cta{{font-family:'JetBrains Mono',monospace;font-size:20px;color:var(--bg);background:var(--lime);
    padding:14px 26px;border-radius:99px;font-weight:500}}
  .glow{{position:absolute;inset:0;background:linear-gradient(180deg,transparent 60%,var(--bg) 96%);z-index:1;pointer-events:none}}
</style></head><body>
  <div class="top"><div class="logo">murzi<b>/</b></div><div class="tag">{tag}</div></div>
  <h1>{headline}</h1>
  <div class="benefit">{benefit}</div>
  <div class="frame"><div class="bar"><i></i><i></i><i></i></div><img src="{img}"></div>
  <div class="glow"></div>
  <div class="foot"><div class="price">{price}</div><div class="cta">murzi.studio →</div></div>
</body></html>"""

def main():
    prev = ROOT / "previews"
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        pg = b.new_page(viewport={"width":1000,"height":1500}, device_scale_factor=2)
        for slug, img, tag, head, ben, price in PINS:
            src = prev / img
            if not src.exists():
                print("skip (no preview):", img); continue
            html = TPL.format(tag=tag, headline=head, benefit=ben, price=price, img=b64(src))
            pg.set_content(html, wait_until="load")
            pg.wait_for_timeout(700)
            out = OUT / f"pin-{slug}.png"
            pg.screenshot(path=str(out))
            print("wrote", out.name)
        b.close()

if __name__ == "__main__":
    main()
