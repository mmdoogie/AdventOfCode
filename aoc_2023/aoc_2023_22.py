with open('data/aoc_2023/22.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]

def parse():
    bricks = []
    for d in dat:
        l, r = d.split('~')
        ll = [int(x) for x in l.split(',')]
        rr = [int(x) for x in r.split(',')]
        assert ll[0] <= rr[0] and  ll[1] <= rr[1] and ll[2] <= rr[2]
        bricks += [ll + rr]
    return bricks

def make_tower(bricks):
    tower = {}
    blocks = {}
    for i, b in enumerate(bricks):
        grp = []
        for z in range(b[2], b[5] + 1):
            for y in range(b[1], b[4] + 1):
                for x in range(b[0], b[3] + 1):
                    tower[(x, y, z)] = i
                    grp += [(x, y, z)]
        blocks[i] = grp

    return tower, blocks

def settle_tower(tower, blocks, output = False, stop_after_change = False):
    changed = False
    moved_blocks = set()

    tower = dict(tower.items())
    blocks = dict(blocks.items())

    while True:
        moved = False
        tower_rem = []
        tower_add = []
        for t in tower:
            if (t[0], t[1], t[2] - 1) in tower:
                continue
            if t[2] == 1:
                continue
            block_group = blocks[tower[t]]
            drop_amt = 1
            while all((g[0], g[1], g[2] - drop_amt) not in tower or (g[0], g[1], g[2] - drop_amt) in block_group for g in block_group):
                drop_amt += 1
                if drop_amt == t[2]:
                    break
            drop_amt -= 1
            if drop_amt > 0:
                tower_rem += block_group
                tower_add += [(g[0], g[1], g[2] - drop_amt) for g in block_group]
                moved_blocks.add(tower[t])
                moved = True
                changed = True
                if output:
                    print('Moving block', tower[t], 'down by', drop_amt)
                break
        if moved:
            for r, a in zip(tower_rem, tower_add):
                i = tower[r]
                del tower[r]
                tower[a] = i
            blocks[i] = tower_add
        else:
            break
        if stop_after_change and changed:
            break

    return tower, blocks, moved_blocks

settled_tower = None
settled_blocks = None

def part1(output = True):
    global settled_tower, settled_blocks
    bricks = parse()
    tower, blocks = make_tower(bricks)

    if output:
        min_x = min(min(b[0], b[3]) for b in bricks)
        min_y = min(min(b[1], b[4]) for b in bricks)
        min_z = min(min(b[2], b[5]) for b in bricks)
        max_x = max(max(b[0], b[3]) for b in bricks)
        max_y = max(max(b[1], b[4]) for b in bricks)
        max_z = max(max(b[2], b[5]) for b in bricks)
        print(min_x, min_y, min_z)
        print(max_x, max_y, max_z)

    if settled_tower is None:
        settled_tower, settled_blocks, _ = settle_tower(tower, blocks, output = output)

    if output:
        print('Settled!')

    bids = sorted(set(settled_blocks))

    can_zap = 0
    for b in bids:
        test_tower = {k: v for k, v in settled_tower.items() if v != b}
        test_blocks = {k: v for k, v in settled_blocks.items() if k != b}
        _, _, moved_blocks = settle_tower(test_tower, test_blocks, stop_after_change = True)
        if len(moved_blocks) == 0:
            can_zap += 1
        if output:
            print('Zapping', b, 'moved', len(moved_blocks), 'blocks. Total zappable:', can_zap)

    return can_zap

def part2(output = True):
    global settled_tower, settled_blocks
    bricks = parse()
    tower, blocks = make_tower(bricks)

    if settled_tower is None:
        settled_tower, settled_blocks, _ = settle_tower(tower, blocks, False)

    if output:
        print('Settled!')

    bids = sorted(set(settled_blocks))
    total_moved = 0
    for b in bids:
        test_tower = {k: v for k, v in settled_tower.items() if v != b}
        test_blocks = {k: v for k, v in settled_blocks.items() if k != b}
        _, _, moved_blocks = settle_tower(test_tower, test_blocks, output = False)
        total_moved += len(moved_blocks)
        if output:
            print('Zapping', b, 'moved', len(moved_blocks), 'blocks. Total moved:', total_moved)

    return total_moved

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
