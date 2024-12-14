"""Module for functions related to displaying or outputting images"""

__all__ = ['min_xy', 'max_xy', 'minmax_x', 'minmax_y', 'print_image', 'make_image', 'ocr_image']

from io import BytesIO
from subprocess import Popen, PIPE

from PIL import Image
from PIL.ImageDraw import Draw

import mrm.cpoint as cpt

def min_xy(pos):
    """Return the minimum values for x and y in a group of point tuples or cpoints"""
    min_x = min(p.real if isinstance(p, complex) else p[0] for p in pos)
    min_y = min(p.imag if isinstance(p, complex) else p[1] for p in pos)

    return min_x, min_y

def max_xy(pos):
    """Return the maximum values for x and y in a group of point tuples or cpoints"""
    max_x = max(p.real if isinstance(p, complex) else p[0] for p in pos)
    max_y = max(p.imag if isinstance(p, complex) else p[1] for p in pos)

    return max_x, max_y

def minmax_x(pos):
    """Return the min and max values for x in a group of point tuples or cpoints"""
    min_x = min(p.real if isinstance(p, complex) else p[0] for p in pos)
    max_x = max(p.real if isinstance(p, complex) else p[0] for p in pos)

    return min_x, max_x

def minmax_y(pos):
    """Return the min and max values for y in a group of point tuples or cpoints"""
    min_y = min(p.imag if isinstance(p, complex) else p[1] for p in pos)
    max_y = max(p.imag if isinstance(p, complex) else p[1] for p in pos)

    return min_y, max_y

def print_image(pos, use_char = False, default_char = ' ', highlighter = lambda x, y, c: c, margin = 1, border = False, ruler = False):
    """Output a text-based representation of the points or cpoints specified in pos.
    Without use_char, present points will be represented with '**' and missing points with '  '.
    With use_char, present points will output their dict value and missing points use default_char.
    highlighter is a function which is given the location and character about to be output
    and which returns the actual string to display at that location, allowing items to be highlighted
    or key points added to the grid.
    """
    min_x, min_y = min_xy(pos)
    max_x, max_y = max_xy(pos)

    from_xy = None
    example = next(iter(pos))
    if isinstance(example, tuple):
        from_xy = lambda x, y: (x, y)
    if isinstance(example, list):
        from_xy = lambda x, y: [x, y]
    if isinstance(example, complex):
        from_xy = cpt.from_xy
    if from_xy is None:
        raise TypeError('Unknown point set type')

    if ruler:
        r_strs = [str(x) for x in range(min_x - margin, max_x + 1 + margin)]
        rows = max(len(r) for r in r_strs)
        r_strs = [f'{r: >{rows}}' for r in r_strs]
        for n in range(rows):
            print(' ' * border + ''.join(r[n] for r in r_strs))
    if border:
        print('┌' + '─' * (max_x - min_x + 1 + 2 * margin ) + '┐')
    for y in range(int(min_y - margin), int(max_y + 1 + margin)):
        if border:
            print('│', end='')
        for x in range(int(min_x - margin), int(max_x + 1 + margin)):
            if from_xy(x, y) in pos:
                if use_char:
                    disp = pos[from_xy(x, y)]
                else:
                    disp = '**'
            else:
                if use_char:
                    disp = default_char
                else:
                    disp = '  '
            print(highlighter(x, y, disp), end='')
        if border:
            print('│', end='')
        if ruler:
            print('', y, end='')
        print()
    if border:
        print('└' + '─' * (max_x - min_x + 1 + 2 * margin ) + '┘')

def make_image(pos, output):
    """Draws a PIL Image which represents the points/cpoints given in pos.
    Present points are filled black, missing points are left white.
    If output is True, also show a text representation.
    """
    min_x, min_y = min_xy(pos)
    max_x, max_y = max_xy(pos)

    width = int(max_x - min_x)
    height = int(max_y - min_y)

    from_xy = None
    example = next(iter(pos))
    if isinstance(example, tuple):
        from_xy = lambda x, y: (x, y)
    if isinstance(example, list):
        from_xy = lambda x, y: [x, y]
    if isinstance(example, complex):
        from_xy = cpt.from_xy
    if from_xy is None:
        raise TypeError('Unknown point set type')

    img = Image.new('1', (2 * width + 2, height + 2), color = 1)
    draw = Draw(img)

    for y in range(int(min_y), int(max_y + 1)):
        for x in range(int(min_x), int(max_x + 1)):
            if from_xy(x, y) in pos:
                draw.point(((x - int(min_x)) * 2 + 1, y - int(min_y) + 1), fill = 0)
                draw.point(((x - int(min_x)) * 2 + 2, y - int(min_y) + 1), fill = 0)
                if output:
                    print('**', end = '')
            elif output:
                print('  ', end='')
        if output:
            print()

    return img

def ocr_image(img, filename=None):
    """Takes a drawn PIL Image and pipes it to gocr to recognize text/digits
    Custom characters can be stored in .gocr for strange symbols or misreads
    If filename is specified, save to that filename for use with gocr externally
    """
    raw_io = BytesIO()
    img.save(raw_io, 'ppm')
    if filename:
        img.save(filename)
    raw_io.seek(0)

    with Popen(["gocr", "-p", "./mrm/.gocr/", "-m2", "-"], stdin=PIPE, stdout=PIPE) as gocr_proc:
        gocr_proc.stdin.write(raw_io.read())
        gocr_proc.stdin.close()
        gocr_proc.wait()
        txt = gocr_proc.stdout.read().decode('utf-8').strip('\n')
        gocr_proc.stdout.close()

    return txt
