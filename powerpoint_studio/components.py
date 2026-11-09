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

PICTO = {
    "Вайтбокс": "pic_whitebox.png",
    "Стена": "pic_stena.png",
    "Пол": "pic_pol.png",
    "Двери": "pic_dveri.png",
    "Ванная": "pic_vannaya.png",
    "Кухни": "pic_kuhni.png",
    "Сад": "pic_sad.png",
    "ПРО": "pic_pro.png",
    "Логистика": "pic_logistika.png",
    "Команда": "pic_komanda.png",
    "Проектный центр": "pic_itogi.png",
}


def head_picto(sl, project, x=B.M, y=B.HEAD_KICKER - 0.14, h=0.58):
    """Пиктограмма проекта слева от заголовка (фирменная линейная графика)."""
    name = PICTO.get(project)
    if not name:
        return x
    path = os.path.join(ASSETS, name)
    if not os.path.exists(path):
        return x
    from PIL import Image
    with Image.open(path) as im:
        w = h * im.size[0] / im.size[1]
    sl.image(path, x, y, w, h)
    return x + w + 0.20


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


def marker(sl, x, y, w=0.34, h=0.035, color=B.YELLOW):
    """Метка подзаголовка: жёлтый отрезок со скошенным правым концом."""
    sl.polygon([(x, y), (x + w, y), (x + w + h * 1.4, y + h), (x, y + h)], color)


def rule(sl, x=B.M, y=B.RULE_Y, w=1.55, color=B.YELLOW, h=0.045, tail=True):
    """Заголовочная линейка: плотный жёлтый отрезок + волосяное продолжение."""
    sl.rect(x, y, w, h, fill=color)
    if tail:
        sl.rect(x + w + 0.16, y + h / 2 - 0.004, B.CW - w - 1.28, 0.008, fill=B.LINE)


SEC_HEAD_SIZE = 12.6          # единый кегль подзаголовков на всех слайдах


def section_head(sl, x, y, w, text, size=None, color=B.INK, tail=None):
    """Подзаголовок блока: жёлтый домик-маркер и волосяная линия под ним.

    Кегль зафиксирован (SEC_HEAD_SIZE), чтобы все блоки во всех слайдах
    стояли на одной типографической сетке.
    """
    size = SEC_HEAD_SIZE
    # подзаголовок обязан остаться в одну строку: кегль подбираем под ширину
    while size > 9.4 and len(wrap(text, w - 0.40, size, 600)) > 1:
        size -= 0.2
    house_shape(sl, x, y + 0.015, 0.24, 0.22, B.YELLOW)
    tx = x + 0.37
    sl.text(tx, y - 0.02, w - 0.40, 0.32, text, size=round(size, 1), weight=600,
            color=color, fit=True, min_size=8.4)
    sl.rect(x, y + 0.36, w, 0.010, fill=B.LINE)
    return tx


def _sent_case(t: str) -> str:
    """«свод → Свод», «действия 2027 · краски → Действия 2027 · Краски»."""
    parts = []
    for chunk in str(t).split(" · "):
        chunk = chunk.strip()
        if chunk and chunk == chunk.upper() and len(chunk) > 3:
            chunk = chunk.capitalize()
        elif chunk:
            chunk = chunk[0].upper() + chunk[1:]
        parts.append(chunk)
    return " · ".join(parts)


