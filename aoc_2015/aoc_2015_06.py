from collections import defaultdict

with open('data/aoc_2015/06.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def part1(output = True):
    on_lights = set()
    for d in dat:
        w = d.split(' ')
        if w[0] == 'turn':
            from_pt = [int(x) for x in w[2].split(',')]
            to_pt = [int(x) for x in w[4].split(',')]
            for y in range(from_pt[1], to_pt[1] + 1):
                for x in range(from_pt[0], to_pt[0] + 1):
                    at_pt = (x, y)
                    if w[1] == 'on':
                        on_lights.add(at_pt)
                    else:
                        on_lights.discard(at_pt)
        else:
            from_pt = [int(x) for x in w[1].split(',')]
            to_pt = [int(x) for x in w[3].split(',')]
            for y in range(from_pt[1], to_pt[1] + 1):
                for x in range(from_pt[0], to_pt[0] + 1):
                    at_pt = (x, y)
                    if at_pt in on_lights:
                        on_lights.remove(at_pt)
                    else:
                        on_lights.add(at_pt)

        if output:
            print(f'{d:50} now lit: {len(on_lights)}')

    return len(on_lights)

def part2(output = True):
    on_lights = defaultdict(int)
    for d in dat:
        w = d.split(' ')
        if w[0] == 'turn':
            from_pt = [int(x) for x in w[2].split(',')]
            to_pt = [int(x) for x in w[4].split(',')]
            for y in range(from_pt[1], to_pt[1] + 1):
                for x in range(from_pt[0], to_pt[0] + 1):
                    at_pt = (x, y)
                    if w[1] == 'on':
                        on_lights[at_pt] += 1
                    else:
                        on_lights[at_pt] = max(0, on_lights[at_pt] - 1)
        else:
            from_pt = [int(x) for x in w[1].split(',')]
            to_pt = [int(x) for x in w[3].split(',')]
            for y in range(from_pt[1], to_pt[1] + 1):
                for x in range(from_pt[0], to_pt[0] + 1):
                    at_pt = (x, y)
                    on_lights[at_pt] += 2

    return sum(on_lights.values())

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
