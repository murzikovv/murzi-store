#!/usr/bin/env python3
"""Pinterest pins for murzi/store — showcase style (ref: Dribbble landing mockups).
The WHOLE landing page shown long, in a browser frame, on a soft pastel mat
tinted per product. Minimal caption. Site is the hero.
Run:  python marketing/pinterest/build_pins.py [slug]   (slug optional = one pin)
"""
import base64, pathlib, sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "marketing" / "pinterest"

# slug, template path, soft-bg, ink, accent, label, price, capHeight
PINS = [
 ("store","templates/01-ai-saas-landing/index.html","#eaf1e6","#1c2a16","#5a8a2a","AI / SaaS landing template","★ 690",2700),
 ("clinic","templates/15-clinic/index.html","#efe6d9","#3a3326","#9c7f48","Clinic · website template","★ 790",2700),
 ("fitness","templates/16-fitness/index.html","#eae7e2","#22201d","#e8500f","Fitness / gym template","★ 690",2700),
 ("salon","templates/17-salon/index.html","#f2e7df","#3a2e27","#a3624a","Hair & beauty salon template","★ 690",2700),
 ("wedding","templates/18-wedding/index.html","#e7ebe1","#34403a","#9c7f3e","Wedding invitation template","★ 690",2700),
 ("cafe","templates/19-cafe/index.html","#efe6d6","#2a211a","#9a5b2c","Coffee shop / café template","★ 690",2700),
 ("home-services","templates/14-home-services/index.html","#e6eefb","#14213d","#cf771c","Home services template","★ 690",2700),
 ("tracker","templates/tracker/preview.html","#e6eef9","#16315f","#1f7a4d","Budget tracker · Excel","★ 490",1500),
 ("pitch-deck","templates/pitch-deck/preview.html","#e7e9f6","#1a2450","#b08a3c","Investor pitch deck · PPTX","★ 590",1500),
]

PIN_TPL = """<!doctype html><html><head><meta charset=utf-8>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
<style>
 *{{margin:0;box-sizing:border-box}}
 body{{width:1000px;background:{bg};font-family:'Space Grotesk',sans-serif;padding:54px 64px 60px;color:{ink}}}
 .cap{{display:flex;align-items:center;justify-content:space-between;margin-bottom:30px}}
 .cap .l{{display:flex;align-items:baseline;gap:14px}}
 .cap .logo{{font-weight:700;font-size:30px}} .cap .logo b{{color:{accent}}}
 .cap .lbl{{font-family:'JetBrains Mono',monospace;font-size:18px;letter-spacing:.04em;opacity:.7}}
 .cap .price{{font-weight:700;font-size:26px;color:{accent}}}
 .win{{border-radius:16px;overflow:hidden;background:#fff;box-shadow:0 50px 90px -36px rgba(20,20,30,.42), 0 8px 24px -12px rgba(20,20,30,.25)}}
 .bar{{display:flex;align-items:center;gap:8px;padding:15px 18px;background:#f4f4f6;border-bottom:1px solid rgba(0,0,0,.06)}}
 .bar i{{width:13px;height:13px;border-radius:50%;background:#cdced6;display:block}}
 .bar .u{{margin-left:14px;flex:1;height:26px;border-radius:7px;background:#e6e6 ec;background:#e7e7ee;display:flex;align-items:center;padding:0 14px;font-family:'JetBrains Mono',monospace;font-size:14px;color:#9a9aa6}}
 .win img{{width:100%;display:block}}
 .foot{{margin-top:26px;text-align:center;font-family:'JetBrains Mono',monospace;font-size:19px;letter-spacing:.04em;color:{ink};opacity:.62}}
</style></head><body>
 <div class="cap"><div class="l"><div class="logo">murzi<b>/</b></div><div class="lbl">{label}</div></div><div class="price">{price}</div></div>
 <div class="win"><div class="bar"><i></i><i></i><i></i><div class="u">murzi.studio</div></div><img src="data:image/png;base64,{img}"></div>
 <div class="foot">one file · edit the text · ship in minutes — murzi.studio</div>
</body></html>"""

def build(b, slug, tpl, bg, ink, accent, label, price, capH):
    if slug in ("tracker", "pitch-deck"):
        shot = (ROOT / "previews" / f"{slug}.png").read_bytes()   # clean landscape crop
    else:
        url = (ROOT / tpl).resolve().as_uri()
        pg = b.new_page(viewport={"width":1240,"height":capH}, device_scale_factor=1.5)
        pg.goto(url, wait_until="load"); pg.wait_for_timeout(2800)
        pg.add_style_tag(content=".rv,.rv2{opacity:1!important;transform:none!important;clip-path:none!important}")
        pg.wait_for_timeout(400)
        shot = pg.screenshot(clip={"x":0,"y":0,"width":1240,"height":capH}); pg.close()
    html = PIN_TPL.format(bg=bg, ink=ink, accent=accent, label=label, price=price,
                          img=base64.b64encode(shot).decode())
    pin = b.new_page(viewport={"width":1000,"height":1500}, device_scale_factor=2)
    pin.set_content(html, wait_until="load"); pin.wait_for_timeout(700)
    h = int(pin.evaluate("document.body.scrollHeight"))
    pin.set_viewport_size({"width":1000,"height":h})
    pin.screenshot(path=str(OUT / f"pin-{slug}.png"), clip={"x":0,"y":0,"width":1000,"height":h}); pin.close()
    print("wrote pin-"+slug+".png")

def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        for row in PINS:
            if only and row[0] != only: continue
            build(b, *row)
        b.close()

if __name__ == "__main__":
    main()