def head(sl, kick_text, title_text, sub_text=None, rule_w=1.55, title_size=15.5,
         title_w=None, sub_size=10.5, project=None, kick_size=31.0, picto=True):
    """Шапка: главное — проект и раздел, ниже — короткое описание содержания слайда."""
    avail_full = B.CW - HEAD_RIGHT
    section = _sent_case(kick_text)
    x0 = B.M
    if project and picto:
        x0 = head_picto(sl, project)
    elif project:
        # жёлтая плашка без пиктограммы
        h1_h = kick_size * 1.15 / 72
        sl.rect(B.M, B.HEAD_KICKER - 0.02, 0.11, h1_h + 0.06, fill=B.YELLOW)
        x0 = B.M + 0.30

    h1_h = kick_size * 1.15 / 72
    if project:
        p_str = project
        p_w = text_width(p_str, kick_size, 700)
        sep_w = text_width(" · ", kick_size, 300)
        sec_size = kick_size
        while sec_size > 17 and x0 + p_w + sep_w + text_width(section, sec_size, 300) > B.M + avail_full:
            sec_size -= 1.0
        sl.text(x0, B.HEAD_KICKER - 0.06, p_w + 0.10, h1_h + 0.06, p_str,
                size=kick_size, weight=700, color=B.INK, line=1.0)
        sl.text(x0 + p_w + sep_w * 0.5, B.HEAD_KICKER - 0.02,
                B.M + avail_full - (x0 + p_w + sep_w), h1_h + 0.06, section,
                size=sec_size, weight=300, color=B.INK_2, line=1.0)
    else:
        sl.text(x0, B.HEAD_KICKER - 0.06, avail_full, h1_h + 0.06, section,
                size=kick_size, weight=700, color=B.INK, line=1.0)

    w = title_w or avail_full
    desc_size = title_size
    lines = wrap(title_text, w, desc_size, 400)
    while len(lines) > 2 and desc_size > 12:
        desc_size -= 0.5
        lines = wrap(title_text, w, desc_size, 400)
    sl.text(B.M, 1.00, w, min(0.62, len(lines) * desc_size * 1.12 / 72 + 0.06),
            title_text, size=desc_size, weight=400, color=B.INK, line=1.12)
    if sub_text:
        sub_y = 1.40 if len(lines) == 1 else 1.56
        sl.text(B.M, sub_y, B.CW - 0.3, 0.28, sub_text, size=sub_size, weight=400,
                color=B.INK_3, line=1.16)
    rule(sl, y=1.86, w=rule_w)


FOOT_SIZE = 6.8       # базовый кегль сноски
FOOT_MIN = 6.0        # ниже не опускаемся: сноска должна читаться


def footnote(sl, text, y=B.FOOTNOTE_Y, size=None, color=B.INK_3, w=None, x=B.M):
    """Сноска-источник: всегда одна строка, кегль подбирается под ширину полосы."""
    w = w or (B.CW - 0.9)
    sz = size or FOOT_SIZE
    while sz > FOOT_MIN and text_width(text, sz, 300) > w:
        sz -= 0.1
    sl.text(x, y, w, 0.30, text, size=round(sz, 1), weight=300, color=color, line=1.12)


def section_label(sl, text, x, y, w, color=B.INK, size=14.5, weight=600):
    sl.text(x, y, w, 0.3, text, size=size, weight=weight, color=color)
    sl.rect(x, y + 0.33, 0.34, 0.035, fill=B.YELLOW)


# ------------------------------------------------------------------ KPI card
def kpi(sl, x, y, w, h, label, value, note=None, value_size=27, accent=B.YELLOW,
        note_color=None, note_prefix=None, label_size=9.5, cut=0.20):
    """KPI-карточка со срезанным правым верхним углом и жёлтой кромкой."""
    sl.polygon([(x, y), (x + w - cut, y), (x + w, y + cut), (x + w, y + h), (x, y + h)],
               fill=B.WHITE, line=B.CARD_BORDER, lw=0.75)
    sl.polygon([(x, y), (x + w - cut, y), (x + w, y + cut), (x + w, y + 0.055),
                (x, y + 0.055)], fill=accent)
    sl.rect(x, y + 0.055, 0.055, h - 0.055, fill=accent)
    sl.text(x + 0.22, y + 0.22, w - 0.44, 0.24, label, size=label_size, weight=400,
            color=B.INK_3, line=1.12)
    sl.text(x + 0.22, y + 0.42, w - 0.44, 0.38, value, size=value_size, weight=700,
            color=B.DARK_TEXT, line=1.0, fit=True, min_size=13)
    if note:
        ny = y + h - 0.38
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


