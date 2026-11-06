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


def prepare(sl, index=None, total=None):
    """Фон слайда: сетка «ромбами» и скошенный угол — рисуется ПОД контентом."""
    bg = []
    # лёгкая диагональная сетка в правом нижнем поле — фирменный приём
    class _Rec:
        def __init__(self):
            self.items = bg
        def line(self, x1, y1, x2, y2, color, lw=0.75, dash=None):
            bg.append(dict(t="line", x1=x1, y1=y1, x2=x2, y2=y2, color=color,
                           lw=lw, dash=dash))
        def polygon(self, points, fill, alpha=None, line=None, lw=1.0):
            bg.append(dict(t="poly", points=points, fill=fill, alpha=alpha,
                           line=line, lw=lw))
        def rect(self, x, y, w, h, fill=None, line=None, lw=0.75, radius=0.0, dash=None):
            bg.append(dict(t="rect", x=x, y=y, w=w, h=h, fill=fill, line=line,
                           lw=lw, radius=radius, dash=dash))
    rec = _Rec()
    # скошенный жёлтый уголок слева внизу
    rec.polygon([(0, B.SLIDE_H - 0.30), (0.30, B.SLIDE_H), (0, B.SLIDE_H)], B.YELLOW)
    sl.items = bg + sl.items


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
