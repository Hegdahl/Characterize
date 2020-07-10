'''Tool for creating console printable images using ANSI escapes.'''
import numpy as np
from PIL import Image
import click
from tqdm import tqdm

from . import colors

@click.command()
@click.argument('image', type=click.File('rb'))
@click.option('-w', '--width', type=click.IntRange(0), default=128)
@click.option('-h', '--height', type=click.IntRange(0), default=36)
@click.option('-fg', '--foregrounds',
              default=','.join(tuple(map(str, range(30, 38)))))
@click.option('-bg', '--backgrounds', 
              default=','.join(tuple(map(str, range(40, 48)))))
@click.option('-c', '--characters', default='█:0,▓:0.25,▒:0.5,░:.75')
@click.option('-m', '--mono-diff', default=False, is_flag=True)
@click.option('-o', '--output', type=click.Path(writable=True))
@click.option('-f', '--format', type=click.Choice(('raw', 'py', 'cpp')), default='raw')
def main(image, width, height, foregrounds, backgrounds, characters, mono_diff, output, format):
    img = np.array(Image.open(image).resize((width, height)))
    img = img/255

    foregrounds = tuple(map(int, foregrounds.split(',')))
    backgrounds = tuple(map(int, backgrounds.split(',')))
    characters = tuple((c, float(f)) for c, f in
                       (ele.split(':') for ele in
                        characters.split(',')))

    palette = colors.make_palette(
        foregrounds,
        backgrounds,
        characters,
    )

    diff_f = colors.color_diff_mono if mono_diff else colors.color_diff

    fmt_f = {
        'raw': lambda s: s,
        'py': lambda s: repr(s)[1:-1],
        'cpp': lambda s: s.replace('\033', '\\e')
    }[format]

    try:
        if output:
            file = open(output, 'w+')
            output_f = file.write

        else:
            output_f = lambda s: print(s, end='')

        show_progress = tqdm if output else lambda v: v

        for row in show_progress(img):
            prev_ansi = None
            for pixel in row:
                style, fg, bg, char = colors.closest(pixel, palette=palette, diff_func=diff_f)
                
                if (style, fg, bg) == prev_ansi:
                    pixel = char
                else:
                    pixel = f'\033[{style};{fg};{bg}m{char}'
                output_f(fmt_f(pixel))
                prev_ansi = (style, fg, bg)
            output_f(fmt_f('\033[m\n'))
    finally:
        if output:
            file.close()
