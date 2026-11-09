"""Фирменные пиктограммы Лемана ПРО: линейная графика, графит + жёлтый акцент.

Стиль из корпоративной презентации: тонкий контур (≈3 pt), белая заливка,
жёлтый акцент внутри. Рисуем в Pillow с 4x суперсэмплингом и сохраняем в assets.
"""
from __future__ import annotations

import os

from PIL import Image, ImageDraw

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
DARK = (48, 55, 56, 255)
YELLOW = (255, 193, 0, 255)
YELLOW_SOFT = (255, 211, 92, 255)
GREY = (176, 181, 181, 255)
CLEAR = (0, 0, 0, 0)

S = 4            # суперсэмплинг
PX = 2.0         # экспорт: px на pt


class Pict:
    """Холст пиктограммы в «сетке» 100×100 (переводится в pt)."""

    def __init__(self, w_pt=72.0, h_pt=72.0, lw=3.0):
        self.w, self.h = w_pt, h_pt
        self.lw = lw
        self.img = Image.new("RGBA", (int(w_pt * S * 3), int(h_pt * S * 3)), CLEAR)
        self.d = ImageDraw.Draw(self.img)

    # координаты в процентах холста
    def _pt(self, x, y):
        k = S * 3.0 * 0.72
        return (x / 100.0 * self.w * k, y / 100.0 * self.h * k)

    def _xy(self, pts):
        return [self._pt(x, y) for x, y in pts]

    def poly(self, pts, fill=CLEAR, outline=DARK, width=None, close=True):
        self.d.polygon(self._xy(pts), fill=fill, outline=outline,
                       width=max(1, int((width or self.lw) * S * 1.4)))

    def rect(self, x, y, w, h, fill=CLEAR, outline=DARK, width=None, r=0.0):
        p = [self._pt(x, y), self._pt(x + w, y + h)]
        box = [p[0][0], p[0][1], p[1][0], p[1][1]]
        kw = dict(fill=fill, outline=outline, width=max(1, int((width or self.lw) * S * 1.4)))
        if r:
            self.d.rounded_rectangle(box, radius=r / 100.0 * self.w * S * 3.0, **kw)
        else:
            self.d.rectangle(box, **kw)

    def ellipse(self, cx, cy, rx, ry=None, fill=CLEAR, outline=DARK, width=None):
        ry = ry if ry is not None else rx
        a = self._pt(cx - rx, cy - ry)
        b = self._pt(cx + rx, cy + ry)
        self.d.ellipse([a[0], a[1], b[0], b[1]], fill=fill, outline=outline,
                       width=max(1, int((width or self.lw) * S * 1.4)))

    def line(self, pts, color=DARK, width=None):
        self.d.line(self._xy(pts), fill=color,
                    width=max(1, int((width or self.lw) * S * 1.4)), joint="curve")

    def save(self, name):
        os.makedirs(ASSETS, exist_ok=True)
        # обрезаем пустые поля по факту отрисовки
        bbox = self.img.getbbox()
        img = self.img.crop(bbox) if bbox else self.img
        out = img.resize((max(2, int(img.size[0] / (S * 0.72) * 0.5 * PX)),
                          max(2, int(img.size[1] / (S * 0.72) * 0.5 * PX))), Image.LANCZOS)
        path = os.path.join(ASSETS, "pic_" + name)
        out.save(path)
        return path


# ------------------------------------------------------------------ отделы
def p_stolyarka():
    c = Pict()
    # рама со створкой и рейки
    c.rect(18, 16, 64, 68, r=1.5)
    c.line([(50, 16), (50, 84)])
    c.rect(24, 24, 20, 26, fill=YELLOW, outline=DARK)
    c.rect(56, 24, 20, 26)
    c.rect(24, 58, 20, 18)
    c.rect(56, 58, 20, 18, fill=YELLOW_SOFT, outline=DARK)
    return c.save("stolyarka.png")


def p_kraski():
    c = Pict()
    c.rect(20, 34, 34, 46, r=1.5)
    c.poly([(20, 34), (54, 34), (54, 44), (20, 44)])
    c.rect(30, 20, 14, 14, fill=YELLOW, outline=DARK)   # крышка-банка
    # валик
    c.rect(60, 26, 24, 14, fill=YELLOW, r=4)
    c.line([(72, 40), (72, 66)])
    c.rect(62, 66, 20, 10, r=2)
    return c.save("kraski.png")


def p_decor():
    c = Pict()
    # рулон обоев
    c.rect(26, 20, 26, 60, r=2)
    c.ellipse(39, 20, 13, 5, fill=YELLOW_SOFT)
    c.ellipse(39, 20, 4, 1.6, fill=DARK, outline=DARK)
    # декоративная рейка
    for i in range(3):
        c.rect(60 + i * 10, 28, 6, 52, fill=YELLOW if i == 1 else CLEAR)
    return c.save("decor.png")


