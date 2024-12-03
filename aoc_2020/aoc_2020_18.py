import operator
import re

with open('data/aoc_2020/18.txt') as f:
    dat = [x.strip() for x in f.readlines()]

def part1(output=False):
    totalSum = 0

    for d in dat:
        val = 0
        op = operator.add

        l = d.split(' ')
        wait = []
        for c in l:
            if c in '123456789':
                val = op(val, int(c))
            elif c in '+*':
                if c == '+':
                    op = operator.add
                else:
                    op = operator.mul
            elif c[0] == '(':
                i = 0
                while c[i] == '(':
                    wait.append((val, op))
                    val = 0
                    op = operator.add
                    i += 1
                val = int(c[i:])
            elif c.endswith(')'):
                idx = c.find(')')
                val = op(val, int(c[:idx]))
                for n in range(idx, len(c)):
                    v = val
                    (val, op) = wait.pop()
                    val = op(val, v)

        totalSum += val

    return totalSum

def parteval(part):
    plusre = re.compile('(([0-9]+) \+ ([0-9]+))')
    mulre = re.compile('(([0-9]+) \* ([0-9]+))')
    el = part

    while True:
        p = plusre.search(el)
        if not p:
            break
        rep = str(int(p.groups()[1]) + int(p.groups()[2]))
        el = plusre.sub(rep, el, count = 1)

    while True:
        m = mulre.search(el)
        if not m:
            break
        rep = str(int(m.groups()[1]) * int(m.groups()[2]))
        el = mulre.sub(rep, el, count = 1)

    if el[0] == '(':
        return el[1:-1]
    else:
        return el

def part2(output=False):
    totalSum = 0

    parenthetical = re.compile('(\([0-9+* ]+\))')

    for d in dat:
        el = d
        while True:
            p = parenthetical.search(el)
            if not p:
                break
            el = parenthetical.sub(parteval(p.groups()[0]), el, count = 1)
        el = parteval(el)
        totalSum += int(el)

    return totalSum
