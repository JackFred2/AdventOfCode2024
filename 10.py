import itertools

from utils.points import Point

grid: list[list[int]] = []

with open("inputs/10.txt") as f:
    for line in f.read().split("\n"):
        if line:
            grid.append([int(c) if c != "." else -1 for c in line])

height = len(grid)
width = len(grid[0])

START = 0
TARGET = 9

total_cache: dict[Point, int] = dict()


def in_bounds(point: Point) -> bool:
    return 0 <= point.x < width and 0 <= point.y < height


def get_score_for(point: Point) -> int:
    if point in total_cache:
        return total_cache[point]


    result = _get_score_for(point)
    total_cache[point] = result
    return result


def _get_score_for(point: Point) -> int:
    if not in_bounds(point):
        return 0

    current = grid[point.y][point.x]

    if current == TARGET:
        return 1
    else:
        target = current + 1
        total = 0

        for neighbour in point.neighbours():
            if in_bounds(neighbour) and grid[neighbour.y][neighbour.x] == target:
                total += get_score_for(neighbour)

        return total


def part1():
    total = 0

    for row, col in itertools.product(range(height), range(width)):
        if grid[row][col] == START:
            found = set()

            to_search = {Point(col, row)}

            while to_search: # is not empty
                point = to_search.pop()
                current = grid[point.y][point.x]
                if current == TARGET:
                    found.add(point)
                else:
                    for neighbour in point.neighbours():
                        if in_bounds(neighbour) and grid[neighbour.y][neighbour.x] == current + 1:
                            to_search.add(neighbour)

            total += len(found)

    print(total)


def part2():
    total = 0

    for row, col in itertools.product(range(height), range(width)):
        if grid[row][col] == START:
            total += get_score_for(Point(col, row))

    print(total)

part1()
part2()