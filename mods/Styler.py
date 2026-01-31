# This mod renders a professional gradient banner and colored logo
import os

def reg(mgr):
    mgr.sub('start', show_ui)

def get_color(step, total):
    # Градиент от фиолетового (200, 50, 255) к синему (50, 150, 255)
    r = int(200 + (50 - 200) * step / total)
    g = int(50 + (150 - 50) * step / total)
    b = int(255 + (255 - 255) * step / total)
    return f"\033[38;2;{r};{g};{b}m"

def show_ui():
    from Ingram.utils import logo as ingram_logo
    
    # 1. Рисуем полоску из твоего ТЗ
    bar_text = " INGRAM MOD MANAGER v1.0.0.1 "
    w = 80
    pad = (w - len(bar_text)) // 2
    full_bar = " " * pad + bar_text + " " * (w - len(bar_text) - pad)
    
    bar_out = ""
    for i, char in enumerate(full_bar):
        # Цвета для фона полоски (чуть темнее)
        br = int(150 + (30 - 150) * i / w)
        bg = int(30 + (100 - 30) * i / w)
        bb = int(200 + (220 - 200) * i / w)
        bar_out += f"\033[48;2;{br};{bg};{bb}m\033[38;2;255;255;255;1m{char}"
    print(f"\n{bar_out}\033[0m\n")

    # 2. Рисуем сам логотип Ingram с градиентом
    for left, right in zip(*ingram_logo):
        line = f"{left}  {right}"
        colored_line = ""
        line_len = len(line)
        for i, char in enumerate(line):
            colored_line += f"{get_color(i, line_len)}{char}"
        print(colored_line + "\033[0m")
    print("\n" + "—" * w + "\n")