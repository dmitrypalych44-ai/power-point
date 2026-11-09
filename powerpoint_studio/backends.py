"""Two renderers for a list of ``Slide`` primitives: PPTX (deliverable) and PDF (proof)."""
from __future__ import annotations

import re
import math
import os

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.oxml.ns import qn
from lxml import etree

import pymupdf

from . import brand as B
from .primitives import wrap, text_width, _FONT_FILES

PT = 72.0  # points per inch
_ALIGN = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}


def _rgb(hexstr: str) -> RGBColor:
    return RGBColor.from_string(hexstr)


def _pcolor(hexstr: str):
    h = hexstr.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def _arc_points(cx, cy, ro, ri, a0, a1):
    n = max(8, int(abs(a1 - a0) / 3))
    pts = []
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n)
        pts.append((cx + ro * math.sin(a), cy - ro * math.cos(a)))
    for i in range(n + 1):
        a = math.radians(a1 + (a0 - a1) * i / n)
        pts.append((cx + ri * math.sin(a), cy - ri * math.cos(a)))
    return pts


def _table_geometry(it):
    """Shared row heights for tables (content-driven)."""
    col_w = [c * it["w"] / sum(it["col_w"]) for c in it["col_w"]]
    nhead = 1 if it["header"] else 0
    heights = []
    for ri, row in enumerate(it["rows"]):
        if ri < nhead:
            need = it["head_h"]
            for ci, cell in enumerate(row):
                lines = wrap(str(cell), col_w[ci] - 0.20, it["head_size"], 600)
                need = max(need, len(lines) * it["head_size"] * 1.16 / 72.0 + 0.12)
            heights.append(need)
            continue
        need = it["row_h"]
        for ci, cell in enumerate(row):
            lines = wrap(str(cell), col_w[ci] - 0.20, it["size"], 400)
            need = max(need, len(lines) * it["size"] * 1.16 / 72.0 + 0.11)
        heights.append(need)
    return col_w, heights


