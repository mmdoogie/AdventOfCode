from mrm.llist import llist

with open('data/aoc_2016/19.txt', encoding = 'utf-8') as f:
    dat = [x.strip('\n') for x in f.readlines()]
    elf_count = int(dat[0])
    #elf_count = 5

def part1(output = True):
    del output

    elves = llist(range(elf_count), circular=True)
    ce = elves.head()
    while len(elves) > 1:
        ce = ce.right()
        elves.drop(ce)
        ce = ce.right()
    return ce.val + 1

def part2(output = True):
    del output

    elves = llist(range(elf_count), circular=True)
    ce = elves.head()
    mp = ce.far_right(len(elves) // 2)
    while len(elves) > 1:
        elves.drop(mp)
        mp = mp.right()
        if len(elves) % 2 == 0:
            mp = mp.right()
        ce = ce.right()
    return ce.val + 1

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
