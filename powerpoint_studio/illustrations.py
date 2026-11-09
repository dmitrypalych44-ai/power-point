"""Фирменные иллюстрации: плоская геометрия в палитре Лемана ПРО.

Рисуем сами (Pillow, 4x supersampling), чтобы попасть в бренд-палитру точно:
жёлтый #FFC100, графит #303738, светлые тинты. Белый фон — прозрачность.
"""
from __future__ import annotations

import math
import os

from PIL import Image, ImageDraw

from . import brand as B

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

WHITE = (255, 255, 255)
YELLOW = (255, 193, 0)
YELLOW_DIM = (227, 172, 0)
YELLOW_SOFT = (255, 211, 92)
YELLOW_FAINT = (255, 241, 201)
DARK = (48, 55, 56)
INK_2 = (86, 93, 94)
GREY = (211, 214, 214)
GREY_2 = (225, 227, 227)
GREY_3 = (240, 241, 241)
EXPORT = 2.0  # множитель «px на pt» при экспорте

S = 4          # supersampling внутри


class Canvas:
    def __init__(self, w_in: float, h_in: float):
        self.w = w_in
        self.h = h_in
        self.img = Image.new("RGBA", (int(w_in * 72 * S), int(h_in * 72 * S)), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.img)

    def _p(self, x, y):
        return (x * 72 * S, y * 72 * S)

    def poly(self, pts, fill=None, outline=None, width=0.02):
        self.d.polygon([self._p(*p) for p in pts], fill=fill,
                       outline=outline, width=int(width * 72 * S) if outline else 0)

    def rect(self, x, y, w, h, fill=None, r=0.0, outline=None, width=0.02):
        box = [self._p(x, y), self._p(x + w, y + h)]
        box = [box[0][0], box[0][1], box[1][0], box[1][1]]
        kw = dict(fill=fill, outline=outline,
                  width=int(width * 72 * S) if outline else 0)
        if r:
            self.d.rounded_rectangle(box, radius=r * 72 * S, **kw)
        else:
            self.d.rectangle(box, **kw)

    def ellipse(self, cx, cy, rx, ry=None, fill=None, outline=None, width=0.02):
        ry = ry or rx
        x0, y0 = self._p(cx - rx, cy - ry)
        x1, y1 = self._p(cx + rx, cy + ry)
        self.d.ellipse([x0, y0, x1, y1], fill=fill, outline=outline,
                       width=int(width * 72 * S) if outline else 0)

    def arc(self, cx, cy, r, start, end, fill, width=0.05):
        x0, y0 = self._p(cx - r, cy - r)
        x1, y1 = self._p(cx + r, cy + r)
        self.d.arc([x0, y0, x1, y1], start, end, fill=fill,
                   width=int(width * 72 * S))

    def line(self, pts, fill, width=0.02):
        self.d.line([self._p(*p) for p in pts], fill=fill,
                    width=int(width * 72 * S), joint="curve")

    def save(self, name: str):
        os.makedirs(ASSETS, exist_ok=True)
        out = self.img.resize((int(self.w * 72 * EXPORT), int(self.h * 72 * EXPORT)),
                              Image.LANCZOS)
        path = os.path.join(ASSETS, name)
        out.save(path)
        return path


def house(c: Canvas, x, y, w, h, fill=DARK, door=None):
    """Дом с двускатной крышей — тот же силуэт, что в логотипе."""
    peak = y
    body_top = y + h * 0.34
    c.poly([(x, body_top), (x + w / 2, peak), (x + w, body_top), (x + w, y + h),
            (x, y + h)], fill=fill)
    if door:
        dw, dh = w * 0.26, h * 0.34
        c.rect(x + w / 2 - dw / 2, y + h - dh, dw, dh, fill=door, r=dw * 0.34)