# =====================================================================  PPTX
class PptxRenderer:
    def __init__(self):
        self.prs = Presentation()
        self.prs.slide_width = Inches(B.SLIDE_W)
        self.prs.slide_height = Inches(B.SLIDE_H)
        self.blank = self.prs.slide_layouts[6]

    # -- text box ---------------------------------------------------------
    @staticmethod
    def _box(slide, x, y, w, h, anchor="t"):
        tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame
        tf.word_wrap = False
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        tf.auto_size = None
        tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE,
                              "b": MSO_ANCHOR.BOTTOM}[anchor]
        return tb, tf

    def build(self, pages):
        for p in pages:
            self.render(p)
        return self

    def render(self, page):
        s = self.prs.slides.add_slide(self.blank)
        bg = s.background.fill
        bg.solid()
        bg.fore_color.rgb = _rgb(B.BG)
        for it in page.items:
            getattr(self, "_" + it["t"])(s, it)
        if page.number:
            _, tf = self._box(s, B.SLIDE_W - 1.25, B.SLIDE_H - 0.50, 0.63, 0.28, "t")
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.RIGHT
            r = p.add_run()
            r.text = str(page.number)
            r.font.size = Pt(9.5)
            r.font.name = B.FONT
            r.font.color.rgb = _rgb(B.INK_3)
        return s

    # -- primitives -------------------------------------------------------
    def _rect(self, s, it):
        radius = it.get("radius") or 0
        shp = s.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE,
            Inches(it["x"]), Inches(it["y"]), Inches(it["w"]), Inches(it["h"]))
        if radius:
            shp.adjustments[0] = min(0.5, radius / max(0.01, min(it["w"], it["h"])))
        if it.get("fill"):
            shp.fill.solid()
            shp.fill.fore_color.rgb = _rgb(it["fill"])
        else:
            shp.fill.background()
        if it.get("line"):
            shp.line.color.rgb = _rgb(it["line"])
            shp.line.width = Pt(it.get("lw") or 0.75)
            if it.get("dash"):
                ln = shp.line._get_or_add_ln()
                d = etree.SubElement(ln, qn("a:prstDash"))
                d.set("val", it["dash"])
        else:
            shp.line.fill.background()
        shp.shadow.inherit = False

    def _line(self, s, it):
        c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(it["x1"]), Inches(it["y1"]),
                                   Inches(it["x2"]), Inches(it["y2"]))
        c.line.color.rgb = _rgb(it["color"])
        c.line.width = Pt(it["lw"])
        if it.get("dash"):
            ln = c.line._get_or_add_ln()
            d = etree.SubElement(ln, qn("a:prstDash"))
            d.set("val", it["dash"])

    def _image(self, s, it):
        s.shapes.add_picture(it["path"], Inches(it["x"]), Inches(it["y"]),
                             Inches(it["w"]), Inches(it["h"]))

    def _poly(self, s, it):
        pts = it["points"]
        fb = s.shapes.build_freeform(Inches(pts[0][0]), Inches(pts[0][1]))
        fb.add_line_segments([(Inches(px), Inches(py)) for px, py in pts[1:]], close=True)
        shp = fb.convert_to_shape()
        shp.fill.solid()
        shp.fill.fore_color.rgb = _rgb(it["fill"])
        if it.get("line"):
            shp.line.color.rgb = _rgb(it["line"])
            shp.line.width = Pt(it.get("lw") or 1.0)
        else:
            shp.line.fill.background()
        shp.shadow.inherit = False

    def _arc(self, s, it):
        self._poly(s, dict(points=_arc_points(it["cx"], it["cy"], it["r_out"], it["r_in"],
                                              it["start"], it["end"]), fill=it["fill"],
                           line=None))

    def _text(self, s, it):
        x, y, w, h = it["x"], it["y"], it["w"], it["h"]
        lines = wrap(it["s"], w, it["size"], it["weight"])
        line_h = it["size"] * it["line"] / 72.0
        total = line_h * len(lines)
        if it["valign"] == "m":
            y += (h - total) / 2
        elif it["valign"] == "b":
            y += h - total
        _, tf = self._box(s, x, y - 0.03, w, total + 0.08)
        for i, ln in enumerate(lines):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = _ALIGN[it["align"]]
            p.line_spacing = it["line"]
            p.space_before = Pt(0)
            p.space_after = Pt(0)
            r = p.add_run()
            r.text = ln if ln else " "
            f = r.font
            f.size = Pt(it["size"])
            f.name = B.FONT
            f.bold = it["weight"] >= 600
            f.color.rgb = _rgb(it["color"])
            if it.get("tracking"):
                r.font._rPr.set("spc", str(int(it["tracking"] * 100)))

    def _bullets(self, s, it):
        x, y, w = it["x"], it["y"], it["w"]
        size, bullet = it["size"], it["bullet"]
        bw = 0.0 if not bullet else 0.26
        line_h = size * it["line"] / 72.0
        cy = y
        for txt in it["items"]:
            lines = wrap(txt, w - bw, size, it["weight"])
            if bullet:
                self._text(s, dict(x=x, y=cy - 0.005, w=bw - 0.02, h=line_h, s=bullet,
                                   size=size, weight=700, color=it["bullet_color"],
                                   align="l", valign="t", line=it["line"]))
            self._text(s, dict(x=x + bw, y=cy, w=w - bw, h=line_h * len(lines), s=txt,
                               size=size, weight=it["weight"], color=it["color"],
                               align="l", valign="t", line=it["line"]))
            cy += line_h * len(lines) + it["gap"]

    def _table(self, s, it):
        x, y = it["x"], it["y"]
        col_w, heights = _table_geometry(it)
        nhead = 1 if it["header"] else 0
        cy = y
        for ri, row in enumerate(it["rows"]):
            fill = it["head_fill"] if ri < nhead else (it["fill"] if (ri - nhead) % 2 == 0 else it["alt"])
            self._rect(s, dict(x=x, y=cy, w=it["w"], h=heights[ri], fill=fill))
            cy += heights[ri]
        cy = y
        for ri, row in enumerate(it["rows"]):
            cx, h = x, heights[ri]
            for ci, cell in enumerate(row):
                cw = col_w[ci]
                align = it["aligns"][ci] if ci < len(it["aligns"]) else "l"
                color = it["head_color"] if ri < nhead else it["text_color"]
                weight = 600 if (ri < nhead or (it["bold_first_col"] and ci == 0)) else 400
                size = it["head_size"] if ri < nhead else it["size"]
                if ri > 0 and align == "l" and len(str(cell)) > 2:
                    weight = max(weight, 600)   # подпись строки читается как заголовок
                pad = 0.10
                cell = str(cell)
                if ri > 0 and align == "r" and re.match(r"^[+\-−]?[\d\s.,]+\s*[%₽pk]?$", cell):
                    size = it["size"] + 1.2
                    weight = 700
                    color = it.get("num_color") or B.INK
                self._text(s, dict(x=cx + pad, y=cy + 0.02, w=cw - 2 * pad, h=h - 0.04,
                                   s=cell, size=size, weight=weight, color=color,
                                   align=align, valign=it["valign"], line=1.16))
                cx += cw
            cy += h

    def save(self, path):
        self.prs.save(path)