KPI_H = 1.16          # единая высота KPI-карточек
KPI_VALUE = 24.0      # единый кегль значения


def kpi_row(sl, cards, y, h=None, gap=0.20, x=B.M, w=B.CW, value_size=None):
    h = KPI_H
    n = len(cards)
    # кегль значения зависит только от числа карточек — одинаково во всех слайдах
    value_size = KPI_VALUE if n <= 4 else (20.0 if n == 5 else 18.0)
    cw = (w - gap * (n - 1)) / n
    for i, c in enumerate(cards):
        kpi(sl, x + i * (cw + gap), y, cw, h, c["label"], c["value"],
            c.get("note"), value_size=value_size,
            note_prefix=c.get("note_prefix"), note_color=c.get("note_color"),
            label_size=c.get("label_size", 9.5))
    return y + h


# ------------------------------------------------------------------ panels
def panel(sl, x, y, w, h, fill=B.SURFACE, radius=0.02, line=None):
    sl.rect(x, y, w, h, fill=fill, line=line, lw=0.75, radius=radius)


CALLOUT_SIZE = 9.4    # единый кегль выносок


def callout(sl, x, y, w, h, text, size=None, color=B.INK, accent=B.YELLOW,
            align="l", weight=600, fill=B.YELLOW_FAINT):
    """Выноска-вывод: одинаковая типографика на всех слайдах."""
    size = CALLOUT_SIZE
    panel(sl, x, y, w, h, fill=fill, radius=0.02)
    sl.rect(x, y + 0.10, 0.05, h - 0.20, fill=accent)
    sl.text(x + 0.26, y + 0.09, w - 0.46, h - 0.18, text, size=size, weight=weight,
            color=color, align=align, valign="m", line=1.24, fit=True, min_size=7.6)


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


# ------------------------------------------------ 4. инфографика вместо таблиц
def roadmap(sl, x, y, w, columns, rows, col_w=None, row_h=0.62, head_h=0.42,
            left_label="Квартал", accent_first=True, size=9.4, head_size=9.6):
    """Дорожная карта: тёмные шапки-колонки, строки кварталов с жёлтой осью.

    columns — подписи колонок (без левой), rows — [(метка, [текст, ...]), ...].
    """
    n = len(columns)
    lw = col_w[0] if col_w else 1.00
    cw = col_w[1:] if col_w else [(w - lw) / n] * n
    gap = 0.10
    # шапки
    sl.rect(x, y, lw, head_h, fill=B.DARK)
    sl.text(x + 0.16, y, lw - 0.24, head_h, left_label, size=head_size, weight=700,
            color=B.WHITE, valign="m")
    cx = x + lw + gap
    for i, col in enumerate(columns):
        sl.rect(cx, y, cw[i], head_h, fill=B.DARK)
        sl.text(cx + 0.16, y, cw[i] - 0.28, head_h, col, size=head_size, weight=700,
                color=B.WHITE, valign="m", line=1.1)
        cx += cw[i] + gap

    # вертикальная жёлтая ось под метками
    axis_x = x + 0.30
    ry = y + head_h + 0.12
    total_h = len(rows) * row_h + (len(rows) - 1) * 0.10
    sl.rect(axis_x - 0.02, ry + 0.10, 0.045, total_h - 0.20, fill=B.LINE)

    for r, (label, cells) in enumerate(rows):
        sl.text(x, ry + 0.06, lw - 0.30, 0.30, label, size=head_size + 0.6, weight=700,
                color=B.INK)
        sl.ellipse = None  # (нет примитива «точка» — используем квадрат)
        sl.rect(axis_x - 0.10, ry + 0.12, 0.22, 0.22, fill=B.YELLOW)
        cx = x + lw + gap
        for i, txt in enumerate(cells):
            panel(sl, cx, ry, cw[i], row_h, fill=B.SURFACE)
            sl.text(cx + 0.16, ry + 0.08, cw[i] - 0.32, row_h - 0.14, txt, size=size,
                    weight=400, color=B.INK_2, line=1.18, fit=True, min_size=7.4)
            cx += cw[i] + gap
        ry += row_h + 0.10


