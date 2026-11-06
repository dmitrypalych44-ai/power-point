"""Слайды 9–14: проект «Пол» (свод, CJM, страт-миры) и проект «Двери»."""
from __future__ import annotations

import os

from . import brand as B
from . import components as C
from .backends import table_height
from .primitives import Slide, text_width

A = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")


def _init_cards(sl, x, y, w, items, cols=2, card_h=1.34, gap=0.16, size=8.4,
                title_size=9.6):
    """Сетка карточек «страт-мир: эффект + инициативы»."""
    cw = (w - gap * (cols - 1)) / cols
    for i, it in enumerate(items):
        cx = x + (i % cols) * (cw + gap)
        cy = y + (i // cols) * (card_h + gap)
        C.panel(sl, cx, cy, cw, card_h)
        sl.rect(cx, cy, 0.05, card_h, fill=it.get("color", B.YELLOW))
        sl.text(cx + 0.22, cy + 0.12, cw - 1.30, 0.22, it["name"], size=8.2, weight=700,
                color=it.get("color", B.YELLOW), caps=True, tracking=0.7)
        sl.text(cx + cw - 1.15, cy + 0.10, 0.95, 0.26, it["effect"], size=11, weight=700,
                color=B.INK, align="r")
        if it.get("note"):
            sl.text(cx + 0.22, cy + 0.34, cw - 0.44, 0.20, it["note"], size=7.4,
                    weight=400, color=B.INK_3, line=1.1)
        sl.bullets(cx + 0.22, cy + 0.56, cw - 0.42, card_h - 0.66, it["items"],
                   size=size, bullet="—", gap=0.05, line=1.2)


# ---------------------------------------------------------------- 9. Пол: свод
def pol_summary():
    sl = Slide(9)
    C.head(sl, "свод",
           "Амбиция 1 900 млн ₽ — 63% рынка ПОЛ в зоне охвата",
           "Магазин 75, Владивосток · покрытия, плитка, клей · Катя Колпакова + Дима Терентьев", project="Пол")
    y0 = B.CONTENT_Y

    C.kpi_row(sl, [
        dict(label="GMV проекта ПОЛ, амбиция 2027", value="1 900 млн ₽",
             note_prefix="2026: 1 510", note="· +25,8%"),
        dict(label="Темп роста к 2026", value="+390 млн ₽",
             note_prefix="магазин", note="+12,7%"),
        dict(label="Доля на рынке ПОЛ", value="63%",
             note_prefix="2026: 56%", note="· ▲ +7 п.п."),
        dict(label="Доля ПОЛ в GMV магазина", value="20,7%",
             note_prefix="2026: 18,6%", note="· ▲ +2,2 п.п."),
    ], y0, h=1.14, value_size=22)
    y1 = y0 + 1.32

    # рынок
    lw = 5.45
    C.section_head(sl, B.M, y1, lw, "Рынок ПОЛ в зоне охвата", size=13.5)
    C.data_row(sl, B.M, y1 + 0.46, lw, [
        dict(label="Рынок ПОЛ, млрд ₽", **{"from": "2,70"}, to="3,00", delta="+11%",
             accent=B.SERIES[0], value_size=14),
        dict(label="Доля Лемана ПРО", **{"from": "56%"}, to="63%", delta="+7 п.п.",
             accent=B.SERIES[1], value_size=14),
        dict(label="GMV проекта", **{"from": "1 510"}, to="1 900", delta="+25,8%",
             accent=B.SERIES[2], value_size=12.5),
    ], h=1.00)

    cy = y1 + 1.62
    sl.text(B.M, cy, lw, 0.22, "Основные конкуренты", size=8.6, weight=700, color=B.INK_2,
            caps=True, tracking=0.7)
    sl.text(B.M, cy + 0.26, lw, 0.34,
            "Красный Мамонт · Полы от Жабы · VoDvore · Шахтинская плитка · Kerama Marazzi",
            size=8.4, weight=600, color=B.INK, line=1.22)
    sl.text(B.M, cy + 0.60, lw, 0.34,
            "+ онлайн: Ozon, Wildberries, AliExpress забирают 42% восприятия «низкой цены»",
            size=8.0, weight=400, color=B.INK_2, line=1.2)

    # откуда рост
    rx = B.M + lw + 0.38
    rw = B.SLIDE_W - B.M - rx
    C.section_head(sl, rx, y1, rw, "Откуда рост +390 млн ₽: 4 страт-мира", size=13.5)
    C.hbars(sl, rx, y1 + 0.56, rw, [
        dict(label="ПРО · 57%", value=330, value_label="+330", label_color=B.INK_2,
             color=B.YELLOW),
        dict(label="Доступность · 17%", value=98, value_label="+98", label_color=B.INK_2,
             color=B.SERIES[1]),
        dict(label="МП2 · 15%", value=88, value_label="+88", label_color=B.INK_2,
             color=B.SERIES[2]),
        dict(label="МП4 · 11%", value=63, value_label="+63", label_color=B.INK_2,
             color=B.SERIES[3]),
    ], row_h=0.46, label_w=2.15, bar_h=0.17, value_w=0.70, size=9.6)

    C.callout(sl, rx, y1 + 2.40, rw, 0.58,
              "Гросс-потенциал инициатив — 579 млн ₽; в план заложен нетто +390 млн ₽ "
              "(коэф. 0,67).", size=8.4)

    # профиль клиента
    C.panel(sl, B.M, 6.42, B.CW, 0.48, fill=B.PANEL_2)
    sl.text(B.M + 0.22, 6.42, 1.85, 0.48, "ПРОФИЛЬ КЛИЕНТА", size=8.0, weight=700,
            color=B.INK, caps=True, tracking=0.7, valign="m")
    seg = [("48%", "B2C «делает сам»"), ("32%", "B2C «делает бригада»"),
           ("20%", "B2B / ПРО")]
    for i, (v, lb) in enumerate(seg):
        x = B.M + 2.24 + i * 2.10
        sl.text(x, 6.42, 0.66, 0.48, v, size=12.0, weight=700, color=B.INK, valign="m")
        sl.text(x + 0.68, 6.42, 1.32, 0.48, lb, size=7.8, weight=400, color=B.INK_2,
                line=1.15, valign="m")
    sl.text(B.M + 8.80, 6.42, 3.20, 0.48,
            "Целевой клиент — B2C, который выбирает покрытие сам, а сопутку доверяет мастеру",
            size=7.8, weight=400, color=B.INK_2, line=1.2, valign="m")

    C.footnote(sl, "Источники: BI ЛП 2026; Досье рынка 2026–2027, магазин 75. Допущения: рынок ПОЛ 2027 — "
                   "3,0 млрд ₽; GMV магазина 75 — 9 170 млн ₽ (+12,65%). Сегментация — после 12.11.2026.")
    return sl


# ---------------------------------------------------------------- 10. Пол: CJM
def pol_cjm():
    sl = Slide(10)
    C.head(sl, "путь клиента",
           "Четыре разрыва и 390 млн ₽: лечим межзвенья, а не полку",
           "Клиент уходит не из-за цены — он теряется на стыках этапов", project="Пол")
    y0 = B.CONTENT_Y

    steps = [
        ("1. Потребность", "Сдача новостройки, покупка квартиры, точечный или срочный ремонт",
         "Не знает объём, этапы и стоимость «пола под ключ»; нет калькулятора и контента",
         "Калькулятор «пол под ключ», UGC-контент, шоурум-зона «ПОЛ», партнёрства с ЖК",
         "Конверсия знание → посещение: 52% → 58%"),
        ("2. Поиск и выбор", "Онлайн-поиск и сравнение, консультация мастера, отзывы",
         "Нет онлайн-наличия и цены по 75-му; не вдохновляет контент; мастер не с нами",
         "Онлайн-витрина пола, гео-оффер, 3 решения под бюджет, рефералка ПРО",
         "Доля онлайн в GMV ПОЛ: 12% → 20%"),
        ("3. Покупка", "Офлайн сам или с мастером, онлайн-оформление, докупка сопутки",
         "Покрытие — у нас, клей, затирка и плинтус — в Ozon; нет корзины «товар + услуга»",
         "Единая корзина «товар + услуга», комплектность чека, цена топ-100 SKU",
         "Attach rate 1,8 → 2,4; комплектные чеки 20% → 35%"),
        ("4. Доставка и работы", "Самовывоз или доставка, приёмка, монтаж, гарантия",
         "Разные сроки, бой керамогранита, срыв монтажа, нет единого окна",
         "Окно доставки 2 часа по зоне 90 минут, жёсткая упаковка, OTIF-контроль",
         "OTIF 88% → 95%; бой при доставке −30%"),
        ("5. Повторная покупка", "Расширение ремонта, следующий объект мастера, рекомендации",
         "Нет системной передачи лида от мастера; лояльность ПРО не закреплена",
         "Рефералка ПРО (до 10 000 ₽/мес), Ключ-карта ПРО (до 4%), B2B-портал, КАМ",
         "200 мастеров-партнёров; повторные чеки ПРО +8 п.п."),
    ]
    cols = [1.62, 2.70, 2.62, 2.62, 2.30]
    heads = ["ЭТАП", "ЧТО ДЕЛАЕТ КЛИЕНТ", "БАРЬЕР", "НАШЕ ДЕЙСТВИЕ", "МЕТРИКА 2027"]
    xs = [B.M]
    for c in cols[:-1]:
        xs.append(xs[-1] + c + 0.08)
    for i, h in enumerate(heads):
        sl.text(xs[i], y0, cols[i], 0.22, h, size=7.4, weight=700,
                color=B.INK_3, tracking=0.7)

    cy = y0 + 0.26
    rh = 0.80
    for i, (name, does, barrier, action, metric) in enumerate(steps):
        C.panel(sl, B.M, cy, B.CW, rh, fill=B.PANEL_2 if i < 4 else B.PANEL)
        if i < 4:
            sl.rect(B.M, cy, 0.05, rh, fill=B.YELLOW)
        sl.text(xs[0] + 0.18, cy + 0.06, cols[0] - 0.22, rh - 0.12, name, size=9.4,
                weight=700, color=B.INK, line=1.14, valign="m")
        sl.text(xs[1], cy + 0.06, cols[1] - 0.06, rh - 0.12, does, size=7.9, weight=400,
                color=B.INK_2, line=1.2, valign="m")
        sl.text(xs[2], cy + 0.06, cols[2] - 0.06, rh - 0.12, barrier, size=7.9, weight=400,
                color=B.INK_2, line=1.2, valign="m")
        sl.text(xs[3], cy + 0.06, cols[3] - 0.06, rh - 0.12, action, size=7.9, weight=400,
                color=B.INK, line=1.2, valign="m")
        sl.text(xs[4], cy + 0.06, cols[4], rh - 0.12, metric, size=7.9, weight=600,
                color=B.INK if i < 4 else B.INK_3, line=1.2, valign="m")
        cy += rh + 0.06

    C.callout(sl, B.M, 6.30, B.CW, 0.56,
              "Связка «единая корзина (товар + услуги) + реферальная программа мастеров + OTIF 95%» "
              "закрывает 3 из 4 точек потери и даёт 236 из 390 млн ₽ прироста.", size=9.0)
    C.footnote(sl, "Источники: CJM категории «Напольные покрытия» (федеральная стратегия категории); "
                   "Досье рынка 2026–2027, магазин 75; реферальная программа ПРО, сентябрь 2026.")
    return sl


# ------------------------------------------------------ 11. Пол: страт-миры
def pol_worlds():
    sl = Slide(11)
    C.head(sl, "страт-миры",
           "Четыре мира: ПРО даёт 57% прироста, зал и доступность — ещё треть",
           "Эффект на GMV проекта ПОЛ — +390 млн ₽ · магазин 75, Владивосток 2027", project="Пол")
    y0 = B.CONTENT_Y

    worlds = [
        dict(name="ПРО · драйвер № 1", effect="+330", note="57% прироста · B2B, мастера, застройщики, КРТ",
             items=["Эксперт по полу и смета в торговом зале — профи приоритет",
                    "Рефералка ПРО и Ключ-карта с кэшбэком",
                    "Спецгамма и особые условия оплаты, ЭДО, КАМ"]),
        dict(name="Доступность", effect="+98", note="17% прироста · ассортимент и сроки",
             color=B.INK,
             items=["+50 артикулов SPC и +200 керамогранита",
                    "1–3 дня с РЦ Хабаровск вместо 7–10",
                    "OSA топ-SKU 92% → 97%, буфер по топ-100"]),
        dict(name="МП2 · торговый зал", effect="+88", note="15% прироста · концепт отдела и стена выбора",
             color=B.INK_2,
             items=["Стена выбора в 5 и 6 отделах: образцы на одном фронте",
                    "Сценарии «под бюджет» 3 × 3 и весь декор в натуре",
                    "−50% времени клиента на расчёт и оформление"]),
        dict(name="МП4 · проектный центр", effect="+63", note="11% прироста · проект и дизайн",
             color=B.SERIES[3],
             items=["+2 СПП: дизайн-проект пола за 3 рабочих дня",
                    "Каждый 4-й проект — с товарами отдела",
                    "Средний чек проекта в 2,5–3 раза выше розничного"]),
    ]
    cw = (B.CW - 3 * 0.16) / 4
    for i, wd in enumerate(worlds):
        x = B.M + i * (cw + 0.16)
        C.panel(sl, x, y0, cw, 2.86)
        sl.rect(x, y0, cw, 0.05, fill=wd.get("color", B.YELLOW))
        hcol = B.INK if i in (0, 2) else B.INK_2
        sl.text(x + 0.22, y0 + 0.22, cw - 0.44, 0.22, wd["name"], size=8.2, weight=700,
                color=hcol, caps=True, tracking=0.7)
        sl.text(x + 0.22, y0 + 0.52, cw - 0.44, 0.42, wd["effect"] + " млн ₽", size=20,
                weight=700, color=B.INK, line=1.0)
        sl.text(x + 0.22, y0 + 0.96, cw - 0.44, 0.4, wd["note"], size=8.2, weight=400,
                color=B.INK_2, line=1.22)
        sl.rect(x + 0.22, y0 + 1.42, cw - 0.44, 0.012, fill=B.LINE)
        sl.bullets(x + 0.22, y0 + 1.54, cw - 0.42, 1.2, wd["items"], size=8.2,
                   bullet="—", gap=0.06, line=1.24)

    # метрики 2027
    cy = y0 + 3.04
    C.section_head(sl, B.M, cy, 4.0, "Метрики проекта 2027", size=11.5)
    metrics = [
        ("OSA топ-SKU пола", "92% → 97%"),
        ("Срок поставки с РЦ", "7–10 → 1–3 дня"),
        ("Конверсия «посещение → покупка»", "70% → 74%"),
        ("Доля B2B / ПРО в GMV", "20% → 26%"),
        ("Доля проекта «Пол» в ПМ", "17% → 25%"),
    ]
    mw = (B.CW - 4 * 0.14) / 5
    for i, (lb, v) in enumerate(metrics):
        x = B.M + i * (mw + 0.14)
        C.panel(sl, x, cy + 0.44, mw, 0.78, fill=B.PANEL_2)
        sl.text(x + 0.16, cy + 0.54, mw - 0.32, 0.3, v, size=11.5, weight=700, color=B.INK)
        sl.text(x + 0.16, cy + 0.86, mw - 0.32, 0.32, lb, size=7.8, weight=400, color=B.INK_2,
                line=1.15)

    C.footnote(sl, "Источники: BI ЛП 2026; расчёт инициатив проекта ПОЛ; магазин 75. "
                   "Распределение эффекта по страт-мирам — расчётная модель, требует подтверждения BI.")
    return sl


# --------------------------------------------------- 12. Пол: инициативы
def pol_initiatives():
    sl = Slide(13)
    C.head(sl, "18 инициатив · доступность и зал",
           "Доступность и зал: 10 инициатив на +186 млн ₽",
           "Ассортимент, сроки и стена выбора · Владивосток, 2027", project="Пол")
    y0 = B.CONTENT_Y

    lw = 6.05
    rw = B.CW - lw - 0.30
    rx = B.M + lw + 0.30

    def col_head(x, w, title, total):
        sl.rect(x, y0, 0.05, 0.24, fill=B.YELLOW)
        sl.text(x + 0.18, y0 - 0.03, w - 1.70, 0.28, title, size=11.2, weight=700,
                color=B.INK, caps=True, tracking=0.7, fit=True, min_size=9.0)
        sl.text(x + w - 1.70, y0 - 0.04, 1.70, 0.30, total, size=13.5, weight=700,
                color=B.INK, align="r")

    col_head(B.M, lw, "Доступность · 6 инициатив", "+98 млн ₽")
    C.action_list(sl, B.M, y0 + 0.44, lw, [
        dict(title="+50 артикулов SPC", text="SPC 33–43 кл., выкладка стеной, подложка",
             term="Q1", effect="21 млн ₽"),
        dict(title="+200 артикулов керамогранита", text="60×60 и 120×60, мат и полированный",
             term="Q1", effect="52 млн ₽"),
        dict(title="+1 поставщик с РЦ Хабаровск", text="Влагостойкий ламинат, срок 1 день",
             term="Q1", effect="6 млн ₽"),
        dict(title="Срок с ДС Хабаровск до 3 дней", text="Автозаказ по ABC, буфер топ-100 SKU",
             term="Q2", effect="9 млн ₽"),
        dict(title="Регионализация плинтуса", text="Полистирол и ПВХ: срок до 3 дней",
             term="Q2", effect="6 млн ₽"),
        dict(title="Сток с УС на склад", text="Оборотный капитал и оборачиваемость",
             term="Q2", effect="4 млн ₽"),
    ], row_h=0.66, gap=0.085, size=9.0, right_w=1.05, effect_size=10.2, term_size=7.8)

    col_head(rx, rw, "МП2 · 4 инициативы", "+88 млн ₽")
    C.action_list(sl, rx, y0 + 0.44, rw, [
        dict(title="Стена выбора в отделах", text="5 и 6 отделы: крупные образцы на фасаде",
             term="Q1", effect="30 млн ₽"),
        dict(title="Больше образцов в натуре", text="Плитка, ламинат, плинтусы в выкрасе",
             term="Q1", effect="24 млн ₽"),
        dict(title="−50% времени на процессы", text="Расчёт «пол под ключ», самовывоз 15 мин",
             term="Q2", effect="12 млн ₽"),
        dict(title="Штат МК: +4 и +2", text="Пики, выходные, эксперт по полу",
             term="Q1–Q2", effect="22 млн ₽"),
    ], row_h=0.66, gap=0.085, size=9.0, right_w=1.05, effect_size=10.2, term_size=7.8)

    C.callout(sl, rx, y0 + 3.44, rw, 1.16,
              "186 млн ₽ = 98 Доступность + 88 МП2. Вторая половина эффекта «Пола» — "
              "18 инициатив ПРО и МП4 на следующем слайде.", size=9.6)

    C.footnote(sl, "Источники: расчёт инициатив проекта ПОЛ, магазин 75; BI ЛП 2026. "
                   "Эффект — вклад инициативы в прирост GMV 2027, млн ₽.")
    return sl


# ------------------------------------------- 14. Пол: инициативы ПРО и МП4
def pol_initiatives_pro():
    sl = Slide(14)
    C.head(sl, "18 инициатив · ПРО и проекты",
           "ПРО и проектный мир: 8 инициатив на +393 млн ₽",
           "Профи в зале, комплекты с клеем и проект пола за 3 дня · 2027", project="Пол")
    y0 = B.CONTENT_Y

    lw = 7.05
    rw = B.CW - lw - 0.28
    rx = B.M + lw + 0.28

    def col_head(x, w, title, total):
        sl.rect(x, y0, 0.05, 0.24, fill=B.YELLOW)
        sl.text(x + 0.18, y0 - 0.03, w - 1.75, 0.28, title, size=11.2, weight=700,
                color=B.INK, caps=True, tracking=0.7, fit=True, min_size=8.6)
        sl.text(x + w - 1.75, y0 - 0.04, 1.75, 0.30, total, size=13.5, weight=700,
                color=B.INK, align="r")

    col_head(B.M, lw, "ПРО · 4 инициативы", "+330 млн ₽")
    C.action_list(sl, B.M, y0 + 0.44, lw, [
        dict(title="МП5 · напольные покрытия", text="Профи в зале: эксперт, смета, резерв под объект",
             term="1П", effect="80 млн ₽"),
        dict(title="МП5 · плитка", text="Керамогранит и плитка, комплект с клеем",
             term="1П", effect="92 млн ₽"),
        dict(title="МП3 · напольные покрытия", text="Ламинат, SPC, ковролин под бюджет",
             term="2П", effect="72 млн ₽"),
        dict(title="МП3 · плитка", text="Крупный формат под новостройки и КРТ",
             term="2П", effect="86 млн ₽"),
    ], row_h=0.72, gap=0.09, size=9.4, right_w=1.30, effect_size=10.4, term_size=8.0)

    col_head(rx, rw, "МП4 · 2 инициативы", "+63 млн ₽")
    C.action_list(sl, rx, y0 + 0.44, rw, [
        dict(title="+2 СПП на проект «Пол»", text="Проект пола за 3 рабочих дня",
             term="Q1", effect="40 млн ₽"),
        dict(title="Каждый 4-й проект с полом", text="Проникновение в проектный мир",
             term="Q2", effect="23 млн ₽"),
    ], row_h=0.72, gap=0.09, size=9.2, right_w=1.10, effect_size=10.2, term_size=8.0)

    C.callout(sl, rx, y0 + 2.10, rw, 1.42,
              "МП5 — доля в проектном мире 11 → 17%, МП3 — 32 → 35%. "
              "Клей и подложка идут в чеке с покрытием — не отдельной покупкой.", size=9.4)


    # итог проекта
    cy = y0 + 3.72
    C.panel(sl, B.M, cy, 5.85, 1.14, fill=B.YELLOW_FAINT)
    sl.text(B.M + 0.26, cy + 0.16, 3.2, 0.26, "Итого проект «Пол»", size=10.0, weight=700,
            color=B.INK, caps=True, tracking=0.7)
    sl.text(B.M + 0.26, cy + 0.48, 3.4, 0.46, "+390 млн ₽", size=22, weight=700, color=B.INK)
    sl.text(B.M + 0.26, cy + 0.90, 5.3, 0.22, "нетто к базе 2026 → 1 900 млн ₽ в 2027",
            size=9.2, weight=400, color=B.INK_2)

    C.panel(sl, B.M + 6.05, cy, B.CW - 6.05, 1.14, fill=B.PANEL)
    sl.text(B.M + 6.31, cy + 0.16, 5.0, 0.26, "18 инициатив четырёх миров", size=10.0,
            weight=700, color=B.INK, caps=True, tracking=0.7)
    sl.text(B.M + 6.31, cy + 0.50, B.CW - 6.55, 0.50,
            "Гросс-потенциал 579 млн ₽; в план заложено нетто 390 млн ₽ (коэф. 0,67).",
            size=9.6, weight=400, color=B.INK_2, line=1.24)

    C.footnote(sl, "Источники: расчёт инициатив проекта ПОЛ, магазин 75; BI ЛП 2026. "
                   "ПРО 330 + Доступность 98 + МП2 88 + МП4 63 = 579 млн ₽ гросс, в план — нетто 390 млн ₽.")
    return sl


# ---------------------------------------------------------------- 13. Двери
def dveri():
    sl = Slide(13)
    C.head(sl, "свод",
           "356 млн ₽: +56% г-г и 28,5% рынка Приморья",
           "Входные, межкомнатные, фурнитура · Алексей Гладуненко + Дмитрий Колганов", project="Двери")
    y0 = B.CONTENT_Y

    C.kpi_row(sl, [
        dict(label="GMV 2026 · факт", value="228 млн ₽", note_prefix="+19%", note="г-1 · 21 ранг"),
        dict(label="Амбиция 2027", value="356 млн ₽", note_prefix="+56%", note="г-1 · 8 ранг, +13"),
        dict(label="Доля рынка проекта", value="28,5%", note_prefix="2026: 18,2%", note="· +10,3 п.п."),
        dict(label="Рынок проекта, Приморье", value="1,25 млрд ₽",
             note_prefix="двери 800", note="· входные 250 · фурнитура 200"),
    ], y0, h=1.14, value_size=21)
    y1 = y0 + 1.30

    # слева: три категории
    lw = 6.05
    C.section_head(sl, B.M, y1, lw, "Категории и наши доли", size=13.0)
    C.priority_columns(sl, B.M, y1 + 0.42, lw, [
        dict(title="225 · Межкомнатные", value="159,7", note="млн ₽ · рынок 800 млн ₽",
             text="Доля 20% · +25,7% г-1. Ядро проекта — 70% GMV.", h=1.62,
             accent=B.SERIES[0]),
        dict(title="210 · Входные", value="37,2", note="млн ₽ · рынок 250 млн ₽",
             text="Доля 15% · +10,0% г-1. Рост — установка МКД.", h=1.62,
             accent=B.SERIES[1]),
        dict(title="1005 · Фурнитура", value="31,4", note="млн ₽ · рынок 200 млн ₽",
             text="Доля 16% · +0,1% г-1. Сток ручек на ДС.", h=1.62,
             accent=B.SERIES[2]),
        dict(title="Итого · Двери", value="228,3", note="млн ₽ · рынок 1,25 млрд ₽",
             text="Доля 18,2% · +19,0%. Цель 2027 — 356 млн ₽.",
             h=1.62, accent=B.YELLOW, head_fill=B.INK),
    ], col_gap=0.12, head_h=0.42, size=7.8)

    # доступность
    cy = y1 + 2.24
    C.section_head(sl, B.M, cy, lw, "Доступность и путь клиента", size=13.0)
    sl.bullets(B.M, cy + 0.38, lw, 1.4, [
        "SAR 32,7% (−0,3 п.п.) → амбиция 60% (+27,3 п.п.); ДС 263 вместо 5 дней — 3 дня",
        "На ДС 263 — 52 коллекции, +2 согласованы; на ДС Новосибирск — 25 коллекций",
        "5 коллекций СТМ на ДС 263 дают 30 млн ₽ в год; ручки и фурнитура — на сток ДС",
        "8 проектов клиента держим на стоке, чтобы закрывать сделку без ожидания",
    ], size=8.2, bullet="—", gap=0.03, line=1.22)

    # справа: два вектора
    rx = B.M + lw + 0.34
    rw = B.SLIDE_W - B.M - rx
    C.section_head(sl, rx, y1, rw, "ПРО и МП4: два вектора роста", size=13.0)
    C.panel(sl, rx, y1 + 0.42, rw, 1.16)
    sl.text(rx + 0.20, y1 + 0.52, rw - 0.4, 0.20, "ПРО · 61,7 → 100 млн ₽ в канале", size=8.4,
            weight=700, color=B.INK, caps=True, tracking=0.6)
    sl.text(rx + 0.20, y1 + 0.72, rw - 0.4, 0.34,
            "Рост — объекты, мастера-партнёры и дотация на установку за счёт скидки на дверь.",
            size=8.2, weight=400, color=B.INK_2, line=1.22)
    for i, (v, lb) in enumerate([("28 → 48", "profi · +70% · база 28 млн ₽"),
                                 ("32,7 → 52", "B2B · +59% · база 32,7 млн ₽")]):
        x = rx + 0.20 + i * (rw / 2 - 0.10)
        sl.text(x, y1 + 1.02, rw / 2 - 0.30, 0.28, v, size=11.6, weight=700, color=B.INK)
        sl.text(x, y1 + 1.28, rw / 2 - 0.30, 0.28, lb, size=7.6, weight=400, color=B.INK_2,
                line=1.12)

    C.panel(sl, rx, y1 + 1.62, rw, 1.62, fill=B.PANEL_2)
    sl.text(rx + 0.20, y1 + 1.70, rw - 0.4, 0.20, "МП4 · 76,3 → 180 млн ₽ (+89%)", size=8.4,
            weight=700, color=B.INK, caps=True, tracking=0.7)
    C.stat_cards(sl, rx + 0.16, y1 + 1.94, rw - 0.32, [
        dict(label="GMV МП4", value="76,3 → 180", note="+89%", pct=0.9, accent=B.SERIES[0]),
        dict(label="Сделки", value="1 654 → 2 800", note="+69%", pct=0.75,
             accent=B.SERIES[1]),
        dict(label="Конверсия", value="71 → 75,2%", note="+4,2 п.п.", pct=0.6,
             accent=B.SERIES[2]),
        dict(label="Сделки с услугой", value="31 → 40%", note="+9 п.п.", pct=0.5,
             accent=B.SERIES[3]),
    ], per_row=2, gap=0.10, h=0.62, size=7.4)

    C.footnote(sl, "Рынок — млн ₽; доля рынка — расчёт от рынка 1 250 млн ₽; конкуренты — магазины на "
                   "Бородинской и специализированные сети. Источники: данные заказчика и BI ЛП 2026 по проекту "
                   "«Двери», магазин 75. Демарш Н. Новгород (119): GMV 279 млн ₽, 6-й ранг (+13), +27,9% г-1. "
                   "Амбиция ПРО на 2027 в источнике не подписана (18 / 16 млн ₽ — ниже базы), взята модель "
                   "канала +10 млн ₽ к базе 61,7 млн ₽ и распределена по структуре 2026.")
    return sl


# --------------------------------------------------- 14. Двери: метрики
def dveri_plan():
    sl = Slide(14)
    C.head(sl, "метрики и план",
           "Рычаги: срок 3 дня, услуга в чеке и сделки с бюджетом",
           "Контроль ежемесячно: SAR, конверсия СПП, доля сделок с услугой и лиды", project="Двери")
    y0 = B.CONTENT_Y

    # ---- слева: показатели
    lw = 6.20
    C.section_head(sl, B.M, y0, lw, "Показатели и цели 2027", size=13.5)
    C.metrics_list(sl, B.M, y0 + 0.44, lw, [
        dict(label="SAR · доступность на полке", value="32,7% → 60%"),
        dict(label="Срок получения товара с ДС", value="5 → 3 дня"),
        dict(label="Доля сделок с услугой установки", value="28% → 40%"),
        dict(label="МП4 · GMV", value="62 → 120 млн ₽"),
        dict(label="МП4 · сделки", value="1 250 → 2 200"),
        dict(label="МП4 · конверсия", value="73% → 75,2%"),
        dict(label="МП4 · доля новосёлов", value="27% · 16,5 млн ₽"),
        dict(label="Штат СПП", value="6 · 4 + 2 в ПЦ"),
    ], row_h=0.40, size=9.4, value_size=10.4, fill=B.SURFACE)

    cy = y0 + 3.86
    C.panel(sl, B.M, cy, lw, 0.72, fill=B.PANEL)
    sl.rect(B.M, cy, 0.06, 0.72, fill=B.YELLOW)
    sl.text(B.M + 0.24, cy + 0.08, lw - 0.48, 0.22, "Ориентир: демарш Тюмень 1 (031)", size=8.4,
            weight=700, color=B.INK, caps=True, tracking=0.6)
    sl.text(B.M + 0.24, cy + 0.32, lw - 0.48, 0.32,
            "GMV 102 млн ₽ (+37%), 2 317 сделок, конверсия 72%; Хабаровск 123 — SAR 66%.",
            size=9.4, weight=400, color=B.INK_2, line=1.22)

    # ---- справа: инициативы
    rx = B.M + lw + 0.32
    rw = B.SLIDE_W - B.M - rx
    C.section_head(sl, rx, y0, rw, "Инициативы 2027", size=13.5)
    C.action_list(sl, rx, y0 + 0.44, rw, [
        dict(title="Доступность",
             text="ДС 263: 52 коллекции +2; Новосибирск — 25 коллекций; 5 коллекций СТМ дают "
                  "30 млн ₽/год; ручки и фурнитура на сток ДС",
             accent=B.SERIES[0]),
        dict(title="Ассортимент",
             text="100% дверей на стоке: прямые поставки ДМ и СПГ, партнёрка со Штыковскими "
                  "Дверями, 8 проектов клиента на стоке", accent=B.SERIES[1]),
        dict(title="Услуга",
             text="Установка МКД: +1–2 мастера, ИП Морозов, воронка 2 партнёра; дотация "
                  "«дверь + установка −10%»", accent=B.SERIES[2]),
        dict(title="Проект",
             text="Рост за счёт состава проекта и бюджета сделки +5% (72 тыс. ₽), а не быстрых "
                  "сделок в Presale", accent=B.SERIES[3]),
        dict(title="ПРО",
             text="УТП и представление дверей для ПРО, НЦКД за счёт маржи СТМ, круглый стол, "
                  "лиды из МП3 и МП5", accent=B.YELLOW),
    ], row_h=0.80, gap=0.09, size=8.4, right_w=0.02)

    C.footnote(sl, "Источники: данные заказчика по проекту «Двери» (МП4 — 62 → 120 млн ₽, 1 250 → 2 200 "
                   "сделок, конверсия 73% → 75,2%, доля сделок с услугой 28% → 40%); BI ЛП 2026; карточка "
                   "DEMARSH. Цель 96 млн ₽ — нижняя граница амбиции МП4 из источника.")
    return sl


PAGES = [pol_summary, pol_cjm, pol_worlds, pol_initiatives, pol_initiatives_pro,
         dveri, dveri_plan]