# ======================================================================  PDF
class PdfRenderer:
    def __init__(self):
        self.doc = pymupdf.open()
        self.page = None

    def render(self, page_model):
        page = self.doc.new_page(width=B.SLIDE_W * PT, height=B.SLIDE_H * PT)
        self.page = page
        page.draw_rect(page.rect, color=None, fill=_pcolor(B.BG))
        for it in page_model.items:
            getattr(self, "_" + it["t"])(it)
        if page_model.number:
            s = str(page_model.number)
            f = self._font(page, 400)
            tw = text_width(s, 9.5) * PT
            page.insert_text((page.rect.width - B.M * PT - tw, page.rect.height - 0.29 * PT),
                             s, fontname=f, fontsize=9.5, color=_pcolor(B.INK_3))
        return page

    @staticmethod
    def _font(page, weight):
        name = f"LM{weight}"
        page.insert_font(fontname=name, fontfile=_FONT_FILES[weight])
        return name

    def _rect(self, it):
        page = self.page
        r = pymupdf.Rect(it["x"] * PT, it["y"] * PT, (it["x"] + it["w"]) * PT,
                         (it["y"] + it["h"]) * PT)
        fill = _pcolor(it["fill"]) if it.get("fill") else None
        color = _pcolor(it["line"]) if it.get("line") else None
        # PyMuPDF takes a relative corner radius (fraction of the short side)
        radius = (it.get("radius") or 0) / max(0.01, min(it["w"], it["h"]))
        radius = min(radius, 0.5)
        if radius > 0.1:
            page.draw_rect(r, color=color, fill=fill,
                           width=(it.get("lw") or 0.75) if color else 0,
                           radius=radius, dashes="3 2" if it.get("dash") else None)
        else:
            page.draw_rect(r, color=color, fill=fill,
                           width=(it.get("lw") or 0.75) if color else 0,
                           dashes="3 2" if it.get("dash") else None)

    def _line(self, it):
        self.page.draw_line((it["x1"] * PT, it["y1"] * PT), (it["x2"] * PT, it["y2"] * PT),
                            color=_pcolor(it["color"]), width=it["lw"],
                            dashes="3 2" if it.get("dash") else None)

    def _image(self, it):
        self.page.insert_image(
            pymupdf.Rect(it["x"] * PT, it["y"] * PT,
                         (it["x"] + it["w"]) * PT, (it["y"] + it["h"]) * PT),
            filename=it["path"], keep_proportion=False)

    def _poly(self, it):
        pts = [(px * PT, py * PT) for px, py in it["points"]]
        shape = self.page.new_shape()
        shape.draw_polyline(pts + [pts[0]])
        shape.finish(color=_pcolor(it["line"]) if it.get("line") else None,
                     fill=_pcolor(it["fill"]) if it.get("fill") else None,
                     width=it.get("lw") or 1.0)
        shape.commit()

    def _arc(self, it):
        self._poly(dict(points=_arc_points(it["cx"], it["cy"], it["r_out"], it["r_in"],
                                           it["start"], it["end"]), fill=it["fill"],
                        line=None))

    def _text(self, it):
        x, y, w, h = it["x"], it["y"], it["w"], it["h"]
        lines = wrap(it["s"], w, it["size"], it["weight"])
        line_h = it["size"] * it["line"] / 72.0
        total = line_h * len(lines)
        if it["valign"] == "m":
            y += (h - total) / 2
        elif it["valign"] == "b":
            y += h - total
        f = self._font(self.page, it["weight"])
        for i, ln in enumerate(lines):
            if not ln:
                continue
            tw = text_width(ln, it["size"], it["weight"])
            tx = x if it["align"] == "l" else (x + (w - tw) / 2 if it["align"] == "c" else x + w - tw)
            ty = y + i * line_h + it["size"] * 0.80 / 72.0
            self.page.insert_text((tx * PT, ty * PT), ln, fontname=f, fontsize=it["size"],
                                  color=_pcolor(it["color"]))

    def _bullets(self, it):
        x, y, w = it["x"], it["y"], it["w"]
        size, bullet = it["size"], it["bullet"]
        bw = 0.0 if not bullet else 0.26
        line_h = size * it["line"] / 72.0
        cy = y
        for txt in it["items"]:
            lines = wrap(txt, w - bw, size, it["weight"])
            if bullet:
                self._text(dict(x=x, y=cy - 0.005, w=bw - 0.02, h=line_h, s=bullet,
                                size=size, weight=700, color=it["bullet_color"],
                                align="l", valign="t", line=it["line"]))
            self._text(dict(x=x + bw, y=cy, w=w - bw, h=line_h * len(lines), s=txt,
                            size=size, weight=it["weight"], color=it["color"],
                            align="l", valign="t", line=it["line"]))
            cy += line_h * len(lines) + it["gap"]

    def _table(self, it):
        x, y = it["x"], it["y"]
        col_w, heights = _table_geometry(it)
        nhead = 1 if it["header"] else 0
        cy = y
        for ri, row in enumerate(it["rows"]):
            fill = it["head_fill"] if ri < nhead else (it["fill"] if (ri - nhead) % 2 == 0 else it["alt"])
            self._rect(dict(x=x, y=cy, w=it["w"], h=heights[ri], fill=fill))
            cy += heights[ri]
        cy = y
        for ri, row in enumerate(it["rows"]):
            cx, h = x, heights[ri]
            for ci, cell in enumerate(row):
                cw = col_w[ci]
                align = it["aligns"][ci] if ci < len(it["aligns"]) else "l"
                color = it["head_color"] if ri < nhead else it["text_color"]
                weight = 600 if (ri < nhead or (it["bold_first_col"] and ci == 0)) else 400
                size = it["head_size"] if ri < nhead else it["size"]
                if ri > 0 and align == "l" and len(str(cell)) > 2:
                    weight = max(weight, 600)   # подпись строки читается как заголовок
                pad = 0.10
                cell = str(cell)
                if ri > 0 and align in ("r", "c") and re.match(r"^[+\-−]?[\d\s.,]+\s*[%₽pk]?", cell):
                    color = it["text_color"] if cell else color
                self._text(dict(x=cx + pad, y=cy + 0.02, w=cw - 2 * pad, h=h - 0.04,
                                s=cell, size=size, weight=weight, color=color,
                                align=align, valign=it["valign"], line=1.16))
                cx += cw
            cy += h

    def save(self, path):
        self.doc.save(path, deflate=True, garbage=3)


def table_height(it) -> float:
    """Bottom-left y offset consumed by a table (useful for stacking)."""
    _, heights = _table_geometry(it)
    return sum(heights)