def column_chart(sl, x, y, w, h, items, gap=0.22, bar_max_w=0.86, labels=True,
                 label_size=7.6, values=True, ticks=None, axis_w=0.52,
                 tick_size=6.8, tick_fmt=None):
    """Столбчатая диаграмма в фирменной палитре (замена вставленному графику).

    items — [dict(label=..., value=..., color=..., highlight=True)]
    ticks — значения засечек по оси Y; подписи рисуются справа налево от оси.
    """
    vals = [it["value"] for it in items]
    mx = max(vals) or 1
    if ticks:
        mx = max(mx, max(ticks))
    band = w / len(items)
    bar_w = min(bar_max_w, band - gap)
    base = y + h
    ax = x + axis_w
    # засечки сетки и подписи шкалы
    for tv in (ticks or [0, mx / 2.0, mx]):
        gy = base - h * tv / mx
        is_zero = (tv == 0)
        sl.line(ax, gy, x + w, gy, B.SURFACE_3 if is_zero else B.LINE, lw=1.0 if is_zero else 0.5)
        txt = (tick_fmt or (lambda v: ("%g" % v)))(tv)
        sl.text(x - 0.04, gy - 0.09, axis_w - 0.06, 0.18, txt, size=tick_size,
                weight=400, color=B.INK_3, align="r", line=1.0)
    for i, it in enumerate(items):
        cx = ax + i * band + (band - bar_w) / 2
        bh = max(0.02, h * it["value"] / mx)
        col = it.get("color") or (B.YELLOW if it.get("highlight") else B.SURFACE_3)
        sl.rect(cx, base - bh, bar_w, bh, fill=col)
        if values:
            vy = base - bh - 0.24
            sl.text(cx - 0.16, vy, bar_w + 0.32, 0.22,
                    it.get("value_label", "%g" % it["value"]), size=8.4, weight=700,
                    color=B.INK, align="c", line=1.0)
        if labels:
            sl.text(cx - 0.20, base + 0.08, bar_w + 0.40, 0.22, it["label"], size=label_size,
                    weight=600, color=B.INK if it.get("highlight") else B.INK_2,
                    align="c", line=1.0)
    sl.line(ax, base, x + w, base, B.INK_3, lw=0.9)


def cjm_flow(sl, x, y, w, h, steps, label_w=0.62, gap=0.05, size=8.4):
    """Полоса этапов пути клиента: стрелки-«шевроны», звёздочные шаги — акцентом.

    steps — [dict(label=..., star=True/False)]
    """
    n = len(steps)
    lw = label_w
    sw = (w - lw - gap * n) / n
    sl.rect(x, y, lw, h, fill=B.YELLOW)
    sl.text(x, y, lw, h, "Шаг", size=8.6, weight=700, color=B.INK, align="c",
            valign="m", caps=True, tracking=0.6)
    cx = x + lw + gap
    for i, st in enumerate(steps):
        star = st.get("star")
        fill = B.YELLOW if star else B.SURFACE
        pts = [(cx, y), (cx + sw - 0.14, y), (cx + sw, y + h / 2),
               (cx + sw - 0.14, y + h), (cx, y + h), (cx + 0.14, y + h / 2)]
        sl.polygon(pts, fill)
        sl.text(cx + 0.24, y, sw - 0.46, h, st["label"], size=size,
                weight=600 if star else 400, color=B.INK, align="c", valign="m",
                line=1.10, fit=True, min_size=6.6)
        if star:
            _star(sl, cx + sw / 2, y - 0.01, 0.125, B.YELLOW_DIM)
        cx += sw + gap


def _star(sl, cx, cy, r, color):
    """Пятиконечная звезда — маркер ключевых шагов пути клиента."""
    import math
    pts = []
    for k in range(10):
        ang = -math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    sl.polygon(pts, color, line=B.WHITE, lw=1.0)


