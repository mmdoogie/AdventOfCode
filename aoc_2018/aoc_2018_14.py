with open('data/aoc_2018/14.txt') as f:
    dat = [x.strip() for x in f.readlines()]

def lln(val):
    return [val, None]

def ll_next(node):
    return node[1]

def ll_val(node):
    return node[0]

def multi_ll_next(node, steps):
    n = node
    for i in range(steps):
        n = ll_next(n)
    return n

def ll_ins_after(after, node):
    node[1] = after[1]
    after[1] = node

def part1(output = True):
    steps = int(dat[0])

    elf1 = lln(3)
    elf2 = lln(7)
    eol = elf2
    elf1[1] = elf2
    elf2[1] = elf1
    recipes_cnt = 2
    result_node = None

    while True:
        res = [int(c) for c in str(ll_val(elf1) + ll_val(elf2))]
        for r in res:
            n = lln(r)
            ll_ins_after(eol, n)
            eol = n
            recipes_cnt += 1
        elf1 = multi_ll_next(elf1, 1 + ll_val(elf1))
        elf2 = multi_ll_next(elf2, 1 + ll_val(elf2))
        if result_node is None and recipes_cnt >= steps - 10:
            result_node = eol
            result_cnt = recipes_cnt
        if recipes_cnt > steps + 10:
            break

    val = ''
    while True:
        val += str(ll_val(result_node))
        result_node = ll_next(result_node)
        if result_node == eol:
            break

    return int(val[steps - result_cnt + 1:steps - result_cnt + 1 + 10])

def part2(output = True):
    steps = [int(c) for c in dat[0]]

    elf1 = lln(3)
    elf2 = lln(7)
    eol = elf2
    elf1[1] = elf2
    elf2[1] = elf1
    recipes_cnt = 2

    result_cnt = 0
    match_idx = 0

    while True:
        res = [int(c) for c in str(ll_val(elf1) + ll_val(elf2))]
        for r in res:
            n = lln(r)
            if steps[match_idx] == r:
                if output and match_idx > 2:
                    print('Match idx', match_idx, 'cnt', recipes_cnt)
                if match_idx == 0:
                    result_cnt = recipes_cnt
                match_idx += 1
                if match_idx == 6:
                    return result_cnt
            else:
                match_idx = 0
            ll_ins_after(eol, n)
            eol = n
            recipes_cnt += 1
        elf1 = multi_ll_next(elf1, 1 + ll_val(elf1))
        elf2 = multi_ll_next(elf2, 1 + ll_val(elf2))

    return 0
