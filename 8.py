import itertools
from typing import TypeAlias

Antinodes: TypeAlias = dict[chr, list[tuple[int, int]]]
FrequencyMap: TypeAlias = dict[chr, list[tuple[int, int]]]

grid: list[list[chr]] = []
frequency_map: FrequencyMap = dict()


with open("inputs/8.txt") as f:
    for (row, line) in enumerate(f):
        grid.append([])
        for (column, char) in enumerate(line.strip()):
            grid[row].append(char)

            if char != ".":
                if not char in frequency_map:
                    frequency_map[char] = []

                frequency_map[char].append((row, column))


height = len(grid)
width = len(grid[0])


def within_bounds(pos: tuple[int, int]) -> bool:
    return 0 <= pos[0] < height and 0 <= pos[1] < width


def calculate_antinodes() -> Antinodes:
    result = dict()

    for (char, antennae) in frequency_map.items():
        result[char] = []
        for (a, b) in itertools.combinations(antennae, 2):
            behind_a = (2 * a[0] - b[0], 2 * a[1] - b[1])
            behind_b = (2 * b[0] - a[0], 2 * b[1] - a[1])
            if within_bounds(behind_a):
                result[char].append(behind_a)
            if within_bounds(behind_b):
                result[char].append(behind_b)

    return result


def calculate_antinodes_full() -> Antinodes:
    result = dict()

    for (char, antennae) in frequency_map.items():
        result[char] = []
        for (a, b) in itertools.combinations(antennae, 2):
            offset = (a[0] - b[0], a[1] - b[1])

            pos = a

            while within_bounds(pos):
                result[char].append(pos)
                pos = (pos[0] + offset[0], pos[1] + offset[1])

            pos = b

            while within_bounds(pos):
                result[char].append(pos)
                pos = (pos[0] - offset[0], pos[1] - offset[1])

    return result


def part1():
    print(len(set([pos for antis in calculate_antinodes().values() for pos in antis])))


def part2():
    print(len(set([pos for antis in calculate_antinodes_full().values() for pos in antis])))

part1()
part2()
