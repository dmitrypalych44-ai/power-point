"""«ЦПМ 75» — два сводных слайда в фирменном стиле колоды (светлая тема).

Содержание — из презентации заказчика «Стратегия ЦПМ 75» (7 слайдов):
склад и логистика, команда в пике, путь заказа и клиентский оффер в новостройки.
"""
from __future__ import annotations

from . import brand as B
from . import components as C
from .primitives import Slide


# --------------------------------------------------------------- helpers
def _kv(sl, x, y, w, label, value, size=13.0, label_size=7.6, rule=True, row_h=0.0):
    """Строка «подпись сверху — значение крупно» с тонкой отбивкой."""
    sl.text(x, y, w, 0.20, label, size=label_size, weight=400, color=B.INK_3,
            caps=True, tracking=0.5, fit=True, min_size=6.4)
    sl.text(x, y + 0.20, w, 0.30, value, size=size, weight=700, color=B.INK, line=1.0,
            fit=True, min_size=9.0)
    if rule and row_h:
        sl.line(x, y + row_h, x + w, y + row_h, B.LINE, lw=0.5)


def _mini(sl, x, y, w, h, value, label, accent=False):
    C.panel(sl, x, y, w, h, fill=B.YELLOW_FAINT if accent else B.SURFACE_2)
    sl.text(x + 0.14, y + 0.10, w - 0.28, 0.26, value, size=12.5, weight=700,
            color=B.INK, line=1.0, fit=True, min_size=9.0)
    sl.text(x + 0.14, y + 0.36, w - 0.28, 0.34, label, size=7.4, weight=400,
            color=B.INK_2, line=1.12, fit=True, min_size=6.4)


def _bar(sl, x, y, w, pct, h=0.10):
    sl.rect(x, y, w, h, fill=B.SURFACE_3)
    sl.rect(x, y, max(0.04, w * pct), h, fill=B.YELLOW)


