"""Low-level drawing primitives rendered twice: into python-pptx and into PyMuPDF.

All coordinates are inches, origin = top-left of the 13.333 x 7.5 in slide.
Every ``Slide`` primitive is a small dict so it can be replayed by both backends.
"""
from __future__ import annotations

import os
from PIL import ImageFont

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
_FONT_FILES = {w: os.path.join(ASSETS, f"LMMain-{w}.ttf") for w in (300, 400, 600, 700)}
_cache: dict[tuple[int, int], ImageFont.FreeTypeFont] = {}


# ---------------------------------------------------------------- text layout
def _font(weight: int, size_pt: float, scale: float = 4.0):
    px = max(1, int(round(size_pt * scale)))
    key = (weight, px)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(_FONT_FILES[weight], px)
    return _cache[key]


def text_width(s: str, size_pt: float, weight: int = 400) -> float:
    """Width in inches of a single line."""
    if not s:
        return 0.0
    f = _font(weight, size_pt)
    return f.getlength(s) / 4.0 / 72.0


def wrap(s: str, width_in: float, size_pt: float, weight: int = 400) -> list[str]:
    """Greedy word wrap; keeps explicit newlines, never splits words."""
    out: list[str] = []
    for para in str(s).split("\n"):
        if not para.strip():
            out.append("")
            continue
        words = para.split(" ")
        line = ""
        for w in words:
            cand = w if not line else line + " " + w
            if text_width(cand, size_pt, weight) <= width_in or not line:
                line = cand
            else:
                out.append(line)
                line = w
        out.append(line)
    return out


def fit_size(s: str, width_in: float, height_in: float, size_pt: float,
             weight: int = 400, min_pt: float = 7.0, line: float = 1.22) -> float:
    """Largest size <= size_pt whose wrapped text fits the box."""
    size = size_pt
    while size > min_pt:
        lines = wrap(s, width_in, size, weight)
        if len(lines) * size * line / 72.0 <= height_in + 0.02:
            return size
        size -= 0.5
    return min_pt


# ---------------------------------------------------------------- primitives
class Slide:
    """Ordered list of drawing primitives for one slide."""

    def __init__(self, number: int | None = None):
        self.items: list[dict] = []
        self.number = number

    # -- shapes ----------------------------------------------------------
    def rect(self, x, y, w, h, fill=None, line=None, lw=0.75, radius=0.0, dash=None):
        self.items.append(dict(t="rect", x=x, y=y, w=w, h=h, fill=fill, line=line,
                               lw=lw, radius=radius, dash=dash))

    def line(self, x1, y1, x2, y2, color, lw=0.75, dash=None):
        self.items.append(dict(t="line", x1=x1, y1=y1, x2=x2, y2=y2, color=color,
                               lw=lw, dash=dash))

    def image(self, path, x, y, w, h=None):
        if h is None:
            with Image.open(path) as im:
                h = w * im.size[1] / im.size[0]
        self.items.append(dict(t="image", path=path, x=x, y=y, w=w, h=h))

    def polygon(self, points, fill, alpha=None, line=None, lw=1.0):
        self.items.append(dict(t="poly", points=points, fill=fill, alpha=alpha,
                               line=line, lw=lw))

    def arc(self, cx, cy, r_out, r_in, start_deg, end_deg, fill):
        """Ring sector; angles clockwise from 12 o'clock (as in PowerPoint doughnuts)."""
        self.items.append(dict(t="arc", cx=cx, cy=cy, r_out=r_out, r_in=r_in,
                               start=start_deg, end=end_deg, fill=fill))

    # -- text ------------------------------------------------------------
    def text(self, x, y, w, h, s, size=12, weight=400, color="FFFFFF",
             align="l", valign="t", line=1.22, tracking=0, caps=False,
             fit=False, min_size=7.0, opacity=1.0, space_after=0.0):
        s = str(s)
        if caps:
            s = s.upper()
        if fit:
            size = fit_size(s, w, h, size, weight, min_size, line)
        self.items.append(dict(t="text", x=x, y=y, w=w, h=h, s=s, size=size,
                               weight=weight, color=color, align=align, valign=valign,
                               line=line, tracking=tracking, opacity=opacity,
                               space_after=space_after))

    def bullets(self, x, y, w, h, items, size=10.5, weight=400, color="FFFFFF",
                bullet="—", gap=0.06, line=1.24, bullet_color=None):
        """Bulleted paragraph list; bullet is a text prefix."""
        self.items.append(dict(t="bullets", x=x, y=y, w=w, h=h, items=list(items),
                               size=size, weight=weight, color=color, bullet=bullet,
                               gap=gap, line=line, bullet_color=bullet_color or "FFC100"))

    def table(self, x, y, w, col_w, rows, header=True, size=9.5, head_size=9.0,
              row_h=0.34, head_h=0.34, fill="FFFFFF", alt="F2F3F3",
              head_fill="303738", head_color="FFFFFF", text_color="303738",
              aligns=None, bold_first_col=False, line_color="FFFFFF", valign="m"):
        self.items.append(dict(t="table", x=x, y=y, w=w, col_w=col_w, rows=rows,
                               header=header, size=size, head_size=head_size,
                               row_h=row_h, head_h=head_h, fill=fill, alt=alt,
                               head_fill=head_fill, head_color=head_color,
                               text_color=text_color, aligns=aligns or ["l"],
                               bold_first_col=bold_first_col,
                               line_color=line_color, valign=valign))


from PIL import Image  # noqa: E402  (used by Slide.image)
