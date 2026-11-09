"""Фирменная «рама» слайда: жёлтая кромка справа, прогресс выпуска и знаки-домики.

Приёмы взяты из корпоративного шаблона Лемана ПРО:
  · жёлтая полоса по правому краю слайда (как на слайде «Привет!»);
  · графитовые знаки-домики как маркеры нумерации и подзаголовков;
  · срезанный угол и диагональная сетка на тёмных вставках.
"""
from __future__ import annotations

from . import brand as B

STRIPE_W = 0.13          # ширина жёлтой кромки по правому краю
EDGE_X = B.SLIDE_W - STRIPE_W


def house_outline(sl, x, y, w, h, color=B.WATER, lw=2.4, peak=0.34):
    """Контур дома из брендбука — светлый водяной знак подложки."""
    pts = [(x, y + h), (x, y + h * peak), (x + w / 2, y), (x + w, y + h * peak),
           (x + w, y + h)]
    for i in range(len(pts) - 1):
        sl.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], color, lw=lw)


def _lattice(sl, x0, y0, x1, y1, fill, step, lw=0.55):
    w, h = x1 - x0, y1 - y0
    n = int((w + h) / step) + 2
    for k in range(-n, n + 1):
        t = k * step
        for slope in (1, -1):
            pts = []
            for px in (x0, x1):
                py = (px - x0) * slope + t + y0
                if y0 - 0.01 <= py <= y1 + 0.01:
                    pts.append((px, py))
            for py in (y0, y1):
                px = (py - y0 - t) / slope + x0
                if x0 - 0.01 <= px <= x1 + 0.01:
                    pts.append((px, py))
            if len(pts) >= 2:
                (ax, ay), (bx, by) = pts[0], pts[-1]
                sl.line(ax, ay, bx, by, fill, lw=lw)


def _inside(pt, poly):
    """Точка внутри простого многоугольника (ray casting)."""
    x, y = pt
    res = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            xi = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x < xi:
                res = not res
    return res


def _hatch_tri(sl, poly, color, step=0.26, lw=0.6, n=140):
    """Диагональная штриховка внутри многоугольника: отрезки обрезаются по точкам."""
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    k = 0
    m = int((x1 - x0 + y1 - y0) / step) + 2
    for k in range(-m, m + 1):
        t = k * step
        a = (x0, t + y0)
        b = (x1, (x1 - x0) + t + y0)
        run = []
        for i in range(n + 1):
            f = i / float(n)
            pt = (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)
            if _inside(pt, poly):
                run.append(pt)
            elif run:
                if len(run) >= 2:
                    sl.line(run[0][0], run[0][1], run[-1][0], run[-1][1], color, lw=lw)
                run = []
        if len(run) >= 2:
            sl.line(run[0][0], run[0][1], run[-1][0], run[-1][1], color, lw=lw)


def _hatch(sl, x0, y0, x1, y1, color=B.HATCH, step=0.30, lw=0.6, dirn=1):
    """Диагональная штриховка под 45° внутри прямоугольника (обрезается по краю)."""
    n = int((x1 - x0 + y1 - y0) / step) + 3
    for k in range(-n, n + 1):
        t = k * step
        pts = []
        for px in (x0, x1):
            py = (px - x0) * dirn + t + y0
            if y0 - 0.005 <= py <= y1 + 0.005:
                pts.append((px, py))
        for py in (y0, y1):
            px = (py - y0 - t) / dirn + x0
            if x0 - 0.005 <= px <= x1 + 0.005:
                pts.append((px, py))
        if len(pts) >= 2:
            (ax, ay), (bx, by) = pts[0], pts[-1]
            sl.line(ax, ay, bx, by, color, lw=lw)


class _Bg:
    """Запись фоновых примитивов в отдельный список (уходит под контент)."""

    def __init__(self):
        self.items = []

    def rect(self, x, y, w, h, fill=None, line=None, lw=0.75, radius=0.0, dash=None):
        self.items.append(dict(t="rect", x=x, y=y, w=w, h=h, fill=fill, line=line,
                               lw=lw, radius=radius, dash=dash))

    def line(self, x1, y1, x2, y2, color, lw=0.75, dash=None):
        self.items.append(dict(t="line", x1=x1, y1=y1, x2=x2, y2=y2, color=color,
                               lw=lw, dash=dash))

    def polygon(self, points, fill, alpha=None, line=None, lw=1.0):
        self.items.append(dict(t="poly", points=points, fill=fill, alpha=alpha,
                               line=line, lw=lw))


def prepare(sl, index=None, total=None):
    """Фон слайда: бумажная подложка, тонированная шапка, штриховка по углам.

    Рисуется ПОД контентом — примитивы ставятся в начало списка. Приёмы:
    диагональная штриховка и срезанный угол из фирменных вставок шаблона,
    тёплая плашка шапки, отделяющая заголовок от содержания.
    """
    bg = _Bg()
    W, H = B.SLIDE_W, B.SLIDE_H
    body = B.CONTENT_Y - 0.06      # низ шапки

    # 1. тёплая бумажная основа вместо чистого белого
    bg.rect(0, 0, W, H, fill=B.PAPER)
    # 2. тёплая плашка шапки
    bg.rect(0, 0, W, body, fill=B.HEAD_TINT)
    # 3. жёлтый клин со срезом справа сверху — под фирменным домиком
    wedge = [(W - 3.05, 0), (W - STRIPE_W, 0), (W - STRIPE_W, 1.16)]
    bg.polygon(wedge, B.HEAD_WEDGE)
    _hatch_tri(bg, wedge, B.HEAD_WEDGE_LINE, step=0.26, lw=0.7)
    # 4. линия отбивки шапки
    bg.rect(0, body, W, 0.012, fill=B.HEAD_LINE)
    # 5. светлая диагональная штриховка в нижнем левом поле
    _hatch(bg, 0, H - 1.44, 1.92, H - 0.54, dirn=-1, color=B.HATCH)
    # 6. поля сноски: узкая тонированная полоса внизу
    bg.rect(0, H - 0.52, W - STRIPE_W, 0.52, fill=B.FOOT_TINT)
    # 7. скошенный жёлтый уголок слева внизу
    bg.polygon([(0, H - 0.30), (0.30, H), (0, H)], B.YELLOW)

    sl.items = bg.items + sl.items


def paper(sl):
    """Тёплая основа для обложки и финала — без рамы и штриховки."""
    sl.items.insert(0, dict(t="rect", x=0, y=0, w=B.SLIDE_W, h=B.SLIDE_H,
                            fill=B.PAPER, line=None, lw=0.75, radius=0.0,
                            dash=None))


def frame(sl, index=None, total=None):
    """Передний план рамы: жёлтая кромка справа и прогресс выпуска графитом."""
    sl.rect(EDGE_X, 0, STRIPE_W, B.SLIDE_H, fill=B.YELLOW)
    if index and total:
        frac = max(0.02, min(1.0, index / float(total)))
        hh = (B.SLIDE_H - 1.1) * frac
        sl.rect(EDGE_X, 0.55, STRIPE_W, hh, fill=B.DARK)
        sl.polygon([(EDGE_X, 0.55 + hh), (B.SLIDE_W, 0.55 + hh),
                    (B.SLIDE_W, 0.55 + hh + 0.08), (EDGE_X, 0.55 + hh + 0.16)],
                   B.DARK)
