from collections import defaultdict
from functools import reduce
from operator import mul
from time import sleep

import mrm.ansi_term as ansi

with open('data/aoc_2023/02.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

COLOR_CODES = {"red": ansi.COLOR_RED, "green": ansi.COLOR_GREEN, "blue": ansi.COLOR_BLUE}

def part1(output = True):
    max_cubes = {"red": 12, "green": 13, "blue": 14}
    gameid_sum = 0

    if output:
        ansi.clear_screen()

    for d in dat:
        game_id, game_list = d.split(': ')
        game_id_num = int(game_id.split(' ')[1])

        if output:
            print(d)
            sleep(0.1 if game_id_num <= 5 else 0)

        pull_list = game_list.split('; ')
        ok = True
        for cube_info in pull_list:
            cube_counts = cube_info.split(', ')
            pull_cubes = defaultdict(lambda: 0)
            for cube_count in cube_counts:
                num_cubes, cube_color = cube_count.split(' ')
                pull_cubes[cube_color] = int(num_cubes)
                if max_cubes[cube_color] < int(num_cubes):
                    ok = False
            if output:
                for color, code in COLOR_CODES.items():
                    if pull_cubes[color] > max_cubes[color]:
                        main_cubes = '*' * max_cubes[color]
                        extra_cubes = '*' * (pull_cubes[color] - max_cubes[color])
                        print(code + f'{main_cubes + ansi.TEXT_UNDERLINE + extra_cubes + ansi.TEXT_RESET:<33s}', end = '')
                    else:
                        print(code + f'{"*" * pull_cubes[color]:<25s}' + ansi.TEXT_RESET, end = '')
                print()
                sleep(0.1 if game_id_num <= 5 else 0)

        if ok:
            gameid_sum += game_id_num

        if output:
            if ok:
                print('✅')
            else:
                print('❌')
            print()
            sleep(0.5 if game_id_num <= 5 else 0.05)

    return gameid_sum

def part2(output = True):
    power_sum = 0

    for d in dat:
        required_cubes = defaultdict(lambda: 0)
        game_id, game_list = d.split(': ')
        game_id_num = int(game_id.split(' ')[1])

        if output:
            print(d)
            sleep(0.75 if game_id_num <= 5 else 0)

        pull_list = game_list.split('; ')
        for cube_info in pull_list:
            cube_counts = cube_info.split(', ')
            for cube_count in cube_counts:
                num_cubes, cube_color = cube_count.split(' ')
                if required_cubes[cube_color] < int(num_cubes):
                    required_cubes[cube_color] = int(num_cubes)

        set_power = reduce(mul, required_cubes.values())
        power_sum += set_power

        if output:
            print('Game requires: ', end = '')
            for color, code in COLOR_CODES.items():
                print(code + f'{"*" * required_cubes[color]:<25s}' + ansi.TEXT_RESET, end = '')
            print(f' Set Power: {set_power:<5d} --> Total Sum: {power_sum:<5d}')
            print()

    return power_sum

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
