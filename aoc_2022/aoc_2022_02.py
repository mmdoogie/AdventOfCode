def parse():
    with open('data/aoc_2022/02.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return lines

def shapePoints(x):
    return ord(x[1]) - ord('X') + 1

themToRPS = {'A': 'rock', 'B': 'paper', 'C': 'scissors'}
usToRPS = {'X': 'rock', 'Y': 'paper', 'Z': 'scissors'}
beats = {'rock': 'scissors', 'paper': 'rock', 'scissors': 'paper'}

def resultPoints(x):
    them, us = x
    themAction = themToRPS[them]
    usAction = usToRPS[us]

    if themAction == usAction:
        return 3
    elif beats[themAction] == usAction:
        return 0
    else:
        return 6

def part1(output=False):
    lines = parse()
    pairs = [tuple(x.strip().split(" ")) for x in lines]
    score = sum([shapePoints(x) + resultPoints(x) for x in pairs])

    return score

def part2(output=False):
    lines = parse()
    pairs = [tuple(x.strip().split(" ")) for x in lines]
    loses = {v: k for k, v in beats.items()}
    invUsToRPS = {v: k for k, v in usToRPS.items()}

    def calculatedAction(x):
        them, us = x
        themAction = themToRPS[them]
        if us == 'X':
            return invUsToRPS[beats[themAction]]
        elif us == 'Y':
            return invUsToRPS[themAction]
        else:
            return invUsToRPS[loses[themAction]]

    newPairs = [(x[0], calculatedAction(x)) for x in pairs]
    score2 = sum([shapePoints(x) + resultPoints(x) for x in newPairs])

    return score2
