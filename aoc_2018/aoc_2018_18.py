from collections import defaultdict

with open('data/aoc_2018/18.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def parse_grid():
    coll_area = defaultdict(lambda: 0)

    for y, d in enumerate(dat):
        for x, c in enumerate(d):
            match c:
                case '|':
                    coll_area[(x, y)] = 1
                case '#':
                    coll_area[(x, y)] = 10000

    return coll_area, x + 1, y + 1

def count_adj(coll_area, loc):
    x, y = loc
    adj_locs = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
                (x,     y - 1),             (x,     y + 1),
                (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]

    return sum(coll_area[a] for a in adj_locs)

def grid_string(coll_area, width, height):
    grid_chars = {0: '.', 1: '|', 10000: '#'}
    grid = ''
    for y in range(height):
        for x in range(width):
            grid += grid_chars[coll_area[(x, y)]]
        grid += '\n'
    grid += '\n'
    return grid

def perform_iteration(coll_area, width, height):
    new_area = defaultdict(lambda: 0)

    for y in range(height):
        for x in range(width):
            curr_type = coll_area[(x, y)]
            adj_sum = count_adj(coll_area, (x, y))
            adj_trees = adj_sum % 10000
            adj_lumberyards = adj_sum // 10000

            match curr_type:
                case 0:
                    if adj_trees >= 3:
                        new_area[(x, y)] = 1
                case 1:
                    new_area[(x, y)] = 10000 if adj_lumberyards >= 3 else 1
                case 10000:
                    if adj_lumberyards >= 1 and adj_trees >= 1:
                        new_area[(x, y)] = 10000

    return new_area

def part1(output = True):
    coll_area, width, height = parse_grid()
    assert width * height < 10000

    if output:
        print('Initial State')
        print(grid_string(coll_area, width, height))

    for it in range(10):
        coll_area = perform_iteration(coll_area, width, height)
        if output:
            print(f'Iteration {it + 1}')
            print(grid_string(coll_area, width, height))

    grid_sum = sum(coll_area.values())
    wood_acres = grid_sum % 10000
    lumberyard_acres = grid_sum // 10000
    if output:
        print(f'Wood: {wood_acres}, Lumberyards: {lumberyard_acres}')

    return wood_acres * lumberyard_acres

def compute_score(grid_scores, pattern_offset, pattern_len, total_minutes):
    minutes_remain = total_minutes - 1 - pattern_offset
    score_index = (minutes_remain % pattern_len) + pattern_offset
    return grid_scores[score_index]

def part2(output = True):
    coll_area, width, height = parse_grid()

    grid_scores = []

    for _ in range(1000):
        coll_area = perform_iteration(coll_area, width, height)

        grid_sum = sum(coll_area.values())
        wood_acres = grid_sum % 10000
        lumberyard_acres = grid_sum // 10000
        grid_score = wood_acres * lumberyard_acres
        grid_scores += [grid_score]

    pattern_len = list(reversed(grid_scores[:-1])).index(grid_score) + 1
    assert grid_scores[-1] == grid_scores[-1 - pattern_len] == grid_scores[-1 - 2 * pattern_len]

    for i in range(1000):
        if grid_scores[i] == grid_scores[i + pattern_len]:
            pattern_1 = grid_scores[i:i + pattern_len]
            pattern_2 = grid_scores[i + pattern_len:i + 2 * pattern_len]
            if pattern_1 != pattern_2:
                continue
            if output:
                print('Pattern offset:', i)
            break
    pattern_offset = i

    if output:
        print('Pattern len:', pattern_len)
        score_checks = [grid_scores[-1 - i * pattern_len] for i in range(4)]
        print('Verify:', score_checks)

    assert compute_score(grid_scores, pattern_offset, pattern_len, 806) == grid_scores[806 - 1]

    return compute_score(grid_scores, pattern_offset, pattern_len, 1000000000)

if __name__ == "__main__":
    print('Part 1:', part1())
    print('Part 2:', part2())
