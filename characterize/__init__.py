'''Tool for creating console printable images using ANSI escapes.'''
import click
import numpy as np
from PIL import Image

from . import colors

# TODO: Output to file
@click.command()
@click.argument('image', type=click.File('rb'))
@click.option('-w', '--width', type=click.IntRange(0), default=128)
@click.option('-h', '--height', type=click.IntRange(0), default=36)
@click.option('-f', '--foregrounds',
              default=','.join(tuple(map(str, range(30, 38)))))
@click.option('-b', '--backgrounds', 
              default=','.join(tuple(map(str, range(40, 48)))))
@click.option('-c', '--characters', default='█:0,▓:0.25,▒:0.5,░:.75')
@click.option('-m', '--mono-diff', default=False, is_flag=True)
@click.option('--debug', default=False, is_flag=True)
def main(image, width, height, foregrounds, backgrounds, characters, mono_diff, debug):
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

    diff_func = colors.color_diff_mono if mono_diff else colors.color_diff

    for row in img:
        for pixel in row:
            print(colors.to_ansi(pixel, palette=palette, diff_func=diff_func), end='')
        print()
