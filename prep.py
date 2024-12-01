#!/usr/bin/env python3
import argparse
from datetime import date, datetime
from os import path
import re
import sys

import aocd
from dotenv import load_dotenv

import mrm.ansi_term as ansi

def prep_template(fn, year, day):
    with open('_template.py', 'r', encoding='utf8') as in_file:
        in_data = in_file.read()
    in_data = re.sub('{YEAR}', str(year), in_data)
    in_data = re.sub('{DAY}', f'{day:02d}', in_data)
    with open(fn, 'w', encoding='utf8') as out_file:
        out_file.write(in_data)

def prep_data(fn, year, day):
    data = aocd.get_data(day=day, year=year)

    with open(fn, 'w', encoding='utf8') as out_file:
        out_file.write(data)

def update_results(year, day, force):
    puz = aocd.get_puzzle(day=day, year=year)
    result_module_name = f'data.aoc_{year}.results'
    result_module = __import__(result_module_name, fromlist = [None])
    answers = {}
    if puz.answered_a:
        answers[1] = puz.answer_a
    if puz.answered_b:
        answers[2] = puz.answer_b
    if day in result_module.results:
        current = result_module.results[day]
    else:
        current = {}
    if any(k in current and current[k] != v for k, v in answers.items()):
        print('Current answers:', current)
        print('Conflict with received answers', answers)
        if not force:
            print(ansi.yellow('Skipping!'))
            return
        print(ansi.red('Overwriting!'))
    if force or any(k not in current for k in answers):
        print(ansi.blue('Results updated: ' + str(answers)))
        result_module.results[day] = answers
        result_module.results.save()
    else:
        print('Results already up to date')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-y', type = int, help = 'Year to prep.')
    ap.add_argument('-d', type = int, help = 'Day to prep.')
    ap.add_argument('-p', type = int, choices = [0, 1, 2], help = 'Only preps specified part: 0 for template, 1 for data, 2 for results')
    ap.add_argument('-f', action = 'store_true', help = 'Force overwrite. Only valid with a specified part.')
    args = ap.parse_args()

    if not args.y:
        args.y = date.today().year

    if not args.d:
        args.d = datetime.utcnow().day

    if args.y >= 15 and args.y <= 24:
        args.y += 2000

    if args.y != 2024:
        print('Year must be 2024')
        sys.exit(1)

    if args.d < 1 or args.d > 25:
        print('Day must be between 1 and 25 inclusive.')
        sys.exit(1)

    if args.f and args.p is None:
        print('Part must be specified to force overwrite.')
        sys.exit(1)

    part_nums = set([args.p]) if args.p is not None else set([0, 1, 2])

    print(f'Prepping {args.y} Day {args.d}')

    if 0 in part_nums:
        template_file = f'aoc_{args.y}/aoc_{args.y}_{args.d:02d}.py'
        if path.isfile(template_file):
            print(f'{template_file} already exists, ', end='')
            if not args.f:
                print(ansi.yellow('skipping!'))
            else:
                print(ansi.red('overwriting!'))
                prep_template(template_file, args.y, args.d)
        else:
            print(ansi.green('Preparing template.'))
            prep_template(template_file, args.y, args.d)

    if 1 in part_nums or 2 in part_nums:
        load_dotenv()

    if 1 in part_nums:
        data_file = f'data/aoc_{args.y}/{args.d:02d}.txt'
        if path.isfile(data_file):
            print(f'{data_file} already exists, ', end='')
            if not args.f:
                print(ansi.yellow('skipping!'))
            else:
                print(ansi.red('overwriting!'))
                prep_data(data_file, args.y, args.d)
        else:
            print(ansi.green('Attempting to fetch input.'))
            prep_data(data_file, args.y, args.d)

    if 2 in part_nums:
        update_results(args.y, args.d, args.f)

if __name__ == '__main__':
    main()