def priority_columns(sl, x, y, w, items, col_gap=0.16, head_h=0.50, size=9.2,
                     body_fill=B.SURFACE):
    """Карточки-столбцы: тёмная шапка, крупная цифра, текст. Заменяет строки таблицы."""
    n = len(items)
    cw = (w - col_gap * (n - 1)) / n
    h = items[0].get("h", 2.4)
    for i, it in enumerate(items):
        cx = x + i * (cw + col_gap)
        sl.rect(cx, y, cw, head_h, fill=it.get("head_fill", B.DARK))
        sl.text(cx + 0.16, y, cw - 0.28, head_h, it["title"], size=9.6, weight=700,
                color=it.get("head_color", B.WHITE), valign="m", line=1.06,
                fit=True, min_size=8)
        panel(sl, cx, y + head_h, cw, h - head_h, fill=body_fill)
        sl.rect(cx, y + head_h, cw, 0.04, fill=it.get("accent", B.YELLOW))
        cy = y + head_h + 0.16
        if it.get("value"):
            sl.text(cx + 0.16, cy, cw - 0.32, 0.34, it["value"], size=15.5, weight=700,
                    color=it.get("value_color", B.INK), line=1.0)
            cy += 0.40
        if it.get("note"):
            sl.text(cx + 0.16, cy, cw - 0.32, 0.24, it["note"], size=8.4, weight=600,
                    color=B.INK_3, line=1.1)
            cy += 0.24
        if it.get("text"):
            sl.text(cx + 0.16, cy + 0.02, cw - 0.32, y + h - cy - 0.12, it["text"],
                    size=size, weight=400, color=B.INK_2, line=1.2, fit=True, min_size=7)


def stat_cards(sl, x, y, w, items, per_row=4, gap=0.18, h=1.02, size=9.0,
               show_bar=True, fill=B.SURFACE, value_size=15.5):
    """Плитки-цифры с полосой прогресса: замена числовым столбцам таблицы."""
    cw = (w - gap * (per_row - 1)) / per_row
    compact = h < 0.86
    vs = value_size - 2.0 if compact else value_size
    for i, it in enumerate(items):
        r, c = divmod(i, per_row)
        cx = x + c * (cw + gap)
        cy = y + r * (h + 0.12)
        panel(sl, cx, cy, cw, h, fill=fill)
        sl.rect(cx, cy, 0.05, h, fill=it.get("accent", B.YELLOW))
        sl.text(cx + 0.20, cy + 0.09, cw - 0.36, 0.18, it["label"], size=7.4, weight=700,
                color=B.INK_3, caps=True, tracking=0.4, line=1.05, fit=True, min_size=6.2)
        vw = cw - 0.34 - (0.80 if (compact and it.get("note")) else 0)
        sl.text(cx + 0.20, cy + 0.27 if compact else cy + 0.29, vw, 0.30, it["value"],
                size=it.get("value_size", vs), weight=700, color=it.get("color", B.INK),
                line=1.0, fit=True, min_size=9.0)
        if it.get("note"):
            if compact:
                sl.text(cx + cw - 0.92, cy + 0.30, 0.74, 0.20, it["note"], size=7.6,
                        weight=700, color=B.YELLOW_DIM, align="r", line=1.05)
            else:
                sl.text(cx + 0.20, cy + h - 0.36, cw - 0.36, 0.22, it["note"], size=7.6,
                        weight=600, color=B.YELLOW_DIM, line=1.02, fit=True,
                        min_size=6.2)
        if show_bar and it.get("pct") is not None:
            bw = cw - 0.40
            sl.rect(cx + 0.20, cy + h - 0.10, bw, 0.05, fill=B.SURFACE_3)
            sl.rect(cx + 0.20, cy + h - 0.10, max(0.03, bw * it["pct"]), 0.05,
                    fill=it.get("bar", B.YELLOW))


