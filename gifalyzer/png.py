import os

from PIL import Image

from .util import humanize_size


def analyze_png(filepath):
    filesize = os.stat(filepath).st_size
    image = Image.open(filepath)
    initial_report = {
        'dimensions': image.size,
        'filesize': filesize,
        'humanized_filesize': humanize_size(filesize),
    }

    rgba = image.convert('RGBA')
    max_alpha = 0
    min_alpha = -1
    alpha = 0
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            r, g, b, a = rgba.getpixel((x, y))
            alpha += a
            if a < min_alpha or min_alpha == -1:
                min_alpha = a
            if a > max_alpha:
                max_alpha = a

    initial_report['avg_alpha'] = alpha/(image.size[0]*image.size[1])
    initial_report['max_alpha'] = max_alpha
    initial_report['min_alpha'] = min_alpha

    return initial_report
