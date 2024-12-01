import mrm.ansi_term as ansi
from mrm.point import adj_ortho
from mrm.dijkstra import dijkstra, Dictlike

with open('data/aoc_2016/13.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]
    office_num = int(dat[0])

def is_open(pt):
    x, y = pt
    if x < 0 or y < 0 or x > 50 or y > 50:
        return False
    fv = x*x + 3*x + 2*x*y + y + y*y + office_num
    return fv.bit_count() % 2 == 0

open_dl = Dictlike(lambda x: 0, is_open)

def neigh(pt):
    return adj_ortho(pt, open_dl)

neigh_dl = Dictlike(neigh)

def viz1(path):
    ansi.clear_screen()
    for y in range(51):
        for x in range(51):
            pt = (x, y)
            if pt == (1, 1):
                print(ansi.green('ss'), end='')
            elif pt == (31, 39):
                print(ansi.green('ee'), end='')
            elif pt in path:
                print(ansi.magenta('++'), end='')
            else:
                if pt in open_dl:
                    print('  ', end='')
                else:
                    print('##', end='')
        print()

def part1(output = True):
    ini = (1, 1)
    fin = (31, 39)
    w, p = dijkstra(neigh_dl, start_point=ini, end_point=fin)

    if output:
        viz1(p[fin])

    return w[fin]

def viz2(wts):
    ansi.clear_screen()
    for y in range(51):
        for x in range(51):
            pt = (x, y)
            if pt in open_dl:
                if pt in wts and wts[pt] < 100:
                    if wts[pt] > 50:
                        print(ansi.red(f'{wts[pt]:02}'), end='')
                    else:
                        print(ansi.green(f'{wts[pt]:02}'), end='')
                else:
                    print('  ', end='')
            else:
                print('##', end='')
        print()

def part2(output = True):
    ini = (1, 1)
    w = dijkstra(neigh_dl, start_point=ini, keep_paths=False)

    if output:
        viz2(w)

    return sum(wt <= 50 for wt in w.values())

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