def share_rows(sl, x, y, w, items, row_h=0.42, label_w=2.55, max_value=None,
               size=9.2, value_size=11.0):
    """Доли рынка: полоса 2027 + засечка 2026 на той же шкале — вместо таблицы."""
    mv = max_value or max(max(it.get("prev") or 0, it.get("cur") or 0) for it in items)
    bw = w - label_w - 1.45
    bar_h = 0.20
    cy = y
    for it in items:
        by = cy + (row_h - bar_h) / 2
        sl.text(x, by - 0.02, label_w, 0.24, it["label"], size=size, weight=600,
                color=B.INK, line=1.05, fit=True, min_size=7.0)
        if it.get("cur") is not None:
            sl.rect(x + label_w, by, bw, bar_h, fill=B.SURFACE_2)
            sl.rect(x + label_w, by, max(0.03, bw * it["cur"] / mv), bar_h,
                    fill=it.get("color", B.YELLOW))
        if it.get("prev") is not None:
            px = x + label_w + bw * it["prev"] / mv
            sl.line(px, by - 0.045, px, by + bar_h + 0.045, B.INK, lw=1.1)
        if it.get("shift"):
            sl.text(x + label_w + bw + 0.12, by - 0.06, 1.20, 0.30, it["shift"],
                    size=value_size, weight=700, color=it.get("value_color", B.INK),
                    align="r", line=1.0)
        if it.get("delta"):
            dy = by + 0.21 if it.get("cur") is not None else by - 0.03
            sl.text(x + label_w + bw + 0.12, dy, 1.20, 0.20, it["delta"],
                    size=7.6, weight=600, color=it.get("delta_color", B.INK_3),
                    align="r", line=1.0)
        cy += row_h
    return cy


def chain(sl, x, y, w, steps, h=0.78, gap=0.14, size=8.6, numbered=True,
          fill=B.SURFACE, accent=B.YELLOW):
    """Цепочка звеньев с номерами — «что делаем по шагам»."""
    n = len(steps)
    cw = (w - gap * (n - 1)) / n
    for i, st in enumerate(steps):
        cx = x + i * (cw + gap)
        panel(sl, cx, y, cw, h, fill=fill)
        sl.rect(cx, y, cw, 0.05, fill=accent if i % 2 == 0 else B.YELLOW_SOFT)
        if numbered:
            sl.text(cx + 0.14, y + 0.12, 0.30, 0.24, "%02d" % (i + 1), size=8.6,
                    weight=700, color=B.YELLOW_DIM)
            tx = cx + 0.50
        else:
            tx = cx + 0.16
        sl.text(tx, y + 0.12, cw - (tx - cx) - 0.14, 0.26, st["title"], size=9.2,
                weight=700, color=B.INK, line=1.05, fit=True, min_size=7.6)
        if st.get("text"):
            sl.text(cx + 0.16, y + 0.40, cw - 0.30, h - 0.46, st["text"], size=size,
                    weight=400, color=B.INK_2, line=1.18, fit=True, min_size=6.8)
        if i < n - 1:
            sl.polygon([(cx + cw + 0.02, y + h / 2 - 0.07), (cx + cw + 0.10, y + h / 2),
                        (cx + cw + 0.02, y + h / 2 + 0.07)], B.LINE)


def ill(sl, name, x, y, w, opacity=1.0):
    """Фирменная векторная иллюстрация из assets."""
    path = os.path.join(ASSETS, name)
    sl.image(path, x, y, w)


