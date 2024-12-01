from time import sleep

import mrm.ansi_term as ansi

with open('data/aoc_2017/19.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]
    width = len(dat[0])
    height = len(dat)

def print_area(x0, y0, gs, encounter, steps, force=False):
    if encounter != '' and steps % 10 != 0 and not force:
        return

    with ansi.hidden_cursor():
        ansi.cursor_home()
        for y in range(y0-gs, y0+gs):
            for x in range(x0-2*gs, x0+2*gs):
                if x < 0 or x >= width or y < 0 or y >= height:
                    print(' ', end='')
                else:
                    txt = dat[y][x]
                    if x == x0 and y == y0:
                        with ansi.text_attr(ansi.COLOR_RED):
                            print(txt, end='')
                    elif txt == '+':
                        with ansi.text_attr(ansi.COLOR_YELLOW):
                            print(txt, end='')
                    elif txt in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                        with ansi.text_attr(ansi.COLOR_MAGENTA):
                            print(txt, end='')
                    else:
                        print(txt, end='')
            print()
        print()
        print('Encountered:', encounter)
        print('Steps:      ', steps)
        #if encounter == '':
        sleep(0.02)

def traverse(output):
    x = dat[0].index('|')
    y = 0
    dx = 0
    dy = 1
    encounter = []
    steps = 0

    if output:
        ansi.clear_screen()
        ansi.save_cursor()
        print_area(x, y, 20, '', 0)

    while True:
        x += dx
        y += dy
        steps += 1
        nxt = dat[y][x]
        if nxt in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            encounter += nxt
        elif nxt == ' ':
            if output:
                with ansi.restored_cursor():
                    print_area(x, y, 20, ''.join(encounter), steps, True)
            return ''.join(encounter), steps
        elif nxt == '+':
            if dx:
                if dat[y-1][x] != ' ':
                    dx = 0
                    dy = -1
                elif dat[y+1][x] != ' ':
                    dx = 0
                    dy = 1
                else:
                    print('error at turn', x, y)
            elif dy:
                if dat[y][x-1] != ' ':
                    dx = -1
                    dy = 0
                elif dat[y][x+1] != ' ':
                    dx = 1
                    dy = 0
                else:
                    print('error at turn', x, y)
            else:
                print('wakko state')
        elif nxt in '|-':
            pass
        else:
            print('unexpected char', nxt, 'encountered!')
        if output:
            with ansi.restored_cursor():
                print_area(x, y, 20, ''.join(encounter), steps)

def part1(output = True):
    txt, _ = traverse(output)
    return txt

def part2(output = True):
    _, steps = traverse(output)
    return steps

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
