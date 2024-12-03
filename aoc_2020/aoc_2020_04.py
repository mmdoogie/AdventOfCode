import re

with open('data/aoc_2020/04.txt') as f:
    dat = [x.strip() for x in f.readlines()]

passports = []
ppt = {}
for line in dat:
    if line == '':
        passports += [ppt]
        ppt = {}
        continue
    for i in line.split(' '):
        k,v = i.split(':')
        ppt[k] = v

if len(ppt.keys()) != 0:
    passports += [ppt]

def part1(output=False):
    required = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
    
    valid = 0
    for p in passports:
        if all([x in p for x in required]):
            valid += 1

    return valid

def part2(output=False):
    required = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
    color = re.compile('^#[0-9a-f]{6}$')
    pid = re.compile('^[0-9]{9}$')

    valid = 0
    for p in passports:
        if any([x not in p for x in required]):
            continue
        
        chk = 0
        for k, v in p.items():
            if k == 'byr':
                if int(v) >= 1920 and int(v) <= 2002:
                    chk += 1
            elif k == 'iyr':
                if int(v) >= 2010 and int(v) <= 2020:
                    chk += 1
            elif k == 'eyr':
                if int(v) >= 2020 and int(v) <= 2030:
                    chk += 1
            elif k == 'hgt':
                if v[-2:] == 'cm':
                    if int(v[:-2]) >= 150 and int(v[:-2]) <= 193:
                        chk += 1
                elif v[-2:] == 'in':
                    if int(v[:-2]) >= 59 and int(v[:-2]) <= 76:
                        chk += 1
            elif k == 'hcl':
                if color.match(v):
                    chk += 1
            elif k == 'ecl':
                if v in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
                    chk += 1
            elif k == 'pid':
                if pid.match(v):
                    chk += 1
        if chk == 7:
            valid += 1

    return valid
