import itertools
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Self

from utils.points import Point


with open("inputs/16.txt") as f:
    raw_grid = set()

    for (row_index, row) in enumerate(f.read().strip().split("\n")):
        for (col_index, char) in enumerate(row):
            point = Point(col_index, row_index)

            if char != "#":
                if char == "E":
                    end_pos = point
                elif char == "S":
                    start_pos = point
                raw_grid.add(point)


direction_symbols = {
    Point(1, 0): "[>]",
    Point(-1, 0): "[<]",
    Point(0, 1): "[v]",
    Point(0, -1): "[^]"
}


@dataclass
class Node:
    pos: Point
    direction: Point
    edges: dict[Self, int] = field(default_factory=dict)

    def link(self: Self, other: Self, score: int, both_ways: bool = False):
        self.edges[other] = score
        if both_ways:
            other.edges[self] = score

    def as_text(self):
        return f"{self.pos}@{direction_symbols[self.direction]}"

    def __hash__(self):
        return hash((self.pos, self.direction))

    def __repr__(self):
        return f"Node({self.as_text()}, edges={[(o.as_text(), score) for (o, score) in self.edges.items()]})"


@dataclass
class Graph:
    nodes: list[Node]


def same_axis(a: Point, b: Point):
    return a.x == b.x or a.y == b.y


def calculate_graph():
    # calculate 4 nodes at:
    # - start
    # - end
    # - dead end
    # - intersections
    # - corners for simplicity
    nodes: list[Node] = []

    for pos in raw_grid:
        neighbours = [n for n in pos.neighbours() if n in raw_grid]
        if pos == start_pos or pos == end_pos or len(neighbours) != 2 or not same_axis(*neighbours):
            nodes_here = [Node(pos, dir) for dir in Point.cardinal()]

            for (a, b) in itertools.combinations(nodes_here, r=2):
                if a.direction != -b.direction:
                    a.link(b, 1000, True)

            nodes += nodes_here

    node_lookup = dict()
    for node in nodes:
        node_lookup[node.pos, node.direction] = node

    for node in nodes:
        pos = node.pos + node.direction
        if not pos in raw_grid:
            continue
        distance = 1
        while (pos, node.direction) not in node_lookup and distance < 200:
            pos += node.direction
            distance += 1
        if distance >= 200:
            raise ValueError()
        other = node_lookup[(pos, node.direction)]

        node.link(other, distance)

    return Graph(nodes), node_lookup[(start_pos, Point(1, 0))]


(graph, start_node) = calculate_graph()


def path_to_points(path: list[Node]) -> set[Point]:
    points = set()

    for (fr, to) in itertools.pairwise(path):
        if fr.direction == to.direction:
            for i in range(to.pos.manhattan_distance(fr.pos) + 1):
                points.add(fr.pos + fr.direction * i)

    return points


def calc_part_2(came_from: dict[Node, list[Node]], end_nodes: set[Node]):
    paths = []

    def walk_path(current_path: list[Node], node: Node):
        if node in came_from:
            nodes = came_from[node]

            for prev in nodes:
                walk_path([prev] + current_path[::], prev)
        else:
            paths.append(current_path)

    for end in end_nodes:
        walk_path([end], end)

    total_points = set()

    for path in paths:
        #print([n.as_text() for n in path])
        total_points.update(path_to_points(path))
    print(len(total_points))
    return


def work():
    def h(node: Node):
        return 0
        #return node.pos.manhattan_distance(end_pos)

    open = {start_node}
    came_from: dict[Node, list[Node]] = defaultdict(lambda: list())
    g_score = defaultdict(lambda: 1000000)
    g_score[start_node] = 0
    f_score = defaultdict(lambda: 1000000)
    f_score[start_node] = h(start_node)

    end_score = 100000000000
    shown_minimum = False

    while open:
        current_node = min(open, key=lambda n: f_score[n])
        if current_node.pos == end_pos :
            end_score = g_score[current_node]

            # first found is optimal for lowest route, however need to find overall lowest for part 2
            if not shown_minimum:
                print(end_score)
                shown_minimum = True

        open.remove(current_node)
        for (neighbour, score) in current_node.edges.items():
            tentative = g_score[current_node] + score
            if tentative < g_score[neighbour]:
                came_from[neighbour] = [current_node]
                g_score[neighbour] = tentative
                f_score[neighbour] = tentative + h(neighbour)
                open.add(neighbour)
            elif tentative == g_score[neighbour]:
                came_from[neighbour].append(current_node)

    calc_part_2(came_from, set([n for (n, score) in g_score.items() if score == end_score]))


work()
