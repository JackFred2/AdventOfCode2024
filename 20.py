import itertools
from collections import Counter

from utils.points import Point

def load_file():
    with open("inputs/20.txt") as f:
        walls = set()

        for (row, line) in enumerate(f.read().strip().split("\n")):
            for (col, char) in enumerate(line):
                p = Point(col, row)

                if char == "#":
                    walls.add(p)
                elif char == "S":
                    start_point = p
                elif char == "E":
                    end_point = p

    path = [start_point]

    current_pos = start_point
    while current_pos != end_point:
        neighbours = [n for n in current_pos.neighbours() if n not in walls and (len(path) == 1 or n != path[-2])]
        if len(neighbours) != 1:
            raise ValueError("Too many neighbours", current_pos)
        next = neighbours[0]
        path.append(next)
        current_pos = next


    return walls, path


walls, base_path = load_file()
path_to_index = dict((p, i) for (i, p) in enumerate(base_path))
#print(path_to_index)
width = max([p.x + 1 for p in walls])
height = max([p.y + 1 for p in walls])


def print_track(cheat: Point = None):
    s = ""

    for y in range(height):
        line = ""
        for x in range(width):
            p = Point(x, y)
            if p in walls:
                if p == cheat:
                    line += "░░"
                else:
                    line += "▓▓" if (x + y) % 2 == 0 else "██"
            elif p == base_path[0]:
                line += "St"
            elif p == base_path[-1]:
                line += "En"
            else:
                line += "  "
        s += line + "\n"

    print(s)


def part1():
    savings = Counter()

    for wall in walls:
        adjacent_path_points = [path_to_index[n] for n in wall.neighbours() if n in path_to_index]

        if len(adjacent_path_points) < 2:
            continue

        saving = max(adjacent_path_points) - min(adjacent_path_points) - 2

        if saving > 0:
            savings[saving] += 1

    print(sum([v for (s, v) in savings.items() if s >= 100]))


def part2():
    # flower 'mask' of reachable points with a 20 length cheat
    max_cheat_length = 20
    flower: set[Point] = set()

    for (x_offset, y_offset) in itertools.product(range(-max_cheat_length, max_cheat_length + 1), repeat=2):
        p = Point(x_offset, y_offset)
        if abs(x_offset) + abs(y_offset) > max_cheat_length:
            continue

        flower.add(p)

    savings = Counter()

    for point in base_path:
        my_index = path_to_index[point]

        for (index, reached) in [(path_to_index[point + offset], point + offset) for offset in flower if (point + offset) in path_to_index]:
            cheat_distance = reached.manhattan_distance(point)
            if index <= my_index + cheat_distance: continue

            savings[index - my_index - cheat_distance] += 1

    print(sum([v for (s, v) in savings.items() if s >= 100]))

part1()
part2()

