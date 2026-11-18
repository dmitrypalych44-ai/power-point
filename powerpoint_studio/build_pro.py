"""Build the compact «Стратегия ПРО — Владивосток 2027» deck (9 slides) in the brand style."""
from __future__ import annotations

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pymupdf

from powerpoint_studio.backends import PptxRenderer, PdfRenderer
from powerpoint_studio import pages_pro, finish, backdrop
from powerpoint_studio.components import house_mark

NAME = "Лемана_ПРО_Стратегия_ПРО_Владивосток_2027_сжатая"


def build(out_dir: str = "deliverables", png: bool = False):
    os.makedirs(out_dir, exist_ok=True)
    pages = [f() for f in pages_pro.PAGES]
    for i, p in enumerate(pages, start=1):
        p.number = i
        if i in (1, len(pages)):
            backdrop.paper(p)
        else:
            backdrop.prepare(p, i, len(pages))
            backdrop.frame(p, i, len(pages))
            house_mark(p)
    print("pages:", len(pages))

    pptx_path = os.path.join(out_dir, NAME + ".pptx")
    prs = PptxRenderer().build(pages).prs
    finish.set_props(prs, "Стратегия ПРО — Владивосток 2027 (сжатая версия)",
                     "Девять слайдов: рынок, потенциал, конкуренция, силы и риски, амбиция, изменения и KPI",
                     keywords="Лемана ПРО; ПРО; Владивосток; 2027; стратегия")
    finish.set_theme_fonts(prs)
    prs.save(pptx_path)
    print("pptx:", pptx_path)

    pr = PdfRenderer()
    for p in pages:
        pr.render(p)
    pdf_path = os.path.join(out_dir, NAME + ".pdf")
    pr.doc.set_metadata({"title": "Стратегия ПРО — Владивосток 2027 (сжатая версия)",
                         "author": "Лемана ПРО", "creator": "powerpoint_studio"})
    pr.save(pdf_path)
    print("pdf:", pdf_path)

    if png:
        doc = pymupdf.open(pdf_path)
        folder = os.path.join(out_dir, "pro_preview")
        os.makedirs(folder, exist_ok=True)
        for i, page in enumerate(doc, start=1):
            page.get_pixmap(dpi=110).save(os.path.join(folder, f"p{i:02d}.png"))
        print("png:", folder)
    return pptx_path


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    build(png="--png" in sys.argv)
