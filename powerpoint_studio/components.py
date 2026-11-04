"""House-style page components: headers, KPI cards, panels, callouts, tables."""
from __future__ import annotations

import os

from . import brand as B
from .primitives import Slide, text_width, wrap

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
HOUSE_YELLOW = os.path.join(ASSETS, "house_yellow.png")
HOUSE_DARK = os.path.join(ASSETS, "house_dark.png")
HOUSE_WHITE = os.path.join(ASSETS, "house_white.png")


# ------------------------------------------------------------------ helpers
def house_mark(sl, h=0.42, x=None, y=0.34, path=None):
    """Фирменный домик Лемана ПРО на каждом слайде — правый верхний угол."""
    path = path or HOUSE_YELLOW
    w = h * 157 / 174.0
    sl.image(path, (x if x is not None else B.SLIDE_W - B.M - w), y, w, h)


def project_badge(sl, name, x=B.M, y=B.HEAD_KICKER - 0.08, size=18.0,
                  color=B.INK, accent=B.YELLOW):
    """Крупное название проекта в шапке: жёлтая плашка + название."""
    label = "Проект «%s»" % name
    w = text_width(label, size, 700) + 0.44
    h = size * 1.30 / 72
    sl.rect(x, y, 0.09, h, fill=accent)
    sl.text(x + 0.24, y - 0.01, w, h + 0.04, label, size=size, weight=700,
            color=color, tracking=0.2)
    return x + 0.24 + w + 0.30
def house_shape(sl, x, y, w, h, fill, peak=0.34):
    """Дом-стрелка из брендбука: pentagon with the roof peak (6 sides)."""
    sl.polygon([(x, y + h), (x, y + h * peak), (x + w / 2, y), (x + w, y + h * peak),
                (x + w, y + h)], fill)


HEAD_RIGHT = 0.86      # зазор под фирменный домик в правом верхнем углу


def kicker(sl, text, x=B.M, y=B.HEAD_KICKER, color=B.INK_3, size=10.5):
    sl.text(x, y, B.CW - HEAD_RIGHT, 0.3, text, size=size, weight=600, color=color,
            tracking=1.4, caps=True)


def fit_title(text, w, size=29, min_size=19.0, max_h=0.82, line=1.04):
    """Largest display size at which the headline fits in `max_h` (1 or 2 lines)."""
    while size > min_size:
        lines = wrap(text, w, size, 700)
        if len(lines) * size * line / 72.0 <= max_h:
            return size, lines
        size -= 0.5
    return min_size, wrap(text, w, min_size, 700)


def title(sl, text, x=B.M, y=B.HEAD_TITLE, w=None, size=29, color=B.INK):
    w = w or (B.CW - HEAD_RIGHT)
    size, _ = fit_title(text, w, size)
    sl.text(x, y, w, 0.66, text, size=size, weight=700, color=color, line=1.04)


def subtitle(sl, text, x=B.M, y=B.HEAD_SUB, w=B.CW, size=12.5, color=B.INK_2):
    sl.text(x, y, w, 0.3, text, size=size, weight=400, color=color, line=1.2)


def rule(sl, x=B.M, y=B.RULE_Y, w=1.55, color=B.YELLOW, h=0.045):
    sl.rect(x, y, w, h, fill=color)


def head(sl, kick_text, title_text, sub_text=None, rule_w=1.55, title_size=29,
         title_w=None, sub_size=12.5, project=None):
    """Шапка слайда. `project` — крупное название проекта, `kick_text` — раздел."""
    x0 = B.M
    if project:
        x0 = project_badge(sl, project)
        sl.text(x0, B.HEAD_KICKER + 0.06, B.CW - (x0 - B.M) - HEAD_RIGHT, 0.3, kick_text,
                size=10.0, weight=600, color=B.INK_3, tracking=1.4, caps=True)
    else:
        kicker(sl, kick_text)
    title(sl, title_text, size=title_size, w=title_w or (B.CW - HEAD_RIGHT))
    if sub_text:
        subtitle(sl, sub_text, size=sub_size)
    rule(sl, w=rule_w)


