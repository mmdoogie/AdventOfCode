from mrm.image import make_image, ocr_image

def parse():
    with open('data/aoc_2022/10.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return lines

def process(lines):
    regX = 1
    valHist = []

    for l in lines:
        p = l.split(" ")
        if p[0] == "noop":
            valHist += [regX]
        if p[0] == "addx":
            valHist += [regX]
            valHist += [regX]
            regX += int(p[1])

    return valHist

def part1(output=False):
    lines = parse()
    valHist = process(lines)

    return sum([n * valHist[n-1] for n in range(20, len(valHist), 40)])

def part2(output=False):
    lines = parse()
    valHist = process(lines)

    present = {}
    for y in range(6):
        line = ""
        for x in range(40):
            sc = valHist[40*y + x]
            if abs(x - sc) <= 1:
                present[(x, y)] = True

    img = make_image(present, output)
    return ocr_image(img)