def p_pol():
    c = Pict()
    for i in range(2):
        for j in range(2):
            c.rect(20 + i * 32, 22 + j * 32, 28, 28,
                   fill=YELLOW if (i + j) % 2 == 0 else CLEAR)
    return c.save("pol.png")


def p_dveri():
    c = Pict()
    c.rect(24, 14, 40, 72, fill=YELLOW_SOFT, r=1.5)
    c.ellipse(56, 50, 2.6, fill=DARK, outline=DARK)
    c.rect(68, 14, 8, 72, fill=CLEAR)
    return c.save("dveri.png")


def p_vannaya():
    c = Pict()
    c.rect(16, 44, 46, 34, r=2)
    c.ellipse(39, 44, 23, 9, fill=YELLOW, outline=DARK)
    c.line([(68, 44), (68, 26)])
    c.line([(68, 26), (80, 26)])
    c.line([(80, 26), (80, 34)])
    c.rect(70, 66, 4, 12)
    return c.save("vannaya.png")


def p_kuhni():
    c = Pict()
    c.rect(14, 40, 72, 40)
    c.line([(14, 56), (86, 56)])
    c.rect(22, 20, 24, 18, fill=YELLOW)
    c.rect(52, 20, 24, 18)
    c.ellipse(30, 48, 2.4, fill=DARK, outline=DARK)
    c.ellipse(60, 48, 2.4, fill=DARK, outline=DARK)
    return c.save("kuhni.png")


def p_sad():
    c = Pict()
    c.poly([(30, 56), (66, 56), (60, 82), (36, 82)], fill=YELLOW)
    c.line([(48, 56), (48, 24)])
    c.ellipse(34, 34, 11, 6, fill=YELLOW_SOFT, outline=DARK)
    c.ellipse(62, 30, 11, 6, fill=YELLOW_SOFT, outline=DARK)
    c.ellipse(48, 18, 6, 8, fill=YELLOW_SOFT, outline=DARK)
    return c.save("sad.png")


def p_pro():
    c = Pict()
    # каска
    c.poly([(24, 52), (24, 40), (34, 26), (66, 26), (76, 40), (76, 52)], fill=YELLOW)
    c.rect(18, 52, 64, 8, fill=CLEAR)
    c.line([(50, 26), (50, 52)])
    # лист-смета
    c.rect(66, 62, 22, 22, fill=CLEAR)
    c.line([(70, 70), (84, 70)])
    c.line([(70, 76), (80, 76)])
    return c.save("pro.png")


def p_logistika():
    c = Pict()
    c.rect(10, 36, 46, 32, fill=YELLOW)
    c.rect(56, 44, 18, 24)
    c.line([(56, 56), (74, 56)])
    c.ellipse(24, 72, 6, fill=CLEAR)
    c.ellipse(66, 72, 6, fill=CLEAR)
    return c.save("logistika.png")


def p_komanda():
    c = Pict()
    for cx, fill in ((30, CLEAR), (50, YELLOW), (70, CLEAR)):
        c.ellipse(cx, 30, 9, fill=fill)
        c.poly([(cx - 15, 84), (cx - 15, 62), (cx, 48), (cx + 15, 62), (cx + 15, 84)],
               fill=fill)
    return c.save("komanda.png")


def p_itogi():
    c = Pict()
    c.line([(16, 84), (84, 84)], color=DARK)
    c.line([(16, 84), (16, 16)], color=DARK)
    for i, h in enumerate((20, 34, 48)):
        c.rect(26 + i * 20, 84 - h, 12, h, fill=YELLOW if i == 2 else CLEAR)
    return c.save("itogi.png")


def p_rynok():
    c = Pict()
    c.rect(12, 30, 22, 54)
    c.rect(39, 18, 22, 66, fill=YELLOW)
    c.rect(66, 44, 22, 40)
    return c.save("rynok.png")


def p_stena():
    c = Pict()
    c.rect(12, 16, 76, 68, r=1.5)
    c.poly([(12, 16), (88, 16), (88, 34), (12, 34)], fill=YELLOW_SOFT)
    c.line([(30, 44), (30, 78)])
    c.line([(44, 44), (44, 78)])
    c.line([(58, 44), (58, 78)])
    c.line([(72, 44), (72, 78)])
    return c.save("stena.png")


def p_whitebox():
    c = Pict()
    c.poly([(50, 16), (86, 34), (50, 52), (14, 34)], fill=YELLOW, outline=DARK)
    c.line([(14, 34), (14, 64), (50, 82), (86, 64), (86, 34)])
    c.line([(50, 52), (50, 82)])
    return c.save("whitebox.png")


def build_all():
    return [f() for f in (p_stolyarka, p_kraski, p_decor, p_pol, p_dveri, p_vannaya,
                          p_kuhni, p_sad, p_pro, p_logistika, p_komanda, p_itogi, p_rynok,
                          p_stena, p_whitebox)]


if __name__ == "__main__":
    for p in build_all():
        print(p)
