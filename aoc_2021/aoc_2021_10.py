with open('data/aoc_2021/10.txt') as f:
    dat = [x.strip() for x in f.readlines()]

def process_part1():
    illegal = []
    incomplete = []
    openers = ['<', '{', '(', '[']
    closers = ['>', '}', ')', ']']
    o_for_c = {a: b for a, b in zip(closers, openers)}
    c_for_o = {b: a for a, b in zip(closers, openers)}

    for line in dat:
        opened = []
        for ch in list(line):
            if ch in openers:
                opened += [ch]
            elif ch in closers:
                if o_for_c[ch] != opened[-1]:
                    illegal += [ch]
                    opened = []
                    break
                else:
                    opened.pop()
        if len(opened) != 0:
            incomplete += [list(reversed([c_for_o[x] for x in opened]))]

    scores = {')': 3, ']': 57, '}': 1197, '>': 25137}
    synscore = sum([scores[x] for x in illegal])
    return synscore, incomplete

def part1(output=False):
    synscore, _ = process_part1()
    return synscore

def part2(output=False):
    _, incomplete = process_part1()
    points = {')': 1, ']': 2, '}': 3, '>': 4}
    compscores = []
    for ic in incomplete:
        subscore = 0
        for icc in ic:
            subscore = subscore * 5 + points[icc]
        compscores += [subscore]

    compscore = sorted(compscores)[int((len(compscores)-1)/2)]
    return compscore
