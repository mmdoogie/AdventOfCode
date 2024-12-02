def parse():
    with open('data/aoc_2019/22.txt') as f:
        dat = [x.strip() for x in f.readlines()]
    return dat

p1_decksize = 10007
p1_card = 2019

# Naïve array shuffling version works fine for Part 1
def cut(cards, pos):
    return cards[pos:] + cards[:pos]

def dealinto(cards):
    return cards[-1:0:-1] + [cards[0]]

def increment(cards, amt):
    new_order = [None] * p1_decksize
    for i in range(p1_decksize):
        new_order[(i * amt) % p1_decksize] = cards[i]
    return new_order

def part1_naive():
    dat = parse()
    cards = list(range(p1_decksize))
    for d in dat:
        if d.startswith('cut'):
            cards = cut(cards, int(d.split(' ')[1]))
        elif d.startswith('deal into'):
            cards = dealinto(cards)
        elif d.startswith('deal with'):
            cards = increment(cards, int(d.split('ment ')[1]))

    return cards.index(p1_card)


# Can reimplment all of these operations to just operate on a specific index
def cut_single(card, decksize, cutpos):
    return (card - cutpos) % decksize

def dealinto_single(card, decksize):
    return (-card - 1) % decksize

def increment_single(card, decksize, amt):
    return (amt * card) % decksize

def part1_single():
    dat = parse()
    idx = p1_card
    for d in dat:
        if d.startswith('cut'):
            idx = cut_single(idx, p1_decksize, int(d.split(' ')[1]))
        elif d.startswith('deal into'):
            idx = dealinto_single(idx, p1_decksize)
        elif d.startswith('deal with'):
            idx = increment_single(idx, p1_decksize, int(d.split('ment ')[1]))
    
    return idx

# Since these are all just add/multiply can redefine these as the modifications of coefficients
# Cut:       (  1 * card + -cutpos) % decksize
# Deal Into: ( -1 * card + -1     ) % decksize
# Increment: (amt * card +  0     ) % decksize
#         y =   m * card +  b, so store (m, b) and look at the effects of each operation

# 1 * (m * x + b) - cutpos so (m, b) -> (m, b - cutpos)
def cut_func(func, cutpos):
    m, b = func
    return (m, b - cutpos)

# -1 * (m * x + b) - 1 so -1 distributes in and (m, b) -> (-m, -b - 1)
def into_func(func):
    m, b = func
    return (-m, -b - 1)

# amt * (m * x + b) so amt distributes in giving (m, b) -> (amt * m, amt * b)
def incr_func(func, amt):
    m, b = func
    return (amt * m, amt * b)

# That lets us compose the entire shuffle sequence down into a single operation
# by applying each operation to the result of the previous
def compose_func(decksize):
    dat = parse()
    # Start from the identity operation, multiplies by 1 and doesn't offset, so index remains the same
    func = (1, 0)
    for d in dat:
        if d.startswith('cut'):
            func = cut_func(func, int(d.split(' ')[1]))
        elif d.startswith('deal into'):
            func = into_func(func)
        elif d.startswith('deal with'):
            func = incr_func(func, int(d.split('ment ')[1]))

    func = (func[0] % decksize, func[1] % decksize)
    return func

# Then we can apply the function to the index of interest
def part1_compose():
    func = compose_func(p1_decksize)
    return (p1_card * func[0] + func[1]) % p1_decksize

def part1(output=False):
    if output:
        print('Part 1 [Naïve]:  ', part1_naive())
        print('Part 1 [Index]:  ', part1_single())
        print('Part 1 [Compose]:', part1_compose())
    return part1_compose()

# That's the only thing that lets us do part 2, but we need to repeat the shuffle operation many times
def part2_func(decksize, repeats):
    # Get the single shuffle function
    func = compose_func(decksize)

    # Compose it with itself repeatedly to get the powers of 2
    # g(x) = f(f(x)); h(x) = g(g(x)) = f(f(f(f(x)))); ...
    i = 1
    funcs = {i: func}
    while i * 2 < repeats:
        m, b = func
        func = (pow(m, 2, decksize), (m * b + b) % decksize)
        i *= 2
        funcs[i] = func

    # Now add in some of those other powers to get the total count of shuffles covered
    remain = repeats - i
    order = list(reversed(list(funcs.keys())))
    while remain > 0:
        valid = [o <= remain for o in order]
        step = order[valid.index(True)]
        sm, sb = funcs[step]
        m, b = func
        func = ((sm * m) % decksize, (sm * b + sb) % decksize)
        remain -= step

    # This is the composed function that covers ALL of the repeats of the operations in one single operation
    return func

# Saw a tip that python's power function supports modulo and can be used for inverses
# a / b = a * 1/b = a * b^-1
def mod_div(a, b, m):
    return (a * pow(b, -1, m)) % m

# Part 2 asks where a card came from, so we need to know x such that f(x) = 2020
# We have y = m * x + b, so x = (y - b) / m
# We can tell normal division doesn't work here because it would very often be a non-integer but we've had integers everywhere else
def part2(output=False):
    p2_decksize = 119315717514047
    p2_repeats = 101741582076661
    full_func = part2_func(p2_decksize, p2_repeats)
    return mod_div(2020 - full_func[1], full_func[0], p2_decksize)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
