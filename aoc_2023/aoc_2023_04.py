with open('data/aoc_2023/04.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def part1(output = True):
    total_points = 0

    for d in dat:
        win_numbers, my_numbers = d.split(': ')[1].split(' | ')
        win_numbers = [int(x) for x in win_numbers.split(' ') if x != '']
        my_numbers = [int(x) for x in my_numbers.split(' ') if x != '']

        card_matches = sum(w in my_numbers for w in win_numbers)
        if card_matches >= 1:
            total_points += pow(2, card_matches - 1)

    return total_points

def part2(output = True):
    card_points = {}
    card_counts = {}

    for i, d in enumerate(dat):
        win_numbers, my_numbers = d.split(': ')[1].split(' | ')
        win_numbers = [int(x) for x in win_numbers.split(' ') if x != '']
        my_numbers = [int(x) for x in my_numbers.split(' ') if x != '']

        card_points[i] = sum(w in my_numbers for w in win_numbers)
        card_counts[i] = 1

    for i, pts in card_points.items():
        for x in range(pts):
            card_counts[i + 1 + x] += card_counts[i]

    return sum(card_counts.values())

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
