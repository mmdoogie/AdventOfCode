from collections import namedtuple
from enum import Enum
from os import system

from aoc_2019.intcode import IntcodeComputer, PartialResult
import mrm.ansi_term as ansi

Pt = namedtuple('Pt', ['x', 'y'])

class Tile(Enum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4

def parse():
    with open('data/aoc_2019/13.txt') as f:
        dat = [x.strip() for x in f.readlines()]

    base_program = [int(x) for x in dat[0].split(',')]
    return base_program

def update_tiles(tiles, outputs):
    new_tiles = {(outputs[3 * i], outputs[3 * i + 1]): outputs[3 * i + 2] for i in range(len(outputs) // 3)}
    score = (-1, 0)
    if score in new_tiles:
        tiles.update({score: new_tiles[score]})
        del new_tiles[score]
    tiles.update({k: Tile(v) for k, v in new_tiles.items()})

def show_screen(tiles):
    min_x = min(tiles.keys(), key=lambda a: a[0])[0]
    min_y = min(tiles.keys(), key=lambda a: a[1])[1]
    max_x = max(tiles.keys(), key=lambda a: a[0])[0]
    max_y = max(tiles.keys(), key=lambda a: a[1])[1]

    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            if x == -1:
                if y == 0:
                    print('Score:', tiles[(x, y)])
                continue
            elif (x,y) in tiles:
                tid = Tile(tiles[(x,y)])
            else:
                tid = Tile.EMPTY

            match tid:
                case Tile.EMPTY:
                    print(' ', end='')
                case Tile.WALL:
                    print('#', end='')
                case Tile.BLOCK:
                    print('~', end='')
                case Tile.PADDLE:
                    print('_', end='')
                case Tile.BALL:
                    print('o', end='')
        print()
    print()

def count_blocks(tiles):
    return sum([t == Tile.BLOCK for t in tiles.values()])

def ball_pos(tiles):
    return Pt(*[k for k, v in tiles.items() if v == Tile.BALL][0])

def paddle_pos(tiles):
    return Pt(*[k for k, v in tiles.items() if v == Tile.PADDLE][0])

def get_score(tiles):
    return tiles[(-1, 0)]

def part1(output=False):
    base_program = parse()
    ic = IntcodeComputer(base_program)
    res = ic.run_partial()
    assert res == PartialResult.TERMINATED
    out = ic.all_outputs()

    tiles = {}
    update_tiles(tiles, out)
    if output:
        show_screen(tiles)

    return count_blocks(tiles)

def part2(output=False):
    base_program = parse()
    p = [2] + base_program[1:]
    ic = IntcodeComputer(p)

    tiles = {}
    ball_dir = None
    last_ball = None

    if output:
        ansi.clear_screen()

    while True:
        res = ic.run_partial()
        out = ic.all_outputs()
        update_tiles(tiles, out)
        if output:
            with ansi.hidden_cursor():
                ansi.cursor_home()
                show_screen(tiles)

        ball = ball_pos(tiles)
        if ball_dir is None:
            last_ball = ball
        ball_dir = Pt(ball.x - last_ball.x, ball.y - last_ball.y)
        last_ball = ball
        paddle = paddle_pos(tiles)

        if ball_dir.y == 1:
            steps = paddle.y - 1 - ball.y
            dist = paddle.x - (ball.x + steps * ball_dir.x)

            if dist < 0:
                paddle_input = 1
            elif dist > 0:
                paddle_input = -1
            else:
                paddle_input = 0
        else:
            if paddle.x < ball.x:
                paddle_input = 1
            else:
                paddle_input = -1

        if count_blocks(tiles) == 0 or res == PartialResult.TERMINATED:
            break

        ic.input(paddle_input)

    return get_score(tiles)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