# ------------------------------------------------------------------ сцены
def ill_house_blocks():
    """Обложка: дом в окружении «миров» — коробки-категории."""
    c = Canvas(4.6, 3.4)
    # фоновая сетка точками (брендовая «карта»)
    for gx in range(0, 11):
        for gy in range(0, 8):
            c.ellipse(0.35 + gx * 0.4, 0.3 + gy * 0.4, 0.022, fill=GREY_2)

    house(c, 1.66, 0.42, 1.30, 1.24, fill=DARK, door=YELLOW)
    # «полки» миров слева и справа
    left = [(0.18, 1.02, YELLOW), (0.18, 1.52, YELLOW_SOFT), (0.18, 2.02, GREY)]
    for x, y, col in left:
        c.rect(x, y, 1.05, 0.36, fill=col, r=0.05)
        c.rect(x + 0.82, y + 0.10, 0.16, 0.16, fill=WHITE, r=0.03)
    right = [(3.32, 1.12, GREY), (3.32, 1.62, YELLOW_SOFT), (3.32, 2.12, YELLOW)]
    for x, y, col in right:
        c.rect(x, y, 1.05, 0.36, fill=col, r=0.05)
        c.rect(x + 0.10, y + 0.10, 0.16, 0.16, fill=WHITE, r=0.03)
    # машинка-подъём снизу
    c.rect(1.55, 2.62, 1.52, 0.34, fill=YELLOW, r=0.04)
    c.rect(1.72, 2.48, 0.30, 0.14, fill=GREY, r=0.02)
    c.rect(2.62, 2.48, 0.30, 0.14, fill=GREY, r=0.02)
    for wx in (1.82, 2.50):
        c.ellipse(wx + 0.14, 3.02, 0.13, fill=DARK)
        c.ellipse(wx + 0.14, 3.02, 0.05, fill=GREY_3)
    return c.save("ill_cover.png")


def ill_stena():
    """Стена: три рулона обоев, валик и панель-рейка."""
    c = Canvas(4.2, 2.6)
    for gx in range(0, 10):
        for gy in range(0, 6):
            c.ellipse(0.3 + gx * 0.42, 0.28 + gy * 0.42, 0.02, fill=GREY_3)
    # рулоны
    for i, (x, col) in enumerate([(0.55, YELLOW), (1.24, YELLOW_SOFT), (1.93, GREY)]):
        c.rect(x, 0.62, 0.52, 1.55, fill=col, r=0.07)
        c.ellipse(x + 0.26, 0.62, 0.26, 0.085, fill=WHITE)
        c.ellipse(x + 0.26, 0.62, 0.10, 0.035, fill=col)
    # валик
    c.rect(2.66, 0.72, 0.86, 0.34, fill=DARK, r=0.10)
    c.rect(3.02, 1.04, 0.14, 0.86, fill=GREY, r=0.05)
    c.rect(2.86, 1.86, 0.46, 0.16, fill=YELLOW, r=0.06)
    # панель-рейка
    for i in range(5):
        c.rect(2.62 + i * 0.20, 2.20, 0.10, 0.30, fill=DARK if i % 2 == 0 else GREY)
    return c.save("ill_stena.png")


def ill_pol():
    """Пол: плоская раскладка плитки 3×2 и шов-линии."""
    c = Canvas(4.2, 2.0)
    for i in range(3):
        for j in range(2):
            c.rect(0.62 + i * 0.98, 0.42 + j * 0.60, 0.88, 0.50,
                   fill=YELLOW if (i + j) % 2 == 0 else YELLOW_SOFT, r=0.03)
    # «подложка» и клей
    c.rect(0.50, 1.66, 3.10, 0.10, fill=GREY)
    c.rect(0.50, 1.80, 1.30, 0.06, fill=GREY_2)
    for i in range(4):
        c.rect(2.02 + i * 0.40, 1.74, 0.28, 0.14, fill=DARK if i % 2 == 0 else GREY_2, r=0.02)
    return c.save("ill_pol.png")


def ill_dveri():
    """Двери: дверное полотно с ручкой и профиль коробки."""
    c = Canvas(3.6, 2.6)
    for gx in range(0, 8):
        for gy in range(0, 6):
            c.ellipse(0.32 + gx * 0.44, 0.3 + gy * 0.44, 0.02, fill=GREY_3)
    c.rect(0.62, 0.38, 1.28, 2.02, fill=YELLOW, r=0.05)
    c.rect(0.80, 0.58, 0.92, 0.66, fill=YELLOW_SOFT, r=0.03)
    c.rect(0.80, 1.40, 0.92, 0.80, fill=YELLOW_SOFT, r=0.03)
    c.ellipse(1.68, 1.28, 0.06, fill=DARK)
    c.rect(2.10, 0.38, 0.16, 2.02, fill=DARK)
    c.rect(2.36, 0.46, 0.92, 0.14, fill=GREY)
    c.rect(2.36, 2.30, 0.92, 0.14, fill=GREY)
    for i in range(3):
        c.rect(2.44 + i * 0.28, 0.92, 0.16, 0.16, fill=YELLOW_DIM, r=0.03)
    return c.save("ill_dveri.png")


