from functools import reduce

def part1(output=False):
    with open("data/aoc_2022/04.txt", mode="r") as file:
        lines = file.readlines()

    containsCount = 0
    overlapsCount = 0

    for l in lines:
        left, right = l.strip().split(",")

        leftMin, leftMax = left.split("-")
        rightMin, rightMax = right.split("-")

        leftMin = int(leftMin)
        leftMax = int(leftMax)
        rightMin = int(rightMin)
        rightMax = int(rightMax)

        if leftMin <= rightMin and leftMax >= rightMax:
            containsCount += 1
        elif rightMin <= leftMin and rightMax >= leftMax:
            containsCount += 1
        
        if leftMin >= rightMin and leftMin <= rightMax:
            overlapsCount += 1
        elif rightMin >= leftMin and rightMin <= leftMax:
            overlapsCount += 1

    return containsCount

def part2(output=False):
    with open("data/aoc_2022/04.txt", mode="r") as file:
        lines = file.readlines()

    containsCount = 0
    overlapsCount = 0

    for l in lines:
        left, right = l.strip().split(",")

        leftMin, leftMax = left.split("-")
        rightMin, rightMax = right.split("-")

        leftMin = int(leftMin)
        leftMax = int(leftMax)
        rightMin = int(rightMin)
        rightMax = int(rightMax)

        leftRange = range(leftMin, leftMax+1)
        rightRange = range(rightMin, rightMax+1)

        leftContains = all([x in rightRange for x in leftRange])
        rightContains = all([x in leftRange for x in rightRange])
        if leftContains or rightContains:
            containsCount += 1
        
        overlaps = any([x in rightRange for x in leftRange])
        if overlaps:
            overlapsCount += 1

    return overlapsCount
