"""Build the Лемана ПРО «Стратегия Владивосток 2027» deck (PPTX + PDF proof)."""
from __future__ import annotations

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pymupdf

from powerpoint_studio.backends import PptxRenderer, PdfRenderer
from powerpoint_studio import pages_a, pages_b, pages_c
from powerpoint_studio import finish


def build(out_dir: str = "deliverables", pdf: bool = True, png: bool = False,
          embed_fonts: bool = False):
    os.makedirs(out_dir, exist_ok=True)
    pages = [f() for f in pages_a.PAGES + pages_b.PAGES + pages_c.PAGES]
    # page numbers come from the deck order; фирменный домик — на каждом слайде
    from powerpoint_studio.components import house_mark
    for i, p in enumerate(pages, start=1):
        p.number = i
        # на обложке и финале стоит полный логотип — отдельный домик не нужен
        if i not in (1, len(pages)):
            house_mark(p)
    print("pages:", len(pages))
    pptx_path = os.path.join(out_dir, "Лемана_ПРО_Стратегия_Владивосток_2027.pptx")
    prs = PptxRenderer().build(pages).prs
    finish.set_props(prs,
                     "Стратегия Владивосток 2027 — Лемана ПРО",
                     "Трансформация магазина 75: шесть миров и вайтбокс, четыре рычага роста и один путь клиента",
                     keywords="Лемана ПРО; стратегия; Владивосток; 2027; магазин 75")
    finish.set_theme_fonts(prs)
    faces = []
    if embed_fonts:
        # ВНИМАНИЕ: по ECMA-376 вложенные шрифты должны быть обфусцированы (ODTTF).
        # Здесь кладётся «сырой» TTF, поэтому режим только для стендовой проверки:
        # в PowerPoint такой файл может потребовать восстановления.
        faces = finish.embed_fonts(
            prs, os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets"))
    prs.save(pptx_path)
    print("pptx:", pptx_path, len(pages), "slides;",
          "fonts embedded" if faces else "шрифт LM Main заявлен, файл кладётся рядом")
    if pdf:
        pr = PdfRenderer()
        for p in pages:
            pr.render(p)
        pdf_path = os.path.join(out_dir, "Лемана_ПРО_Стратегия_Владивосток_2027.pdf")
        pr.doc.set_metadata({
            "title": "Стратегия Владивосток 2027 — Лемана ПРО",
            "subject": "Трансформация магазина 75: шесть миров и вайтбокс, четыре рычага роста и один путь клиента",
            "author": "Лемана ПРО",
            "keywords": "Лемана ПРО, стратегия, Владивосток, 2027",
            "creator": "powerpoint_studio",
        })
        pr.save(pdf_path)
        print("pdf:", pdf_path)
        if png:
            doc = pymupdf.open(pdf_path)
            folder = os.path.join(out_dir, "preview")
            os.makedirs(folder, exist_ok=True)
            for i, page in enumerate(doc, start=1):
                page.get_pixmap(dpi=110).save(os.path.join(folder, f"s{i:02d}.png"))
            print("png:", folder)
    return pptx_path


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    build(pdf=True, png="--png" in sys.argv, embed_fonts="--embed-fonts" in sys.argv)
