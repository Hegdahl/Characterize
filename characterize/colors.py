'''Color translation'''

FG_COLORS = {
    30:(0, 0, 0),        # Black
    31:(170, 0, 0),      # Red
    32:(0, 170, 0),      # Green
    33:(170, 85, 0),     # Yellow
    34:(0, 0, 170),      # Blue
    35:(170, 0, 170),    # Magenta
    36:(0, 170, 170),    # Cyan
    37:(170, 170, 170),  # White

    90: (85, 85, 85),    # Bright Black
    91: (255, 85, 85),   # Bright Red
    92: (85, 255, 85),   # Bright Green
    93: (255, 255, 85),  # Bright Yellow
    94: (85, 85, 255),   # Bright Blue
    95: (255, 85, 255),  # Bright Magenta
    96: (85, 255, 255),  # Bright Cyan
    97: (255, 255, 255), # Bright White
}

BG_COLORS = {
    40: (0, 0, 0),        # Black
    41: (170, 0, 0),      # Red
    42: (0, 170, 0),      # Green
    43: (170, 85, 0),     # Yellow
    44: (0, 0, 170),      # Blue
    45: (170, 0, 170),    # Magenta
    46: (0, 170, 170),    # Cyan
    47: (170, 170, 170),  # White

    100: (85, 85, 85),    # Bright Black
    101: (255, 85, 85),   # Bright Red
    102: (85, 255, 85),   # Bright Green
    103: (255, 255, 85),  # Bright Yellow
    104: (85, 85, 255),   # Bright Blue
    105: (255, 85, 255),  # Bright Magenta
    106: (85, 255, 255),  # Bright Cyan
    107: (255, 255, 255), # Bright White
}

def lerp(f, c1, c2):
    return tuple(int((1-f)*v1+f*v2) for v1,v2 in zip(c1, c2))

def color_diff(c1, c2):
    return sum((v1-v2)**2 for v1,v2 in zip(c1, c2))\
        + (sum(c1)-sum(c2))**2/2

def color_diff_mono(c1, c2):
    return (sum(c1)-sum(c2))**2

def make_palette(fgs, bgs, characters):
    palette = {}
    for fg in fgs:
        for bg in bgs:
            for char, frac in characters:
                color = lerp(frac, FG_COLORS[fg], BG_COLORS[bg])
                palette[color] = fg, bg, char
    return palette

def to_ansi(target, palette, diff_func):
    best_diff = float('inf')
    best_ansi = None
    for color, ansi in palette.items():
        diff = diff_func(target, color)
        if diff < best_diff:
            best_diff = diff
            best_ansi = ansi

    fg, bg, char = best_ansi
    return f'\033[{fg};{bg}m{char}\033[m'
