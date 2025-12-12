from mrm.parse import all_nums
import mrm.point as pt

def parse():
    with open('data/aoc_2025/12.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    presents = [pt.grid_as_dict(lines[5*i+1:5*i+5], lambda x: x=='#') for i in range(6)]
    puzzles  = [list(all_nums(l)) for l in lines if 'x' in l]
    return presents, puzzles

def part1(output=False):
    presents, puzzles = parse()

    impossible_cnt = 0
    possible_cnt = 0
    present_size = [len(p) for p in presents]
    for p in puzzles:
        area = p[0] * p[1]
        min_present_area = sum(sz * cnt for sz, cnt in zip(present_size, p[2:]))
        if min_present_area > area:
            impossible_cnt += 1
            continue
        bounding_box_area = (p[0] // 3) * (p[1] // 3)
        if sum(p[2:]) <= bounding_box_area:
            possible_cnt += 1
    if output:
        print('Impossible:', impossible_cnt)
        print('  Possible:', possible_cnt)
    assert possible_cnt == len(puzzles) - impossible_cnt

    return possible_cnt

def part2(output=False):
    return 'Decorate!'

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