# ------------------------------------------------- 1. склад и логистика
def warehouse():
    sl = Slide(1)
    C.head(sl, "переимплантация склада · гамма · доступность",
           "Склад наполняет полку магазина раньше, чем клиент придёт",
           "977 → 1 200 паллетомест, 1 700+ новых артикулов, обратный поток −34% "
           "и 720 м² крытой отгрузки", project="Логистика")
    y0 = B.CONTENT_Y

    C.kpi_row(sl, [
        dict(label="Ёмкость склада", value="977 → 1 200", note="+223 пм · +23%"),
        dict(label="Гамма подбора", value="1 700+", note="новых артикулов · 6 отделов"),
        dict(label="Обратный поток", value="37,7% → 25%", note="−34% к текущему уровню"),
        dict(label="Доступность товара", value="98%", note="цель на полке · +32,6% SKU"),
        dict(label="Эффект RD в год", value="29,9 млн ₽", note="упущенный ТО 23,1 млн ₽"),
    ], y0, h=1.14)
    y1 = y0 + 1.16 + 0.20

    gap = 0.18
    pw = (B.CW - 2 * gap) / 3
    ph = 2.80

    # --- склад: ёмкость, гамма, сборки под КЗ
    x = B.M
    C.panel(sl, x, y1, pw, ph, fill=B.SURFACE)
    sl.rect(x, y1, 0.05, ph, fill=B.YELLOW)
    sl.text(x + 0.24, y1 + 0.14, pw - 0.44, 0.24, "Склад и гамма", size=8.6, weight=700,
            color=B.INK, caps=True, tracking=0.6)

    sl.text(x + 0.24, y1 + 0.50, pw - 0.44, 0.20, "Сборки со склада под КЗ", size=8.2,
            weight=400, color=B.INK_3)
    sl.text(x + 0.24, y1 + 0.70, pw - 0.44, 0.32, "15% → 25%+", size=16.0, weight=700,
            color=B.INK, line=1.0)
    _bar(sl, x + 0.24, y1 + 1.06, pw - 0.48, 0.25 / 0.40)
    sl.text(x + 0.24, y1 + 1.18, pw - 0.44, 0.22, "доля сборок под клиентские заказы",
            size=7.6, weight=400, color=B.INK_2, fit=True, min_size=6.6)

    sl.bullets(x + 0.24, y1 + 1.50, pw - 0.44, 1.10, [
        "1 700+ артикулов подбора: отделы 4, 5, 8, 11, 12, 14",
        "+223 паллетоместа — место под сборку клиентских заказов",
        "Обратный поток 37,7% → 25%: −34% к текущему уровню",
    ], size=8.4, bullet="—", gap=0.08, line=1.18)

    # --- доступность товара
    x = B.M + pw + gap
    C.panel(sl, x, y1, pw, ph, fill=B.SURFACE)
    sl.rect(x, y1, 0.05, ph, fill=B.YELLOW)
    sl.text(x + 0.24, y1 + 0.14, pw - 0.44, 0.24, "Доступность товара", size=8.6, weight=700,
            color=B.INK, caps=True, tracking=0.6)

    sl.text(x + 0.24, y1 + 0.50, pw - 0.44, 0.20, "Цель доступности на полке", size=8.2,
            weight=400, color=B.INK_3)
    sl.text(x + 0.24, y1 + 0.70, pw - 0.44, 0.34, "98%", size=20.0, weight=700,
            color=B.INK, line=1.0)
    _bar(sl, x + 0.24, y1 + 1.10, pw - 0.48, 0.98)
    sl.text(x + 0.24, y1 + 1.22, pw - 0.44, 0.22, "+32,6% SKU доступности с удалённого склада",
            size=7.6, weight=400, color=B.INK_2, fit=True, min_size=6.6)

    sl.bullets(x + 0.24, y1 + 1.50, pw - 0.44, 1.10, [
        "Товары с RD — в склад магазина: полка не пустеет",
        "≥ 30 SKU/ч — нацеленность команды пополнения",
        "+1 МЦПМ в команде пополнения, сопровождение флоп-сотрудников",
    ], size=8.4, bullet="—", gap=0.08, line=1.18)

    # --- навес
    x = B.M + 2 * (pw + gap)
    C.panel(sl, x, y1, pw, ph, fill=B.SURFACE)
    sl.rect(x, y1, 0.05, ph, fill=B.YELLOW)
    sl.text(x + 0.24, y1 + 0.14, pw - 0.44, 0.24, "Удобство клиента · навес", size=8.6,
            weight=700, color=B.INK, caps=True, tracking=0.6)

    sl.text(x + 0.24, y1 + 0.50, pw - 0.44, 0.20, "Крытая зона отгрузки", size=8.2,
            weight=400, color=B.INK_3)
    sl.text(x + 0.24, y1 + 0.70, pw - 0.44, 0.34, "720 м²", size=20.0, weight=700,
            color=B.INK, line=1.0)

    chips = [("Сухо", "не мокнем под дождём и снегом"),
             ("Предсказуемо", "слоты держим по времени"),
             ("Безопасно", "ровное покрытие без луж и наледи"),
             ("Комфортно", "отдельная зона для доставок и заказов")]
    cy = y1 + 1.02
    for name, txt in chips:
        sl.rect(x + 0.24, cy + 0.11, 0.06, 0.10, fill=B.YELLOW)
        sl.text(x + 0.38, cy + 0.04, pw - 0.62, 0.19, name, size=8.2, weight=700, color=B.INK)
        sl.text(x + 0.38, cy + 0.21, pw - 0.62, 0.18, txt, size=7.4, weight=400,
                color=B.INK_2, fit=True, min_size=6.4)
        cy += 0.35

    sl.text(x + 0.24, y1 + ph - 0.32, pw - 0.44, 0.22,
            "CSAT 4,85 — цель · грузчик +1 в смену",
            size=7.4, weight=600, color=B.YELLOW_DIM, fit=True, min_size=6.2)

    C.callout(sl, B.M, y1 + ph + 0.14, B.CW, 0.50,
              "Склад перестаёт быть «местом хранения»: товар приезжает на полку магазина "
              "раньше, чем клиент придёт за ним.")
    C.footnote(sl, "Источники: данные заказчика — стратегия ЦПМ 75, переимплантация склада и доступность "
                   "товара, 2026–2027. RD — удалённый склад · КЗ — клиентский заказ · CSAT — оценка "
                   "клиента · SKU — товарная позиция.")
    return sl


