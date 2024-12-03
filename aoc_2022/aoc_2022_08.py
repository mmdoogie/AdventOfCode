def parse():
    with open('data/aoc_2022/08.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    cols = []
    for x in range(len(lines[0])):
        cols += [[]]

    for l in lines:
        for n,x in enumerate(l):
            cols[n] += [x]
    return lines, cols

def part1(output=False):
    lines, cols = parse()

    vis = []
    for n,l in enumerate(lines):
        for x in range(len(l)):
            if all([v<l[x] for v in l[0:x]]):
                vis += [(x,n)]
            if all([v<l[x] for v in l[x+1:]]):
                vis += [(x,n)]

    for n,c in enumerate(cols):
        for x in range(len(c)):
            if all([v<c[x] for v in c[0:x]]):
                vis += [(n,x)]
            if all([v<c[x] for v in c[x+1:]]):
                vis += [(n,x)]

    visCount = len(set(vis))
    return visCount

def part2(output=False):
    lines, cols = parse()
    bestScore = 0
    for x in range(len(cols)):
        for y in range(len(lines)):
            val = lines[y][x]

            left = list([x>=val for x in lines[y][0:x]])
            right = [x>=val for x in lines[y][x+1:]]
            top = [x>=val for x in cols[x][0:y]]
            bot = [x>=val for x in cols[x][y+1:]]
            
            left.reverse()
            top.reverse()
        
            leftScore = left.index(True) + 1 if True in left else len(left)
            rightScore = right.index(True) + 1 if True in right else len(right)
            topScore = top.index(True) + 1 if True in top else len(top)
            botScore = bot.index(True) + 1 if True in bot else len(bot)
            
            score = leftScore * rightScore * topScore * botScore
            if score > bestScore:
                bestScore = score
    return bestScore
