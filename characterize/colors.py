'''Color translation'''

FG_COLORS_NORMAL = {
    30: (0, 0, 0),        # Black
    31: (170, 0, 0),      # Red
    32: (0, 170, 0),      # Green
    33: (170, 85, 0),     # Yellow
    34: (0, 0, 170),      # Blue
    35: (170, 0, 170),    # Magenta
    36: (0, 170, 170),    # Cyan
    37: (170, 170, 170),  # White
}

FG_COLORS_BRIGHT = {
    30: (85, 85, 85),    # Black
    31: (255, 85, 85),   # Red
    32: (85, 255, 85),   # Green
    33: (255, 255, 85),  # Yellow
    34: (85, 85, 255),   # Blue
    35: (255, 85, 255),  # Magenta
    36: (85, 255, 255),  # Cyan
    37: (255, 255, 255), # White
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
}

def lerp(f, c1, c2):
    return tuple(int((1-f)*v1+f*v2) for v1,v2 in zip(c1, c2))

def color_diff(c1, c2):
    return sum((v1-v2)**2 for v1,v2 in zip(c1, c2))

def color_diff_mono(c1, c2):
    return (sum(c1)-sum(c2))**2

def make_palette(fgs, bgs, characters):
    palette = {}

    for fg in fgs:
        for bg in bgs:
            for char, frac in characters:
                color = tuple(v/255 for v in lerp(frac, FG_COLORS_NORMAL[fg], BG_COLORS[bg]))
                palette[color] = 0, fg, bg, char

    for fg in fgs:
        for bg in bgs:
            for char, frac in characters:
                color = tuple(v/255 for v in lerp(frac, FG_COLORS_BRIGHT[fg], BG_COLORS[bg]))
                palette[color] = 1, fg, bg, char

    return palette

def closest(target, palette, diff_func):
    best_diff = float('inf')
    best_ansi = None
    for color, ansi in palette.items():
        diff = diff_func(target, color)
        if diff < best_diff:
            best_diff = diff
            best_ansi = ansi

    return best_ansi
