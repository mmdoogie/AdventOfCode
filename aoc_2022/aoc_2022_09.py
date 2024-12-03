def parse():
    with open('data/aoc_2022/09.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return lines

def part1(output=False):
    lines = parse()
    head = {"x":0, "y":0}
    tail = {"x":0, "y":0}

    def st(a):
        return str(a["x"]) + "," + str(a["y"])

    tailVisit = [st(tail)]

    for l in lines:
        parts = l.split(" ")
        for n in range(int(parts[1])):
            if parts[0] == 'L':
                head["x"] -= 1
            elif parts[0] == 'R':
                head["x"] += 1
            elif parts[0] == 'U':
                head["y"] -= 1
            elif parts[0] == 'D':
                head["y"] += 1

            dx = head["x"] - tail["x"]
            dy = head["y"] - tail["y"]
        
            udx = dx if dx > 0 else -dx
            udy = dy if dy > 0 else -dy

            sdx = 1 if dx > 0 else -1
            sdy = 1 if dy > 0 else -1

            if udy == 0 and udx == 2:
                tail["x"] += sdx
            elif udx == 0 and udy == 2:
                tail["y"] += sdy
            elif (udx == 1 and udy == 2) or (udx == 2 and udy == 1):
                tail["x"] += sdx
                tail["y"] += sdy

            tailVisit += [st(tail)]

    return len(set(tailVisit))

def part2(output=False):
    lines = parse()
    knots = []
    for n in range(10):
        knots += [{"x":0, "y":0}]

    def st(a):
        return str(a["x"]) + "," + str(a["y"])

    def updatePos(head, tail):
        dx = head["x"] - tail["x"]
        dy = head["y"] - tail["y"]

        udx = dx if dx > 0 else -dx
        udy = dy if dy > 0 else -dy

        sdx = 1 if dx > 0 else -1
        sdy = 1 if dy > 0 else -1

        if udy == 0 and udx == 2:
            tail["x"] += sdx
        elif udx == 0 and udy == 2:
            tail["y"] += sdy
        elif (udx >= 1 and udy == 2) or (udx == 2 and udy >= 1):
            tail["x"] += sdx
            tail["y"] += sdy
        
        return head, tail

    tailVisit = [st(knots[9])]

    for l in lines:
        parts = l.split(" ")
        for n in range(int(parts[1])):
            if parts[0] == 'L':
                knots[0]["x"] -= 1
            elif parts[0] == 'R':
                knots[0]["x"] += 1
            elif parts[0] == 'U':
                knots[0]["y"] -= 1
            elif parts[0] == 'D':
                knots[0]["y"] += 1

            for n in range(9):
                knots[n], knots[n+1] = updatePos(knots[n], knots[n+1])

            tailVisit += [st(knots[9])]

    return len(set(tailVisit))