def ill_vannaya():
    """Ванная: раковина, смеситель, плитка."""
    c = Canvas(4.2, 2.6)
    for gx in range(0, 10):
        for gy in range(0, 6):
            c.ellipse(0.3 + gx * 0.42, 0.28 + gy * 0.42, 0.02, fill=GREY_3)
    # тумба
    c.rect(0.70, 1.42, 1.90, 0.86, fill=DARK, r=0.05)
    c.rect(1.56, 1.62, 0.10, 0.46, fill=GREY, r=0.04)
    # раковина
    c.ellipse(1.65, 1.42, 1.05, 0.20, fill=YELLOW)
    c.ellipse(1.65, 1.36, 0.95, 0.16, fill=WHITE)
    # смеситель
    c.rect(1.58, 0.86, 0.14, 0.46, fill=DARK, r=0.05)
    c.arc(1.72, 0.90, 0.24, 180, 340, DARK, width=0.07)
    # плитка
    for i in range(2):
        for j in range(3):
            c.rect(2.94 + i * 0.40, 0.62 + j * 0.40, 0.36, 0.36,
                   fill=YELLOW_SOFT if (i + j) % 2 else GREY_2)
    return c.save("ill_vannaya.png")


def ill_kuhni():
    """Кухни: фасады, столешница, вытяжка."""
    c = Canvas(4.2, 2.6)
    for gx in range(0, 10):
        for gy in range(0, 6):
            c.ellipse(0.3 + gx * 0.42, 0.28 + gy * 0.42, 0.02, fill=GREY_3)
    c.rect(0.60, 0.58, 2.60, 1.86, fill=GREY_3, r=0.04)
    # верхние шкафы
    for i in range(3):
        c.rect(0.74 + i * 0.62, 0.72, 0.54, 0.62, fill=YELLOW if i == 1 else YELLOW_SOFT, r=0.03)
    # столешница
    c.rect(0.60, 1.46, 2.60, 0.12, fill=DARK)
    # нижние фасады
    for i in range(3):
        c.rect(0.74 + i * 0.62, 1.66, 0.54, 0.66, fill=GREY, r=0.03)
        c.rect(0.86 + i * 0.62, 1.74, 0.30, 0.05, fill=WHITE, r=0.02)
    # вытяжка
    c.poly([(1.28, 0.20), (1.88, 0.20), (2.02, 0.52), (1.14, 0.52)], fill=DARK)
    # остров
    c.rect(3.34, 1.20, 0.72, 1.24, fill=YELLOW, r=0.04)
    c.rect(3.24, 1.08, 0.92, 0.14, fill=YELLOW_DIM, r=0.05)
    return c.save("ill_kuhni.png")


def ill_sad():
    """Сад: растение, горшок, инструмент."""
    c = Canvas(4.2, 2.6)
    for gx in range(0, 10):
        for gy in range(0, 6):
            c.ellipse(0.3 + gx * 0.42, 0.28 + gy * 0.42, 0.02, fill=GREY_3)
    # горшок
    c.poly([(1.08, 1.76), (2.32, 1.76), (2.16, 2.42), (1.24, 2.42)], fill=YELLOW)
    c.rect(1.02, 1.64, 1.36, 0.16, fill=YELLOW_DIM, r=0.05)
    # стебель и листья
    c.line([(1.70, 1.66), (1.70, 0.86)], fill=DARK, width=0.07)
    for sx, sy, rx in [(1.34, 1.10, 0.26), (2.06, 1.10, 0.26), (1.70, 0.72, 0.22)]:
        c.ellipse(sx, sy, rx, 0.17, fill=DARK)
    # лейка
    c.rect(2.92, 1.42, 0.72, 0.52, fill=GREY, r=0.06)
    c.poly([(3.62, 1.50), (3.94, 1.20), (3.98, 1.30), (3.70, 1.60)], fill=GREY)
    c.arc(3.16, 1.36, 0.20, 200, 340, DARK, width=0.05)
    # трава
    for i in range(4):
        c.line([(2.72 + i * 0.09, 2.40), (2.78 + i * 0.09, 2.14)], fill=DARK, width=0.04)
    return c.save("ill_sad.png")


def ill_pro():
    """ПРО: каска, смета, ящик инструментов."""
    c = Canvas(4.2, 2.6)
    for gx in range(0, 10):
        for gy in range(0, 6):
            c.ellipse(0.3 + gx * 0.42, 0.28 + gy * 0.42, 0.02, fill=GREY_3)
    # каска
    c.arc(1.28, 1.34, 0.60, 180, 360, YELLOW, width=0.34)
    c.rect(0.62, 1.30, 1.32, 0.12, fill=YELLOW_DIM, r=0.04)
    # смета (лист с строками)
    c.rect(2.24, 0.62, 0.92, 1.24, fill=WHITE, r=0.03, outline=GREY, width=0.02)
    for i in range(4):
        c.rect(2.40, 0.84 + i * 0.24, 0.60 if i % 2 == 0 else 0.42, 0.08,
               fill=DARK if i == 0 else GREY, r=0.02)
    # ящик инструментов
    c.rect(1.86, 2.06, 1.44, 0.42, fill=DARK, r=0.05)
    c.rect(2.36, 1.94, 0.44, 0.12, fill=GREY, r=0.04)
    c.rect(3.54, 1.62, 0.12, 0.86, fill=YELLOW, r=0.05)
    c.rect(3.42, 1.42, 0.36, 0.22, fill=YELLOW_DIM, r=0.04)
    return c.save("ill_pro.png")


