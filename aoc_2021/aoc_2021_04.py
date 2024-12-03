with open('data/aoc_2021/04.txt', 'r') as f:
    dat = [x.strip() for x in f.readlines()]

calls = [int(x) for x in dat[0].split(',')]
numCards = int((len(dat) - 1) / 6)
txtCards = [dat[i*6+2 : i*6+2+5] for i in range(numCards)]

def checkCards(cards):
    for i, d in enumerate(cards):
        sums = [0, 0, 0, 0, 0]
        for r in d:
            if sum(r) == -5:
                return i
            for j, c in enumerate(r):
                sums[j] += c
        if any([s == -5 for s in sums]):
            return i
    return -1

def applyNumber(cards, num):
    for i, c in enumerate(cards):
        for j, r in enumerate(c):
            for k, v in enumerate(r):
                if v == num:
                    cards[i][j][k] = -1

def scoreCard(cards, c, n):
    card = cards[c]
    return sum([x for x in sum(card, []) if x != -1]) * n

def part1(output=False):
    cards = [[[int(y) for y in x.split(' ') if y != ''] for x in c] for c in txtCards]
    for n in calls:
        applyNumber(cards, n)
        c = checkCards(cards)
        if c != -1:
            return scoreCard(cards, c, n)

def getWinners(cards):
    winners = set()
    for i, d in enumerate(cards):
        sums = [0, 0, 0, 0, 0]
        for r in d:
            if sum(r) == -5:
                winners.add(i)
            for j, c in enumerate(r):
                sums[j] += c
        if any([s == -5 for s in sums]):
            winners.add(i)
    return winners

def part2(output=False):
    cards = [[[int(y) for y in x.split(' ') if y != ''] for x in c] for c in txtCards]
    winners = set()

    for n in calls:
        applyNumber(cards, n)
        winning = getWinners(cards)
        newWinners = winning.difference(winners)
        winners.update(newWinners)
        if len(newWinners) != 0:
            scores = [scoreCard(cards, w, n) for w in newWinners]

    return scores[0]

