from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
ITEMS = [
    ("resume-modern",  "Resume — Modern",  "a two-column modern resume with a sidebar, skill bars and a timeline"),
    ("resume-classic", "Resume — Classic", "a clean, single-column, ATS-friendly resume"),
    ("resume-bold",    "Resume — Bold",    "a confident resume with a colour banner and a two-column body"),
]
LICENSE = '''murzi/store — Single Commercial License
Template: "{product}" (Resume / CV)

Copyright (c) 2026 murzi.studio. All rights reserved.

You may use this template to create your OWN resume (or one client's),
edit it freely and print/export it as a PDF for any job application.

You may NOT resell, redistribute or include the template file itself in
any pack or marketplace. The product is your finished resume, not the source.

Fonts load from Google Fonts under their open licenses.
'''
README = '''# {product}

{blurb}. One HTML file, A4, print-ready.

## How to use
1. Open `index.html` in any browser (Chrome recommended).
2. Edit the text directly in the file (open it in any text editor) — name,
   contact, experience, skills. Everything is plain HTML.
3. Print to PDF: **File → Print** (or Ctrl/Cmd + P) →
   Destination **Save as PDF**, Margins **Default/None**, **Background graphics ON**.
4. You now have a pixel-perfect, recruiter-ready PDF.

## Rebrand
Change one line — the `--accent` colour in the `:root` block at the top of the
`<style>` — to recolour the whole resume.

## License
Single-use commercial license, see `LICENSE.txt`.

---
Designed by **[murzi.studio](https://murzi.studio)**.
'''
for folder, product, blurb in ITEMS:
    d = ROOT / "templates" / folder
    (d / "LICENSE.txt").write_text(LICENSE.format(product=product), encoding="utf-8")
    (d / "README.md").write_text(README.format(product=product, blurb=blurb), encoding="utf-8")
    print("docs", folder)
print("done")