def ill_logistika():
    """Логистика: фура, паллеты, стрелка."""
    c = Canvas(4.2, 2.6)
    for gx in range(0, 10):
        for gy in range(0, 6):
            c.ellipse(0.3 + gx * 0.42, 0.28 + gy * 0.42, 0.02, fill=GREY_3)
    # прицеп
    c.rect(0.62, 0.86, 2.06, 1.24, fill=GREY_3, r=0.04, outline=GREY, width=0.02)
    for i in range(3):
        c.rect(0.78 + i * 0.62, 1.04, 0.48, 0.86, fill=YELLOW if i != 1 else YELLOW_SOFT, r=0.03)
    # кабина
    c.poly([(2.76, 0.98), (3.42, 0.98), (3.72, 1.42), (3.72, 2.10), (2.76, 2.10)], fill=DARK)
    c.rect(3.02, 1.10, 0.44, 0.34, fill=YELLOW_FAINT, r=0.03)
    for wx in (1.12, 1.98, 3.26):
        c.ellipse(wx + 0.22, 2.14, 0.22, fill=DARK)
        c.ellipse(wx + 0.22, 2.14, 0.09, fill=GREY_3)
    # паллеты
    for i in range(2):
        c.rect(3.86, 0.62 - i * 0.26, 0.0, 0.0, fill=YELLOW)
    c.rect(3.80, 1.70, 0.30, 0.10, fill=YELLOW_DIM)
    return c.save("ill_logistika.png")


def ill_komanda():
    """Команда: три фигуры и общий результат."""
    c = Canvas(4.2, 2.6)
    for gx in range(0, 10):
        for gy in range(0, 6):
            c.ellipse(0.3 + gx * 0.42, 0.28 + gy * 0.42, 0.02, fill=GREY_3)
    people = [(0.86, GREY, 0.0), (1.86, YELLOW, 0.20), (2.86, DARK, 0.0)]
    for x, col, dy in people:
        c.ellipse(x + 0.32, 0.92 + dy, 0.20, fill=col)
        c.poly([(x, 2.06), (x, 1.52), (x + 0.32, 1.28), (x + 0.64, 1.52), (x + 0.64, 2.06)],
               fill=col)
    # восходящие столбики
    for i, h in enumerate([0.30, 0.52, 0.78]):
        c.rect(3.52 + i * 0.22, 2.10 - h, 0.14, h, fill=YELLOW if i == 2 else GREY)
    c.line([(3.46, 2.14), (3.98, 2.14)], fill=DARK, width=0.03)
    return c.save("ill_komanda.png")


def ill_plan():
    """Планы и метрики: график роста и чек-лист."""
    c = Canvas(4.2, 2.6)
    for gx in range(0, 10):
        for gy in range(0, 6):
            c.ellipse(0.3 + gx * 0.42, 0.28 + gy * 0.42, 0.02, fill=GREY_3)
    # оси
    c.line([(0.66, 0.52), (0.66, 2.24), (3.52, 2.24)], fill=GREY, width=0.03)
    # столбики роста
    for i, h in enumerate([0.34, 0.52, 0.74, 1.06, 1.42]):
        c.rect(0.92 + i * 0.46, 2.24 - h, 0.30, h, fill=YELLOW if i >= 3 else YELLOW_SOFT, r=0.03)
    c.line([(1.07, 1.78), (1.53, 1.58), (1.99, 1.36), (2.45, 1.04), (2.91, 0.70)],
           fill=DARK, width=0.05)
    for i, h in enumerate([1.78, 1.58, 1.36, 1.04, 0.70]):
        c.ellipse(1.07 + i * 0.46, h, 0.06, fill=DARK)
    # чек-лист
    for i in range(3):
        c.rect(3.52, 0.72 + i * 0.34, 0.16, 0.16, fill=YELLOW, r=0.03)
        c.rect(3.76, 0.78 + i * 0.34, 0.32, 0.05, fill=GREY)
    return c.save("ill_plan.png")


def build_all():
    return [ill_house_blocks(), ill_stena(), ill_pol(), ill_dveri(), ill_vannaya(),
            ill_kuhni(), ill_sad(), ill_pro(), ill_logistika(), ill_komanda(), ill_plan()]


if __name__ == "__main__":
    for p in build_all():
        print(p)
