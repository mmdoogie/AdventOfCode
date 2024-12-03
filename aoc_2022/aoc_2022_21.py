def parse():
    with open('data/aoc_2022/21.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]

    monkeys = {}
    for l in lines:
        p = l.split(": ")
        name = p[0]
        if p[1].isnumeric():
            op = "yell"
            nl = None
            nr = None
            val = int(p[1])
        else:
            s = p[1].split(" ")
            nl = s[0]
            op = s[1]
            nr = s[2]
            val = None
        monkeys[name] = {"op": op, "nl": nl, "nr": nr, "val": val}

    return monkeys

def part1(output=False):
    monkeys = parse()
    while not monkeys["root"]["val"]:
        for n,m in monkeys.items():
            if m["val"]:
                continue
            if monkeys[m["nl"]]["val"] and monkeys[m["nr"]]["val"]:
                os = str(monkeys[m["nl"]]["val"]) + m["op"] + str(monkeys[m["nr"]]["val"])
                m["val"] = int(eval(os))

    return monkeys["root"]["val"]

def part2(output=False):
    monkeys = parse()
    monkeys["humn"]["val"] = None

    # Phase 1 - propagate values like in part 1, until one of the two root args are available.
    # Also make a list of the monkeys depending on humn for Phase 2
    rootVal = None
    leftSide = False
    nhc = False
    needHumn = []
    while nhc or not rootVal:
        nhc = False
        for n,m in monkeys.items():
            if m["val"] or n == "humn":
                continue
            if m["nl"] == "humn" or m["nr"] == "humn":
                if n not in needHumn:
                    needHumn += [n]
                    nhc = True
                continue
            if n == "root":
                if monkeys[m["nl"]]["val"]:
                    rootVal = monkeys[m["nl"]]["val"]
                    leftSide = True
                if monkeys[m["nr"]]["val"]:
                    rootVal = monkeys[m["nr"]]["val"]
                    leftSide = False
                continue
            if not monkeys[m["nl"]]["val"]:
                if m["nl"] in needHumn and n not in needHumn:
                    needHumn += [n]
                    nhc = True
            elif not monkeys[m["nr"]]["val"]:
                if m["nr"] in needHumn and n not in needHumn:
                    needHumn += [n]
                    nhc = True
            else:
                os = str(monkeys[m["nl"]]["val"]) + m["op"] + str(monkeys[m["nr"]]["val"])
                m["val"] = int(eval(os))

    # Set the opposite side value to the value from Phase 1
    if leftSide:
        monkeys[monkeys["root"]["nr"]]["val"] = rootVal
    else:
        monkeys[monkeys["root"]["nl"]]["val"] = rootVal

    invOp = {"+":"-", "-":"+", "*":"/", "/":"*"}

    # Phase 2 - propagate values in reverse by performing inverse operations.
    while not monkeys["humn"]["val"]:
        for n in needHumn:
            am = monkeys[n]
            lm = monkeys[am["nl"]]
            rm = monkeys[am["nr"]]

            # Requires two forms when solving for the righthand argument
            # Add and multiply are transitive, subtract and divide are not
            # a = b + c --> c = a - b
            # a = b * c --> c = a / b
            # a = b - c --> c = b - a
            # a = b / c --> c = b / a
            if am["val"] and lm["val"] and not rm["val"]:
                if am["op"] in "+*":
                    rm["val"] = int(eval(str(am["val"]) + invOp[am["op"]] + str(lm["val"])))
                else:
                    rm["val"] = int(eval(str(lm["val"]) + am["op"] + str(am["val"])))

            # Only one form when solving for the lefthand argument
            # a = b + c --> b = a - c
            # a = b * c --> b = a / c
            # a = b - c --> b = a + c
            # a = b / c --> b = a * c
            if am["val"] and rm["val"] and not lm["val"]:
                lm["val"] = int(eval(str(am["val"]) + invOp[am["op"]] + str(rm["val"])))

    return monkeys["humn"]["val"]