# --------------------------------- 2. команда, путь заказа и новостройки
def team_and_client():
    sl = Slide(2)
    C.head(sl, "команда в пике · LT-поток · новостройки",
           "Команда в пике, короткий путь заказа и оффер в новостройки",
           "176 человек в пике нагрузки, 58 FTE снимает 3PL, новостройки — 400 млн ₽ GMV "
           "к концу 2027", project="Логистика")
    y0 = B.CONTENT_Y

    C.kpi_row(sl, [
        dict(label="Команда склада в пике", value="176 чел.", note="43 / 43 / 61 / 29 по участкам"),
        dict(label="Операционная нагрузка", value="58 FTE", note="снимаем с магазина на год"),
        dict(label="Время магазину", value="9 520 ч", note="возвращаем в год"),
        dict(label="GMV LT-отгрузок", value="+18%", note="прогноз к 2027 году"),
        dict(label="Оффер в новостройки", value="400 млн ₽", note="цель 2027 · ещё 10 ЖК"),
    ], y0, h=1.14)
    y1 = y0 + 1.16 + 0.20

    gap = 0.18
    pw = (B.CW - 2 * gap) / 3
    ph = 2.80

    # --- команда
    x = B.M
    C.panel(sl, x, y1, pw, ph, fill=B.SURFACE)
    sl.rect(x, y1, 0.05, ph, fill=B.YELLOW)
    sl.text(x + 0.24, y1 + 0.14, pw - 0.44, 0.24, "Команда в пике нагрузки", size=8.6,
            weight=700, color=B.INK, caps=True, tracking=0.6)

    mw = (pw - 0.48 - 0.12) / 2
    mh = 0.70
    for k, (val, lab) in enumerate([("43", "Складские операции"), ("43", "ОЗК"),
                                    ("61", "Пополнение"), ("29", "Выдача")]):
        mx = x + 0.24 + (k % 2) * (mw + 0.12)
        my = y1 + 0.50 + (k // 2) * (mh + 0.10)
        _mini(sl, mx, my, mw, mh, val, lab)

    sl.bullets(x + 0.24, y1 + 2.02, pw - 0.44, 0.72, [
        "Штат считаем от целевой продуктивности и закрываем на месяц раньше сезона",
        "Профессионализм: обучение, сертификация, совмещение профессий, кадровый резерв",
    ], size=7.8, bullet="—", gap=0.05, line=1.16)

    # --- путь заказа
    x = B.M + pw + gap
    C.panel(sl, x, y1, pw, ph, fill=B.SURFACE)
    sl.rect(x, y1, 0.05, ph, fill=B.YELLOW)
    sl.text(x + 0.24, y1 + 0.14, pw - 0.44, 0.24, "LT-поток: путь заказа", size=8.6,
            weight=700, color=B.INK, caps=True, tracking=0.6)

    steps = [("ШАГ 1 · ДАРКСТОР", "800+", "артикулов добавляется · отделы 2, 5, 6, 7, 14, 15"),
             ("ШАГ 2 · 3PL", "3PL", "партнёрская обработка и доставка — снимаем нагрузку"),
             ("ШАГ 3 · КЛИЕНТ", "Быстрее", "стабильные сроки, меньше ручных операций")]
    cy = y1 + 0.48
    for name, val, txt in steps:
        sl.text(x + 0.24, cy, pw - 0.44, 0.19, name, size=7.8, weight=700,
                color=B.YELLOW_DIM, tracking=0.5)
        sl.text(x + 0.24, cy + 0.18, pw - 0.44, 0.28, val, size=13.5, weight=700,
                color=B.INK, line=1.0, fit=True, min_size=9.5)
        sl.text(x + 0.24, cy + 0.46, pw - 0.44, 0.30, txt, size=7.4, weight=400,
                color=B.INK_2, line=1.14, fit=True, min_size=6.2)
        cy += 0.76

    # --- новостройки
    x = B.M + 2 * (pw + gap)
    C.panel(sl, x, y1, pw, ph, fill=B.SURFACE)
    sl.rect(x, y1, 0.05, ph, fill=B.YELLOW)
    sl.text(x + 0.24, y1 + 0.14, pw - 0.44, 0.24, "Клиентский оффер в новостройки", size=8.6,
            weight=700, color=B.INK, caps=True, tracking=0.6)

    rows = [("Сегодня", "60 млн ₽", "текущий GMV по 5 ЖК · 4% GMV доставки"),
            ("Конец 2026", "100 млн ₽", "прогноз по всем ЖК · +20 млн ₽"),
            ("Цель · конец 2027", "400 млн ₽", "ещё 10 новых ЖК в 2027")]
    cy = y1 + 0.48
    for k, (lab, val, note) in enumerate(rows):
        big = (k == 2)
        sl.text(x + 0.24, cy, pw - 0.44, 0.18, lab, size=7.6, weight=400,
                color=B.INK_3, caps=True, tracking=0.4)
        sl.text(x + 0.24, cy + 0.18, pw - 0.44, 0.30, val, size=15.0 if big else 12.5,
                weight=700, color=B.YELLOW_DIM if big else B.INK, line=1.0)
        sl.text(x + 0.24, cy + 0.48, pw - 0.44, 0.20, note, size=7.4, weight=400,
                color=B.INK_2, fit=True, min_size=6.2)
        cy += 0.72

    C.callout(sl, B.M, y1 + ph + 0.14, B.CW, 0.50,
              "Один склад, одна команда, понятный путь заказа — и клиент, который возвращается.")
    C.footnote(sl, "Источники: данные заказчика — стратегия ЦПМ 75 (команда склада, LT-поток, новостройки), 2026–2027. "
                   "5 ЖК сегодня и 5 с октября 2026 · 3PL — партнёрская логистика · ОЗК — обработка заказов клиентов · "
                   "FTE — полная занятость.")
    return sl


PAGES = [warehouse, team_and_client]
