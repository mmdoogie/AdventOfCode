with open('data/aoc_2023/07.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def hand_value(hand, j_as_joker = False):
    card_vals = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10}
    card_vals.update({x: int(x) for x in '98765432'})

    if j_as_joker:
        card_vals['J'] = 1

    card_val = sum((100**(4 - i)) * card_vals[h] for i, h in enumerate(hand))

    occurence = {h: sum(c == h for c in hand) for h in hand}

    if j_as_joker and 'J' in occurence:
        j_count = occurence['J']
        del occurence['J']
        if j_count == 5:
            occurence['A'] = 5
        else:
            top_card = max(occurence.items(), key = lambda x: (x[1], card_vals[x[0]]))[0]
            occurence[top_card] += j_count

    counts = sorted(occurence.values(), reverse = True)

    if counts[0] == 5:
        hand_val = 6
    elif counts[0] == 4:
        hand_val = 5
    elif counts[0] == 3 and counts[1] == 2:
        hand_val = 4
    elif counts[0] == 3:
        hand_val = 3
    elif counts[0] == 2 and counts[1] == 2:
        hand_val = 2
    elif counts[0] == 2 and counts[1] == 1:
        hand_val = 1
    else:
        hand_val = 0

    return hand_val * 100 ** 5 + card_val

def part1(output = True):
    hand_vals = [hand_value(d.split(' ')[0]) for d in dat]
    hand_bids = [int(d.split(' ')[1]) for d in dat]

    type_bid = sorted(((v, b) for v, b in zip(hand_vals, hand_bids)), key = lambda x: x[0])
    winnings = sum((i + 1) * t[1] for i, t in enumerate(type_bid))

    return winnings

def part2(output = True):
    hand_vals = [hand_value(d.split(' ')[0], j_as_joker = True) for d in dat]
    hand_bids = [int(d.split(' ')[1]) for d in dat]

    type_bid = sorted(((v, b) for v, b in zip(hand_vals, hand_bids)), key = lambda x: x[0])
    winnings = sum((i + 1) * t[1] for i, t in enumerate(type_bid))

    return winnings

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
