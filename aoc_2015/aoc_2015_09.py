from mrm.tsp import held_karp

with open('data/aoc_2015/09.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def build_graph():
    ngh = {}
    wts = {}
    for d in dat:
        parts = d.split(' ')
        from_city = parts[0]
        to_city = parts[2]
        dist = int(parts[4])
        ngh[from_city] = to_city
        ngh[to_city] = from_city
        wts[(from_city, to_city)] = dist
        wts[(to_city, from_city)] = dist
    return ngh, wts

def part1(output = True):
    ngh, wts = build_graph()

    min_dist = sum(wts.values())
    for sp in ngh:
        d, p = held_karp(ngh, wts, dont_loop = True, start_point = sp)
        min_dist = min(min_dist, d)
        if output:
            print(f'From {sp:20} shortest dist {d:<5} on path {p}')

    return min_dist

def part2(output = True):
    ngh, wts = build_graph()

    max_dist = 0
    for sp in ngh:
        d, p = held_karp(ngh, wts, dont_loop = True, start_point = sp, min_fn = max)
        max_dist = max(max_dist, d)
        if output:
            print(f'From {sp:20}  longest dist {d:<5} on path {p}')

    return max_dist

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
