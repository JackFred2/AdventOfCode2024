from utils.points import Point

type Region = tuple[chr, set[Point]]

grid: dict[Point, chr] = dict()
regions: list[Region] = []

width = 0
height = 0

with open("inputs/12.txt") as f:
    for row, line in enumerate([l.strip() for l in f if l]):
        height = max(row, height)
        for col, char in enumerate(line):
            width = max(width, col)
            grid[Point(col, row)] = char


def calculate_regions():
    seen: set[Point] = set()

    for (point, char) in grid.items():
        if point in seen:
            continue

        region = set()
        to_check = {point}

        while to_check:
            p = to_check.pop()
            region.add(p)
            seen.add(p)

            for n in p.neighbours():
                if n in grid and n not in seen and grid[n] == char:
                    to_check.add(n)

        regions.append((char, region))
        seen.add(point)


calculate_regions()


def part1():
    total = 0

    for (char, region) in regions:
        area = len(region)
        touching = 0

        for point in region:
            for neighbour in point.neighbours():
                if neighbour in grid and grid[neighbour] == char:
                    touching += 1

        total += area * (4 * area - touching)

    print(total)


# count corners
def part2():
    total = 0

    for (char, region) in regions:
        area = len(region)
        corner_count = 0

        for point in region:

            # outside corner(s)
            different_neighbours = [n for n in point.neighbours() if n not in grid or grid[n] != char]
            match len(different_neighbours):
                case 4:
                    corner_count += 4
                case 3:
                    corner_count += 2
                case 2:
                    if different_neighbours[0].x != different_neighbours[1].x and different_neighbours[0].y != different_neighbours[1].y:
                        corner_count += 1

            for offset in [Point(1, 1), Point(1, -1), Point(-1, -1), Point(-1, 1)]:
                a = point + (offset.x, 0)
                b = point + (0, offset.y)
                if all([p in grid and grid[p] == char for p in [a, b]]) and grid[point + offset] != char:
                    corner_count += 1
                    pass

        total += area * corner_count

    print(total)


part1()
part2()