import functools
import operator
import re
from collections import Counter
from dataclasses import dataclass

from utils.points import Point


@dataclass
class Robot:
    start_position: Point
    velocity: Point


SIZE = Point(101, 103)
robots: list[Robot] = []

with open("inputs/14.txt") as f:
    for line in f.read().strip().split("\n"):
        match = re.search("p=(\\d+,\\d+) v=(-?\\d+,-?\\d+)", line)

        if match:
            robots.append(Robot(
                Point(*map(int, match.group(1).split(","))),
                Point(*map(int, match.group(2).split(",")))
            ))
        else:
            raise ValueError("Unknown robot", line)

def part1():
    robot_positions: list[Point] = []
    seconds = 100

    for robot in robots:
        pos = (robot.start_position + robot.velocity * seconds) % SIZE
        robot_positions.append(pos)

    center = SIZE // 2

    quadrants = Counter()

    for pos in robot_positions:
        diff = pos - center
        if diff.x == 0 or diff.y == 0: # irrelevant
            continue
        else:
            quadrants[diff.sign()] += 1

    print(functools.reduce(operator.mul, quadrants.values(), 1))


def print_bots(robots: list[Point]) -> str:
    flat = set(robots)

    lines = []
    for row in range(SIZE.y):
        lines.append(
            "".join(["██" if Point(col, row) in flat else "  " for col in range(SIZE.x)])
        )

    return "\n".join(lines)


def step(bots: list[tuple[Point, Point]], size):
    return [((bot[0] + bot[1] * size) % SIZE, bot[1]) for bot in bots]


# could have written a neighbour count threshold, but I wasn't sure on the output image format at the time
# initially printed the first few hundred and found a recurring similar pattern; changed to only output on those steps
# and looked through until found
# 'initial offset' may be different for you
def part2():
    initial_offset = 13
    cycle_step = 101

    bots = [(bot.start_position, bot.velocity) for bot in robots]
    bots = step(bots, initial_offset)

    with open("14_out.txt", mode="w", encoding="UTF-8") as f:
        for i in range(initial_offset, 10_000, cycle_step):
            f.write(str(i) + "\n\n")

            f.write(print_bots([bot[0] for bot in bots]))
            f.write("\n\n")

            bots = step(bots, cycle_step)


part1()
part2()