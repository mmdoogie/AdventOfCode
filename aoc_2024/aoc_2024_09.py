from dataclasses import dataclass

from mrm.iter import batched

@dataclass
class File:
    loc: int
    size: int
    fid: int = -1

def parse():
    with open('data/aoc_2024/09.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    if len(lines[0]) % 2 == 1:
        lines[0] += '0'
    files, spaces = [], []
    loc = 0
    for fid, (filesize, spacesize) in enumerate(batched(lines[0], batch_size=2)):
        filesize, spacesize = int(filesize), int(spacesize)
        files += [File(loc, filesize, fid)]
        loc += filesize
        spaces += [File(loc, spacesize)]
        loc += spacesize
    return files, spaces

def checksum(files):
    return sum(sum(block * f.fid for block in range(f.loc, f.loc + f.size)) for f in files)

def part1(output=False):
    files, spaces = parse()

    from_files = iter(sorted(files, key=lambda f: f.loc, reverse=True))
    from_file = next(from_files)
    split_files = []
    for s in spaces:
        while s.size:
            if from_file.loc < s.loc:
                break
            if from_file.size <= s.size:
                from_file.loc = s.loc
                s.size -= from_file.size
                s.loc += from_file.size
                from_file = next(from_files)
            else:
                from_file.size -= s.size
                split_files += [File(s.loc, s.size, from_file.fid)]
                s.size = 0
        if from_file.loc < s.loc:
            break

    return checksum(files + split_files)

def part2(output=False):
    files, spaces = parse()

    for f in sorted(files, key=lambda f: f.loc, reverse=True):
        for s in spaces:
            if s.loc > f.loc:
                break
            if s.size >= f.size:
                f.loc = s.loc
                s.size -= f.size
                s.loc += f.size
                break

    return checksum(files)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
