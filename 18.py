import dataclasses
import itertools
import queue
from collections import defaultdict
from dataclasses import field

from utils.points import Point


def read_input():
    coords = []

    with open("inputs/18.txt") as f:

        for line in f.read().strip().split("\n"):
            x, y = map(int, line.split(","))
            coords.append(Point(x, y))

    return coords

coords = read_input()
grid_size = 71

def make_grid(coords: list[Point]):
    grid = list()

    for coord in coords:
        grid.append(coord)

    return grid


def print_grid(grid: list[Point]):
    as_set = set(grid)

    s = ""

    edges = {-1, grid_size}

    for col in range(-1, grid_size + 1):
        for row in range(-1, grid_size + 1):
            if Point(row, col) in as_set or row in edges or col in edges:
                s += "██"
            else:
                s += "  "
        s += "\n"

    print(s)

grid = make_grid(coords)
#print_grid(grid[:1024])


@dataclasses.dataclass(order=True)
class PrioItem:
    priority: int
    item: Point = field(compare=False)


def dijkstra(grid: list[Point], start: Point, end: Point) -> list[Point] | None:
    as_set = set(grid)
    inverse = set()

    for (x, y) in itertools.product(range(grid_size), repeat=2):
        if Point(x, y) not in as_set:
            inverse.add(Point(x, y))

    q = queue.PriorityQueue()
    distances = defaultdict(lambda: 1_000_000)
    prev = dict()

    for p in inverse:
        q.put(PrioItem(1_000_000, p))

    distances[start] = 0
    q.put(PrioItem(0, start))

    while not q.empty():
        node: Point = q.get_nowait().item

        for neighbour in [n for n in node.neighbours() if n in inverse]:
            alt = distances[node] + 1
            if alt < distances[neighbour]:
                prev[neighbour] = node
                distances[neighbour] = alt

                q.put(PrioItem(alt, neighbour))

    path = []

    node = end

    while node in prev and node != start:
        path.insert(0, node)
        node = prev[node]

    if node != start:
        return None

    return path


def part1():
    print(len(dijkstra(grid[:1024], Point(0, 0), Point(grid_size - 1, grid_size - 1))))


def part2():
    start = Point(0, 0)
    end = Point(grid_size - 1, grid_size - 1)

    blocks = []
    path = dijkstra(blocks, start, end)
    path_as_set = set(path)

    i = 0

    for i in range(len(grid)):
        blocks = grid[:i]
        if any([b in path_as_set for b in blocks]):
            path = dijkstra(blocks, start, end)
            if not path:
                break
            path_as_set = set(path)

    print(grid[i - 1])


part1()
part2()
