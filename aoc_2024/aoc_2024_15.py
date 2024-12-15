import mrm.ansi_term as ansi
import mrm.cpoint as cpt
import mrm.image as img

def parse(expand_grid=False):
    with open('data/aoc_2024/15.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]

    split = lines.index('')
    grid = cpt.grid_as_dict(lines[:split])
    moves = ''.join(lines[split + 1:])

    if expand_grid:
        expand = {'#': '##', 'O': '[]', '.': '..', '@': '@.'}
        p2_grid = {k + k.real + offset: expand[v][offset] for k, v in grid.items() for offset in [0, cpt.RIGHT]}
        return p2_grid, moves

    return grid, moves

def gps(grid):
    tot = 0
    for g in grid:
        if grid[g] not in 'O[':
            continue
        x, y = cpt.as_xy(g, int)
        tot += 100 * y + x
    return tot

def viz(grid, pt, move):
    viz_grid = {cpt.as_xy(k, int): v for k, v in grid.items()}
    viz_grid[cpt.as_xy(pt, int)] = '@'
    print(f'@ {cpt.as_xy(pt, int)} move {move}' + ' '*20)
    color_map = {'[': ansi.yellow, ']': ansi.yellow, 'O': ansi.yellow, '#': ansi.cyan, '@': ansi.red}
    img.print_image(viz_grid, use_char=True, border=True, highlighter=lambda x, y, c: color_map[c](c) if c in color_map else c)

MOVE_MAP = {'^': cpt.UP, '<': cpt.LEFT, '>': cpt.RIGHT, 'v': cpt.DOWN}

def part1(output=False):
    grid, moves = parse(expand_grid=False)
    start = [g for g in grid if grid[g] == '@'][0]
    grid[start] = '.'

    if output:
        ansi.clear_screen()

    pt = start
    for m in moves:
        dist = MOVE_MAP[m]
        if grid[pt + dist] == '.':
            pt += dist
        elif grid[pt + dist] == '#':
            pass
        else:
            i = 2
            while True:
                if grid[pt + i * dist] == 'O':
                    i += 1
                    continue
                if grid[pt + i * dist] == '#':
                    break
                grid[pt + i * dist] = 'O'
                grid[pt + dist] = '.'
                pt += dist
                break
        if output:
            with ansi.hidden_cursor():
                ansi.cursor_home()
                viz(grid, pt, m)

    return gps(grid)

def part2(output=False):
    grid, moves = parse(expand_grid=True)
    start = [g for g in grid if grid[g] == '@'][0]
    grid[start] = '.'

    other_side = {'[': cpt.RIGHT, ']': cpt.LEFT}

    if output:
        ansi.clear_screen()

    pt = start
    for m in moves:
        dist = MOVE_MAP[m]
        if grid[pt + dist] == '.':
            pt += dist
        elif grid[pt + dist] == '#':
            pass
        elif dist in [cpt.LEFT, cpt.RIGHT]:
            i = 2
            while True:
                if grid[pt + i * dist] in '[]':
                    i += 1
                    continue
                if grid[pt + i * dist] == '#':
                    break
                for n in reversed(range(1, i)):
                    grid[pt + (n + 1) * dist] = grid[pt + n * dist]
                grid[pt + dist] = '.'
                pt += dist
                break
        else:
            box_set = set()
            checked = set()

            box_set.add(pt + dist)
            box_set.add(pt + dist + other_side[grid[pt + dist]])

            jammed = False
            while True:
                to_add = set()
                for b in box_set:
                    if b in checked:
                        continue
                    checked.add(b)
                    if grid[b + dist] in '[]':
                        to_add.add(b + dist)
                        to_add.add(b + dist + other_side[grid[b + dist]])
                    if grid[b + dist] == '#':
                        jammed = True
                        break
                if jammed:
                    break
                box_set.update(to_add)
                if len(to_add) == 0:
                    to_move = sorted(box_set, key=lambda x:(x.imag, x.real), reverse=dist==cpt.DOWN)
                    for b in to_move:
                        grid[b + dist] = grid[b]
                        grid[b] = '.'
                    pt += dist
                    break

        if output:
            with ansi.hidden_cursor():
                ansi.cursor_home()
                viz(grid, pt, m)

    return gps(grid)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
