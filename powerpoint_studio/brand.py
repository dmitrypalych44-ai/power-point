"""Brand system for Лемана ПРО (LM Pro) corporate presentations.

Only the corporate palette is used:
  core (внешнее + внутреннее):  #FFFFFF · #303738 · #FFC100
  derived tints of the corporate grey are used for panels/separators only.
"""

# --- core brand colours -------------------------------------------------
YELLOW = "FFC100"      # фирменный жёлтый
DARK = "303738"        # фирменный графит
WHITE = "FFFFFF"       # белый

# --- derived tints of the corporate palette (no foreign hues) -----------
PANEL = "3C4446"       # graphite +6% (подложка блока)
PANEL_2 = "454D4F"     # graphite +10% (активная подложка)
LINE = "5A6365"        # hairline on dark
GREY = "9AA0A1"        # вторичный текст (белый 62% на графите)
GREY_2 = "6E7678"      # третичный текст / подписи
DARK_TEXT = "303738"   # текст на белых карточках
YELLOW_DIM = "8A6A00"  # тёмный оттенок жёлтого (только для приглушённых баров)
YELLOW_SOFT = "FFD35C" # жёлтый 70% (второй тон диаграмм)

# --- typography ---------------------------------------------------------
FONT = "LM Main"       # корпоративный шрифт; фолбэк — системный sans
FONT_BOLD = "LM Main"

# --- geometry (inches) --------------------------------------------------
SLIDE_W = 13.333
SLIDE_H = 7.5

M = 0.62                       # левое/правое поле
CW = SLIDE_W - 2 * M           # ширина контентной области (12.09)
HEAD_KICKER = 0.42
HEAD_TITLE = 0.64
HEAD_SUB = 1.50
RULE_Y = 1.86
CONTENT_Y = 1.98
CONTENT_BOTTOM = 6.92
FOOTNOTE_Y = 7.04
