from io import BytesIO
from subprocess import Popen, PIPE

from PIL import Image
from PIL.ImageDraw import Draw

with open('data/aoc_2018/10.txt', encoding='utf-8') as f:
    dat = [x.strip() for x in f.readlines()]

def min_pos(pos):
    min_x = min(p[0] for p in pos)
    min_y = min(p[1] for p in pos)

    return (min_x, min_y)

def max_pos(pos):
    max_x = max(p[0] for p in pos)
    max_y = max(p[1] for p in pos)

    return (max_x, max_y)

def area_pos(pos):
    min_x, min_y = min_pos(pos)
    max_x, max_y = max_pos(pos)

    return (max_x - min_x) * (max_y - min_y)

def find_msg(output = True):
    pos = [[int(x) for x in d.split('> ')[0].split('<')[1].split(',')] for d in dat]
    vel = [[int(x) for x in d.split('y=<')[1].split('>')[0].split(',')] for d in dat]

    min_area = area_pos(pos)
    min_it = 0

    it = 0
    while True:
        it += 1
        for p, v in zip(pos, vel):
            p[0] += v[0]
            p[1] += v[1]
        a = area_pos(pos)
        if a < min_area:
            if output and (it % 1000 == 0 or a < 100000):
                print('Step:', it, 'Area:', a)
            min_area = a
            min_it = it
        if it - min_it >= 1:
            break

    for p, v in zip(pos, vel):
        p[0] -= v[0]
        p[1] -= v[1]
    assert area_pos(pos) == min_area

    return pos, it - 1

def make_image(pos, output):
    min_x, min_y = min_pos(pos)
    max_x, max_y = max_pos(pos)

    width = max_x - min_x
    height = max_y - min_y

    im = Image.new('1', (2 * width + 2, height + 2), color = 1)
    draw = Draw(im)

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if [x, y] in pos:
                draw.point(((x - min_x) * 2 + 1, y - min_y + 1), fill = 0)
                draw.point(((x - min_x) * 2 + 2, y - min_y + 1), fill = 0)
                if output:
                    print('**', end = '')
            elif output:
                print('  ', end='')
        if output:
            print()

    return im

def ocr_image(img):
    raw_io = BytesIO()
    img.save(raw_io, 'ppm')
    raw_io.seek(0)

    with Popen(["gocr", "-"], stdin=PIPE, stdout=PIPE) as gocr_proc:
        gocr_proc.stdin.write(raw_io.read())
        gocr_proc.stdin.close()
        gocr_proc.wait()
        txt = gocr_proc.stdout.read().decode('utf-8').strip('\n')
        gocr_proc.stdout.close()

    return txt

msg_time = 0

def part1(output = True):
    global msg_time
    pos, msg_time = find_msg(output)

    img = make_image(pos, output)
    txt = ocr_image(img)

    return txt

def part2(output = True):
    if msg_time == 0:
        part1(False)
    return msg_time
