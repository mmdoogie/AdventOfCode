with open('data/aoc_2018/09.txt') as f:
    dat = [x.strip() for x in f.readlines()]

def play_game(players, marbles):
    l_next = {0: 0}
    l_prev = {0: 0}
    current_marble = 0

    used = 0
    player = 0
    scores = [0] * players
    while used < marbles:
        used += 1
        if used % 23 == 0:
            scores[player] += used
            dst = current_marble
            for _ in range(7):
                dst = l_prev[dst]
            scores[player] += dst
            l_next[l_prev[dst]] = l_next[dst]
            l_prev[l_next[dst]] = l_prev[dst]
            current_marble = l_next[dst]
            del l_next[dst], l_prev[dst]
        else:
            l_next[used] = l_next[l_next[current_marble]]
            l_prev[used] = l_next[current_marble]
            l_prev[l_next[l_next[current_marble]]] = used
            l_next[l_next[current_marble]] = used
            current_marble = used
        player = (player + 1) % players
    return max(scores)

def part1(output = True):
    players = int(dat[0].split(' players')[0])
    marbles = int(dat[0].split('worth ')[1].split(' points')[0])

    if output:
        assert play_game(9, 25) == 32
        assert play_game(10, 1618) == 8317
        assert play_game(13, 7999) == 146373
        assert play_game(17, 1104) == 2764
        assert play_game(21, 6111) == 54718
        assert play_game(30, 5807) == 37305

    if output:
        print('Players:', players)
        print('Marbles:', marbles)

    return play_game(players, marbles)

def part2(output = True):
    players = int(dat[0].split(' players')[0])
    marbles = int(dat[0].split('worth ')[1].split(' points')[0])
    
    if output:
        print('Now with Marbles:', marbles * 100)

    return play_game(players, marbles * 100)
