import mrm.image as im

with open('data/aoc_2016/08.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def compute(output):
    screen = set()

    for d in dat:
        if 'rect' in d:
            a, b = [int(x) for x in d.split(' ')[1].split('x')]
            for y in range(b):
                for x in range(a):
                    screen.add((x, y))
        elif 'column' in d:
            a, b = [int(x) for x in d.split('=')[1].split(' by ')]
            old_col = {s for s in screen if s[0] == a}
            new_col = {(s[0], (s[1] + b) % 6) for s in old_col}
            screen = screen.difference(old_col).union(new_col)
        else:
            a, b = [int(x) for x in d.split('=')[1].split(' by ')]
            old_row = {s for s in screen if s[1] == a}
            new_row = {((s[0] + b) % 50, s[1]) for s in old_row}
            screen = screen.difference(old_row).union(new_row)

        if output:
            print(d)
            im.print_image(screen)
            print()

    return screen

def part1(output = True):
    return len(compute(output))

def part2(output = True):
    screen = compute(False)
    img = im.make_image(screen, output)
    return im.ocr_image(img)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
