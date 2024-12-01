import re
from collections import Counter

left = []
right = []

with open("inputs/1.txt") as f:
    for line in f:
        match = re.match("(\\d+)\\s+(\\d+)", line)
        left.append(int(match.group(1)))
        right.append(int(match.group(2)))


def part1():
    print(sum([abs(x - y) for (x, y) in zip(sorted(left), sorted(right))]))


def part2():
    freq = Counter(right)
    print(sum([x * freq[x] for x in left]))


part1()
part2()