def footnote(sl, text, y=B.FOOTNOTE_Y, size=6.8, color=B.INK_3, w=None, x=B.M):
    sl.text(x, y, w or (B.CW - 0.9), 0.34, text, size=size, weight=300, color=color,
            line=1.18)


def section_label(sl, text, x, y, w, color=B.INK, size=14.5, weight=600):
    sl.text(x, y, w, 0.3, text, size=size, weight=weight, color=color)
    sl.rect(x, y + 0.33, 0.34, 0.035, fill=B.YELLOW)


# ------------------------------------------------------------------ KPI card
def kpi(sl, x, y, w, h, label, value, note=None, value_size=27, accent=B.YELLOW,
        note_color=None, note_prefix=None, label_size=9.5):
    """Белая KPI-карточка с жёлтой полосой сверху и тонкой обводкой."""
    sl.rect(x, y, w, h, fill=B.WHITE, line=B.CARD_BORDER, lw=0.75)
    sl.rect(x, y, w, 0.045, fill=accent)
    sl.text(x + 0.22, y + 0.20, w - 0.4, 0.24, label, size=label_size, weight=400,
            color=B.INK_3, line=1.12)
    sl.text(x + 0.22, y + 0.44, w - 0.4, h - 0.9, value, size=value_size, weight=700,
            color=B.DARK_TEXT, line=1.0, fit=True, min_size=13)
    if note:
        ny = y + h - 0.42
        if note_prefix:
            pw = text_width(note_prefix, 8.6, 600)
            sl.text(x + 0.22, ny, pw + 0.04, 0.3, note_prefix, size=8.6, weight=600,
                    color=B.YELLOW_DIM if note_color is None else note_color, line=1.1)
            sl.text(x + 0.22 + pw + 0.04, ny, w - 0.44 - pw, 0.3, note, size=8.6,
                    weight=400, color=B.INK_2, line=1.1)
        else:
            sl.text(x + 0.22, ny, w - 0.44, 0.3, note, size=8.6, weight=400,
                    color=note_color or B.INK_2, line=1.1)


def donut(sl, cx, cy, r_out, r_in, parts, center=None, center_value_size=34,
          label_size=9.0, leader_x=None):
    """Фирменное кольцо-диаграмма: только палитра бренда + её тёмные оттенки."""
    total = sum(p["value"] for p in parts) or 1
    a = 0.0
    for p in parts:
        sweep = 360.0 * p["value"] / total
        sl.arc(cx, cy, r_out, r_in, a, a + sweep, p.get("color", B.YELLOW))
        a += sweep
    if center is not None:
        sl.text(cx - r_in * 0.95, cy - 0.32, r_in * 1.9, 0.64, center, size=center_value_size,
                weight=700, color=B.INK, align="c", valign="m", line=1.0)


def legend(sl, x, y, w, items, size=9.5, row_h=0.34, marker=0.14, marker_shape="house"):
    """Легенда фирменными «домиками»."""
    cy = y
    for it in items:
        mx = x + marker / 2
        if marker_shape == "house":
            house_shape(sl, x, cy + 0.03, marker, marker, it.get("color", B.YELLOW))
        else:
            sl.rect(x, cy + 0.03, marker, marker, fill=it.get("color", B.YELLOW))
        sl.text(x + marker + 0.14, cy - 0.01, 0.62, 0.22, it["value"], size=size,
                weight=700, color=B.INK, align="l")
        sl.text(x + marker + 0.78, cy - 0.01, w - marker - 0.78, 0.30, it["label"],
                size=size, weight=400, color=B.INK_2, line=1.2)
        cy += row_h


def hbars(sl, x, y, w, items, row_h=0.52, label_w=2.35, bar_h=0.16, max_value=None,
          value_w=0.85, size=9.2):
    """Горизонтальные полосы: подпись — жёлтая полоса — значение."""
    max_value = max_value or max(i["value"] for i in items)
    cy = y
    for bi, it in enumerate(items):
        sl.text(x, cy, label_w - 0.12, 0.24, it["label"], size=size, weight=400,
                color=it.get("label_color", B.INK), line=1.15)
        bw = (w - label_w - value_w) * it["value"] / max_value
        sl.rect(x + label_w, cy + 0.03, (w - label_w - value_w), bar_h, fill=B.SURFACE_3)
        col = it.get("color") or B.SERIES[bi % len(B.SERIES)]
        sl.rect(x + label_w, cy + 0.03, max(0.02, bw), bar_h, fill=col)
        sl.text(x + w - value_w, cy, value_w, 0.24, it["value_label"], size=size, weight=700,
                color=B.INK, align="r")
        cy += row_h


