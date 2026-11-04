"""Build the Лемана ПРО «Стратегия Владивосток 2027» deck (PPTX + PDF proof)."""
from __future__ import annotations

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pymupdf

from powerpoint_studio.backends import PptxRenderer, PdfRenderer
from powerpoint_studio import pages_a, pages_b, pages_c


def build(out_dir: str = "deliverables", pdf: bool = True, png: bool = False):
    os.makedirs(out_dir, exist_ok=True)
    pages = [f() for f in pages_a.PAGES + pages_b.PAGES + pages_c.PAGES]
    # page numbers come from the deck order
    for i, p in enumerate(pages, start=1):
        p.number = i
    print("pages:", len(pages))
    pptx_path = os.path.join(out_dir, "Лемана_ПРО_Стратегия_Владивосток_2027.pptx")
    PptxRenderer().build(pages).save(pptx_path)
    print("pptx:", pptx_path, len(pages), "slides")
    if pdf:
        pr = PdfRenderer()
        for p in pages:
            pr.render(p)
        pdf_path = os.path.join(out_dir, "Лемана_ПРО_Стратегия_Владивосток_2027.pdf")
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
    build(pdf=True, png="--png" in sys.argv)