def data_row(sl, x, y, w, items, gap=0.14, h=0.92, size=8.2, fill=B.SURFACE):
    """Компактная строка «2026 → 2027»: заменяет мини-таблицу из 2–4 строк."""
    n = len(items)
    cw = (w - gap * (n - 1)) / n
    for i, it in enumerate(items):
        cx = x + i * (cw + gap)
        panel(sl, cx, y, cw, h, fill=fill)
        sl.rect(cx, y, 0.05, h, fill=it.get("accent", B.YELLOW))
        sl.text(cx + 0.18, y + 0.09, cw - 0.32, 0.22, it["label"], size=7.6, weight=700,
                color=B.INK_3, caps=True, tracking=0.4, line=1.05, fit=True, min_size=6.2)
        cy = y + 0.32
        if it.get("from"):
            sl.text(cx + 0.18, cy, cw - 0.32, 0.26, "%s → %s" % (it["from"], it["to"]),
                    size=it.get("value_size", 13.0), weight=700, color=B.INK,
                    fit=True, min_size=9.0)
        else:
            sl.text(cx + 0.18, cy, cw - 0.32, 0.26, it.get("to", ""),
                    size=it.get("value_size", 13.0), weight=700, color=B.INK,
                    fit=True, min_size=9.0)
        if it.get("delta"):
            sl.text(cx + 0.18, y + h - 0.26, cw - 0.32, 0.20, it["delta"],
                    size=size - 0.4, weight=600, color=B.YELLOW_DIM, line=1.05)


def action_list(sl, x, y, w, items, row_h=0.66, gap=0.09, size=8.6,
                num_w=0.46, right_w=1.55, num_start=1, effect_size=10.6,
                term_size=8.2):
    """Список действий: номер, название, суть, срок и эффект — вместо таблицы."""
    cy = y
    for i, it in enumerate(items):
        panel(sl, x, cy, w, row_h, fill=B.SURFACE if i % 2 == 0 else B.SURFACE_2)
        sl.rect(x, cy, 0.05, row_h, fill=it.get("accent", B.YELLOW))
        # номер в фирменном домике — приём нумерации корпоративного шаблона
        num = "%02d" % (i + num_start)
        house_shape(sl, x + 0.19, cy + 0.10, 0.27, 0.25,
                    it.get("num_fill", B.DARK))
        sl.text(x + 0.19, cy + 0.115, 0.27, 0.23, num, size=7.6, weight=700,
                color=B.WHITE, align="c", valign="m", fit=True, min_size=5.6)
        tw = w - num_w - right_w - 0.50
        sl.text(x + 0.20 + num_w, cy + 0.10, tw, 0.24, it["title"], size=9.6,
                weight=700, color=B.INK, line=1.05, fit=True, min_size=7.8)
        sl.text(x + 0.20 + num_w, cy + 0.33, tw, row_h - 0.38, it["text"], size=size,
                weight=400, color=B.INK_2, line=1.16, fit=True, min_size=6.6)
        rx = x + w - right_w - 0.12
        if it.get("term"):
            sl.text(rx, cy + 0.10, right_w, 0.24, it["term"], size=term_size,
                    weight=600, color=B.INK_3, align="r")
        if it.get("effect"):
            sl.text(rx, cy + 0.32, right_w, 0.26, it["effect"], size=effect_size,
                    weight=700,
                    color=it.get("effect_color", B.INK), align="r", fit=True, min_size=8)
        cy += row_h + gap
    return cy - gap


def metrics_list(sl, x, y, w, items, row_h=0.34, size=9.2, value_size=9.6,
                 label_color=B.INK, fill=None):
    """Список «показатель — значение» без таблицы: тонкие линии и крупные цифры."""
    cy = y
    for i, it in enumerate(items):
        if fill and i % 2 == 0:
            sl.rect(x, cy, w, row_h, fill=fill)
        ind = it.get("indent", False)
        sl.text(x + 0.14 + (0.26 if ind else 0), cy, w - 2.35 - (0.26 if ind else 0),
                row_h, it["label"], size=size - (0.8 if ind else 0),
                weight=400 if ind else 600,
                color=it.get("label_color", B.INK_2 if ind else label_color),
                valign="m", line=1.1)
        sl.text(x + w - 2.20, cy, 2.06, row_h, it["value"], size=value_size, weight=700,
                color=it.get("color", B.INK), align="r", valign="m", line=1.1,
                fit=True, min_size=7.5)
        sl.line(x + 0.14, cy + row_h, x + w - 0.14, cy + row_h, B.LINE, lw=0.5)
        cy += row_h
    return cy