def kpi_row(sl, cards, y, h=1.22, gap=0.20, x=B.M, w=B.CW, value_size=26):
    n = len(cards)
    cw = (w - gap * (n - 1)) / n
    for i, c in enumerate(cards):
        kpi(sl, x + i * (cw + gap), y, cw, h, c["label"], c["value"],
            c.get("note"), value_size=c.get("value_size", value_size),
            note_prefix=c.get("note_prefix"), note_color=c.get("note_color"),
            label_size=c.get("label_size", 9.5))
    return y + h


# ------------------------------------------------------------------ panels
def panel(sl, x, y, w, h, fill=B.SURFACE, radius=0.03, line=None):
    sl.rect(x, y, w, h, fill=fill, line=line, lw=0.75, radius=radius)


def callout(sl, x, y, w, h, text, size=10.5, color=B.INK, accent=B.YELLOW,
            align="l", weight=600, fill=B.YELLOW_FAINT):
    panel(sl, x, y, w, h, fill=fill, radius=0.02)
    sl.rect(x, y + 0.10, 0.05, h - 0.20, fill=accent)
    sl.text(x + 0.26, y + 0.10, w - 0.46, h - 0.2, text, size=size, weight=weight,
            color=color, align=align, valign="m", line=1.26, fit=True, min_size=8)


def big_statement(sl, x, y, w, h, lead, text, lead_color=B.YELLOW):
    """Фирменный приём: жирный лид капсом + обычный текст в одну строку."""
    lw = text_width(lead, 11, 700) + 0.10
    sl.text(x, y, lw, h, lead, size=11, weight=700, color=lead_color, caps=True,
            line=1.26, tracking=0.3)
    sl.text(x + lw, y, w - lw, h, text, size=11, weight=400, color=B.INK, line=1.26)


def label_value(sl, x, y, w, value, label, value_size=19, color=B.INK,
                label_color=B.INK_2, gap=0.02):
    sl.text(x, y, w, 0.34, value, size=value_size, weight=700, color=color, line=1.0)
    sl.text(x, y + value_size * 1.12 / 72 + gap, w, 0.5, label, size=8.6, weight=400,
            color=label_color, line=1.16)


def stat_block(sl, x, y, w, h, items, value_size=17, fill=B.PANEL):
    """Столбик «цифра над подписью» на подложке."""
    panel(sl, x, y, w, h, fill=fill)
    cy = y + 0.16
    for it in items:
        sl.text(x + 0.18, cy, w - 0.36, 0.32, it["value"], size=value_size, weight=700,
                color=it.get("color", B.YELLOW_DIM if it.get("accent") else B.INK), line=1.0)
        cy += value_size * 1.05 / 72 + 0.05
        lines_h = 0.16
        sl.text(x + 0.18, cy, w - 0.36, 0.44, it["label"], size=8.6, weight=400,
                color=B.INK_2, line=1.16)
        cy += lines_h + 0.46


def chevrons(sl, x, y, w, h, labels, active=0, gap=0.12, size=9.5, fill=None,
             acc=B.YELLOW):
    """Полоса этапов (стрелки «дом») — навигация по логике слайда."""
    n = len(labels)
    cw = (w - gap * (n - 1)) / n
    for i, lb in enumerate(labels):
        cx = x + i * (cw + gap)
        on = (i == active) or active is None
        house_shape(sl, cx, y, cw, h, fill or (acc if on else B.SURFACE_2), peak=0.42)
        sl.text(cx + 0.06, y + h * 0.48, cw - 0.12, h * 0.46, lb, size=size, weight=600,
                color=B.DARK_TEXT if on else B.INK, align="c", valign="m", line=1.08,
                fit=True, min_size=6.5, caps=True)
