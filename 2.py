import math
from itertools import pairwise

reports = []

with open("inputs/2.txt") as f:
    for line in f:
        reports.append([int(x) for x in line.split(" ")])


def sign(i: int) -> int:
    if i == 0:
        return 0
    elif i < 0:
        return -1
    else:
        return 1


def is_safe(report: [int]) -> bool:
    sgn = 0

    for (a, b) in pairwise(report):
        if sgn == 0:
            sgn = sign(a - b)
            if sgn == 0: # start with 2 same
                return False
        elif sgn != sign(a - b): # same direction
            return False

        if abs(a - b) > 3:
            return False

    return True


def part1():
    print(sum([is_safe(report) for report in reports]))


# cant fix by removing
def part2():
    count = 0

    for report in reports:
        if is_safe(report):
            count += 1
        else:
            for droppedIndex in range(len(report)):
                copy = [x for (i, x) in enumerate(report) if i != droppedIndex]
                if is_safe(copy):
                    count += 1
                    break

    print(count)


part1()
part2()