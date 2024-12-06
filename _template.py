from collections import Counter, defaultdict, deque, namedtuple
from functools import cache, cmp_to_key, partial, reduce
from itertools import combinations, cycle, groupby, permutations, product
import math
import operator
import random
import re

import mrm.ansi_term as ansi
from mrm.bitvector import Bitvector
from mrm.cache import Keycache
import mrm.cpoint as cpt
from mrm.crt import all_coprime, coprime, crt
from mrm.dijkstra import Dictlike, dijkstra
from mrm.graph import prim_mst
import mrm.image as img
from mrm.iter import batched, sliding_window
import mrm.llist as llist
from mrm.parse import ensure_equal_length
import mrm.point as pt
from mrm.search import fn_binary_search
from mrm.text import let2num, num2let
from mrm.tsp import held_karp, held_karp_dist
from mrm.util import big_pi, md5sum

def parse():
    with open('data/aoc_{YEAR}/{DAY}.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return lines

def part1(output=False):
    lines = parse()
    return ''

def part2(output=False):
    lines = parse()
    return ''

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
