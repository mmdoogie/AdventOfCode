"""Module for functions related to displaying or outputting images"""

__all__ = ['min_xy', 'max_xy', 'minmax_x', 'minmax_y', 'print_image', 'make_image', 'ocr_image']

from io import BytesIO
from subprocess import Popen, PIPE

from PIL import Image
from PIL.ImageDraw import Draw

def min_xy(pos):
    """Return the minimum values for x and y in a group of point tuples"""
    min_x = min(p[0] for p in pos)
    min_y = min(p[1] for p in pos)

    return min_x, min_y

def max_xy(pos):
    """Return the maximum values for x and y in a group of point tuples"""
    max_x = max(p[0] for p in pos)
    max_y = max(p[1] for p in pos)

    return max_x, max_y

def minmax_x(pos):
    """Return the min and max values for x in a group of point tuples"""
    min_x = min(p[0] for p in pos)
    max_x = max(p[0] for p in pos)

    return min_x, max_x

def minmax_y(pos):
    """Return the min and max values for y in a group of point tuples"""
    min_y = min(p[1] for p in pos)
    max_y = max(p[1] for p in pos)

    return min_y, max_y

def print_image(pos, use_char = False, default_char = ' ', highlighter = lambda x, y, c: c, margin = 1):
    """Output a text-based representation of the points specified in pos.
    Without use_char, present points will be represented with '**' and missing points with '  '.
    With use_char, present points will output their dict value and missing points use default_char.
    highlighter is a function which is given the location and character about to be output
    and which returns the actual string to display at that location, allowing items to be highlighted
    or key points added to the grid.
    """
    min_x, min_y = min_xy(pos)
    max_x, max_y = max_xy(pos)

    for y in range(min_y - margin, max_y + 1 + margin):
        for x in range(min_x - margin, max_x + 1 + margin):
            if (x, y) in pos:
                if use_char:
                    disp = pos[(x, y)]
                else:
                    disp = '**'
            else:
                if use_char:
                    disp = default_char
                else:
                    disp = '  '
            print(highlighter(x, y, disp), end='')
        print()

def make_image(pos, output):
    """Draws a PIL Image which represents the points given in pos.
    Present points are filled black, missing points are left white.
    If output is True, also show a text representation.
    """
    min_x, min_y = min_xy(pos)
    max_x, max_y = max_xy(pos)

    width = max_x - min_x
    height = max_y - min_y

    img = Image.new('1', (2 * width + 2, height + 2), color = 1)
    draw = Draw(img)

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) in pos:
                draw.point(((x - min_x) * 2 + 1, y - min_y + 1), fill = 0)
                draw.point(((x - min_x) * 2 + 2, y - min_y + 1), fill = 0)
                if output:
                    print('**', end = '')
            elif output:
                print('  ', end='')
        if output:
            print()

    return img

def ocr_image(img):
    """Takes a drawn PIL Image and pipes it to gocr to recognize text/digits
    Custom characters can be stored in .gocr for strange symbols or misreads
    """
    raw_io = BytesIO()
    img.save(raw_io, 'ppm')
    raw_io.seek(0)

    with Popen(["gocr", "-p", "./mrm/.gocr/", "-m2", "-"], stdin=PIPE, stdout=PIPE) as gocr_proc:
        gocr_proc.stdin.write(raw_io.read())
        gocr_proc.stdin.close()
        gocr_proc.wait()
        txt = gocr_proc.stdout.read().decode('utf-8').strip('\n')
        gocr_proc.stdout.close()

    return txt
