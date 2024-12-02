from collections import namedtuple
from aoc_2019.intcode import IntcodeComputer, PartialResult
from mrm.image import make_image, ocr_image

def parse():
    with open('data/aoc_2019/11.txt') as f:
        dat = [x.strip() for x in f.readlines()]

    base_program = [int(x) for x in dat[0].split(',')]
    return base_program

Point = namedtuple('Point', ['x', 'y'])

def do_paint(base_program, initial_val = 0):
    ic = IntcodeComputer(base_program)

    panels = {}
    curr_point = Point(0, 0)
    face_dirs = [Point(0, -1), Point(1,0), Point(0, 1), Point(-1, 0)]
    face_idx = 0

    ic.input(initial_val)
    res = ic.run_partial()
    while res != PartialResult.TERMINATED:
        panel_color = ic.output()
        face_rot = ic.output()

        panels[curr_point] = panel_color
        face_idx = (face_idx + (2 * face_rot - 1)) % 4
        curr_point = Point(curr_point.x + face_dirs[face_idx].x, curr_point.y + face_dirs[face_idx].y)

        if curr_point in panels:
            ic.input(panels[curr_point])
        else:
            ic.input(0)

        res = ic.run_partial()

    return panels

def part1(output=False):
    base_program = parse()
    return len(do_paint(base_program))

def part2(output=False):
    base_program = parse()
    panels = do_paint(base_program, initial_val = 1)
    max_x = max([l.x for l in panels])
    max_y = max([l.y for l in panels])

    present = {(x, y): True for y in range(max_y + 1) for x in range(max_x + 1) if panels.get(Point(x,y), 0) == 1}
    img = make_image(present, output)
    return ocr_image(img)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
