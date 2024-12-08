from mrm.image import make_image, ocr_image

with open('data/aoc_2021/13.txt') as f:
    dat = [x.strip() for x in f.readlines()]

pointStrs = [x for x in dat if len(x) > 0 and x[0] != 'f']
foldStrs = [x for x in dat if len(x) > 0 and x[0] == 'f']
folds = [x.split(' ')[2].split('=') for x in foldStrs]

def fold(points, axis, loc):
    for p in points:
        if axis == 'x':
            if p[0] < loc:
                continue
            else:
                p[0] = loc - (p[0] - loc)
        else:
            if p[1] < loc:
                continue
            else:
                p[1] = loc - (p[1] - loc)


def part1(output=False):
    points = [[int(y) for y in x.split(',')] for x in pointStrs]

    fold(points, folds[0][0], int(folds[0][1]))
    uniqPoints = set([','.join([str(a) for a in p]) for p in points])
    return len(uniqPoints)

def part2(output=False):
    points = [[int(y) for y in x.split(',')] for x in pointStrs]

    for f in folds:
        fold(points, f[0], int(f[1]))

    img = make_image(points, output)
    return ocr_image(img)
