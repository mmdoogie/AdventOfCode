def parse():
    with open('data/aoc_2022/11.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    monkeys = []
    for n in range(8):
        m = {}
        m["items"] = [int(x) for x in lines[n*7+1].split(":")[1].split(",")]
        ops = lines[n*7+2].split("= ")[1].split(" ")
        if ops[2] != "old":
            m["opv"] = int(ops[2])
            if ops[1] == "*":
                m["op"] = lambda x, y: x * y
            else:
                m["op"] = lambda x, y: x + y
        else:
            m["opv"] = 0
            m["op"] = lambda x, y: x * x
        m["tdiv"] = int(lines[n*7+3].split("by ")[1])
        m["dt"] = int(lines[n*7+4].split("monkey ")[1])
        m["df"] = int(lines[n*7+5].split("monkey ")[1])
        m["count"] = 0
        monkeys += [m]
    return monkeys

def part1(output=False):
    monkeys = parse()

    for n in range(20):
        for m in monkeys:
            for i in m["items"]:
                m["count"] += 1
                worry = i
                worry = m["op"](worry, m["opv"])
                worry = int(worry / 3)
                if worry % m["tdiv"] == 0:
                    monkeys[m["dt"]]["items"] += [worry]
                else:
                    monkeys[m["df"]]["items"] += [worry]
            m["items"] = []

    cnts = [m["count"] for m in monkeys]
    cnts.sort(reverse=True)
    return cnts[0] * cnts[1]

def part2(output=False):
    monkeys = parse()

    mod = 1
    for m in monkeys:
        mod *= m["tdiv"]

    for n in range(10000):
        for m in monkeys:
            for i in m["items"]:
                m["count"] += 1
                worry = i
                worry = m["op"](worry, m["opv"])
                worry = worry % mod
                if worry % m["tdiv"] == 0:
                    monkeys[m["dt"]]["items"] += [worry]
                else:
                    monkeys[m["df"]]["items"] += [worry]
            m["items"] = []

    cnts = [m["count"] for m in monkeys]
    cnts.sort(reverse=True)
    return cnts[0] * cnts[1]
