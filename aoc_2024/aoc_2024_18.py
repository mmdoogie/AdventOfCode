from functools import partial

from mrm.ansi_term import red, green, blue, cyan
from mrm.dijkstra import Dictlike, dijkstra
from mrm.image import print_image
from mrm.parse import all_nums
from mrm.point import adj_ortho
from mrm.search import fn_binary_search

def parse():
    with open('data/aoc_2024/18.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    grid = {(x, y) for y in range(70 + 1) for x in range(70 + 1)}
    corrupted = [tuple(all_nums(l)) for l in lines]

    return grid, corrupted

START = (0, 0)
END = (70, 70)

def find_path(grid, corrupted, corr_cnt, output=False, extra_corr=None):
    sub_corr = set(corrupted[:corr_cnt])

    @Dictlike
    def ngh(loc):
        return [a for a in adj_ortho(loc, grid) if a not in sub_corr]

    if output:
        w, p = dijkstra(ngh, start_point=START, end_point=END)
        def highlighter(x, y, _):
            loc = (x, y)
            if loc in {START, END}:
                return blue('@')
            if loc == extra_corr:
                return cyan('⚠')
            if loc in p[END]:
                return green('O')
            if loc in sub_corr:
                return red('-')
            return '.'
        print_image(grid, highlighter=highlighter, margin=0, border=True, ruler=True)
    else:
        w = dijkstra(ngh, start_point=START, end_point=END, keep_paths=False)

    if END in w:
        return w[END]
    return corrupted[corr_cnt - 1]

def part1(output=False):
    grid, corrupted = parse()
    return find_path(grid, corrupted, 1024, output=output)

def part2(output=False):
    grid, corrupted = parse()
    search_fn = partial(find_path, grid, corrupted)
    l_inp, _, _, r_val = fn_binary_search(search_fn, 1025, lambda x: isinstance(x, tuple), len(corrupted), output=output)
    if output:
        find_path(grid, corrupted, l_inp, output=True, extra_corr=corrupted[l_inp])
    return ','.join(str(n) for n in r_val)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
