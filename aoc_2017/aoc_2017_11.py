with open('data/aoc_2017/11.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]
    path = dat[0].split(',')

def dist(x, y):
    x = abs(x)
    y = abs(y)

    # if y is bigger, most efficient is to go down, then diagonal
    if y > x:
        diag = x * 2
        down = y - x
        return int(down + diag)

    # if x is bigger, move over then diagonal, but over is way more expensive
    diag = y * 2
    over = x - y
    return int(diag + 2 * over)

def traverse():
    x, y = 0, 0
    max_dist = 0

    for d in path:
        if d == 'n':
            y += 1
        elif d == 'ne':
            x += 0.5
            y += 0.5
        elif d == 'se':
            x += 0.5
            y -= 0.5
        elif d == 's':
            y -= 1
        elif d == 'sw':
            x -= 0.5
            y -= 0.5
        elif d == 'nw':
            x -= 0.5
            y += 0.5
        else:
            print('Unexpected direction encountered!')

        max_dist = max(max_dist, dist(x, y))

    return dist(x, y), max_dist

def part1(output = True):
    del output

    end_dist, _ = traverse()
    return end_dist

def part2(output = True):
    del output

    _, max_dist = traverse()
    return max_dist

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
