"""SWOT-схема по колоде «Стратегия Владивосток 2027» — один слайд в фирменном стиле."""
from __future__ import annotations

from . import brand as B
from . import components as C
from .primitives import Slide

QUADS = [
    dict(letter="S", name="Сильные стороны", tag="финансовая база и работающие каналы",
         accent=B.YELLOW,
         items=["FY26: оборот 8,88 млрд ₽, GMV 9,17 млрд ₽, РХД 1,23 млрд ₽ — 16% к GMV",
                "Новосёлы: 4 099 в программе, 1 593 сделки (39,3%) — канал уже работает",
                "Логистика 977 → 1 200 пм; 3PL даёт 58 FTE и 9 520 ч магазину в год"]),
    dict(letter="W", name="Слабые стороны", tag="люди, срок и недобранный охват",
         accent=B.INK_2,
         items=["EXI 75,9% (−1,5 п.п.) и укомплектованность 91% при плане найма +27 чел.",
                "Охват новосёлов 13,3% против 18,5% у лидера, конверсия 39,3% против 44,6%",
                "Срок МП 3,5 — 23 дня; гибкие ресурсы 26% при цели 15%"]),
    dict(letter="O", name="Возможности", tag="стройка, ПРО и новые ЖК",
         accent=B.YELLOW_SOFT,
         items=["251 МКД — 70,1 млрд ₽ ёмкости; потенциал ПРО 30,7 млрд ₽ (доля 7,6%)",
                "Ещё 10 ЖК: 60 млн ₽ сегодня → 400 млн ₽ GMV к концу 2027",
                "Демарш Нижнего Новгорода: +5 п.п. охвата и конверсии без CAPEX"]),
    dict(letter="T", name="Угрозы", tag="разрыв плана и внешняя среда",
         accent=B.YELLOW_DIM,
         items=["Амбиция 10,18 против кадража 9,08 млрд ₽ — план выше тренда на 12%",
                "FY25 уже дал −6% оборота: рынок умеет падать",
                "Зависимость от партнёрского 3PL и сезонного найма в пик"]),
]

PRIORITIES = [
    ("SO · атаковать", "ЖК и ПРО под стройку: 400 млн ₽ и 3 млрд ₽"),
    ("WO · подтянуть", "Охват и конверсию новосёлов до уровня лидера"),
    ("ST · защитить", "EXI ≥ 78% и стабильность 77% при найме +27"),
    ("WT · не допустить", "План на гибких ресурсах 26% при цели 15%"),
]


def swot():
    sl = Slide(1)
    C.head(sl, "SWOT · СТРАТЕГИЯ 2027",
           "Что помогает и что мешает амбиции 10,18 млрд ₽",
           "Анализ колоды «Стратегия Владивосток 2027»: финансы FY26, ПРО, новосёлы, "
           "логистика и команда", raw=True)
    y0 = B.CONTENT_Y

    gap = 0.20
    qw = (B.CW - gap) / 2
    qh = 1.56
    rows_y = [y0 + 0.04, y0 + 1.72]

    for i, q in enumerate(QUADS):
        x = B.M + (i % 2) * (qw + gap)
        y = rows_y[i // 2]
        C.panel(sl, x, y, qw, qh, fill=B.SURFACE)
        sl.rect(x, y, 0.06, qh, fill=q["accent"])
        # буква в квадрате
        sl.rect(x + 0.24, y + 0.14, 0.30, 0.30, fill=q["accent"])
        sl.text(x + 0.24, y + 0.14, 0.30, 0.30, q["letter"], size=12.0, weight=700,
                color=B.WHITE if q["accent"] in (B.INK_2, B.YELLOW_DIM) else B.INK,
                align="c", valign="m", line=1.0)
        sl.text(x + 0.64, y + 0.14, qw - 0.90, 0.22, q["name"], size=10.5, weight=700,
                color=B.INK, caps=True, tracking=0.5, fit=True, min_size=8.4)
        sl.text(x + 0.64, y + 0.34, qw - 0.90, 0.18, q["tag"], size=7.4, weight=400,
                color=B.INK_3, fit=True, min_size=6.4)
        sl.bullets(x + 0.26, y + 0.64, qw - 0.50, qh - 0.70, q["items"], size=8.4,
                   bullet="—", gap=0.085, line=1.18)

    # приоритеты действий
    by = rows_y[1] + qh + 0.18
    cw = (B.CW - 3 * 0.14) / 4
    for i, (lab, txt) in enumerate(PRIORITIES):
        x = B.M + i * (cw + 0.14)
        C.panel(sl, x, by, cw, 0.86, fill=B.YELLOW_FAINT)
        sl.rect(x, by, 0.05, 0.86, fill=B.YELLOW)
        sl.text(x + 0.18, by + 0.10, cw - 0.32, 0.20, lab, size=7.4, weight=700,
                color=B.YELLOW_DIM, caps=True, tracking=0.4, fit=True, min_size=6.4)
        sl.text(x + 0.18, by + 0.32, cw - 0.32, 0.46, txt, size=8.0, weight=400,
                color=B.INK, line=1.16, fit=True, min_size=6.6)

    C.callout(sl, B.M, by + 1.00, B.CW, 0.48,
              "Сила колоды — «где расти» (стройка, ПРО, ЖК) и прибыль 16% к GMV; "
              "уязвимость — «кем и как»: команда, срок 23 дня и охват новосёлов.")
    C.footnote(sl, "Источники: колода «Лемана ПРО · Стратегия Владивосток 2027» (42 слайда), "
                   "данные заказчика — финансы FY24–FY26, ПРО, новосёлы, ЦПМ 75.")
    return sl


PAGES = [swot]
