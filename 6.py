import itertools
from typing import TypeAlias, Literal

with open("inputs/6.txt") as f:
    grid = [l for l in f.read().split("\n") if l] # remove blank

width = len(grid[0])
height = len(grid)


Direction: TypeAlias = Literal["north", "east", "south", "west"]
Position: TypeAlias = tuple[int, int]
PositionAndDir: TypeAlias = tuple[Position, Direction]


for (row, col) in itertools.product(range(height), range(width)):
    if grid[row][col] == "^":
        start_col = col
        start_row = row
        break


directions = {
    "north": (-1, 0),
    "east": (0, 1),
    "south": (1, 0),
    "west": (0, -1)
}


clockwise = {
    "north": "east",
    "east": "south",
    "south": "west",
    "west": "north"
}


def outside(pos: Position) -> bool:
    return pos[0] < 0 or pos[0] >= height or pos[1] < 0 or pos[1] >= width


Result: TypeAlias = tuple[bool, set[Position]] # loops, visited
def walk(obstruction: Position | None = None) -> Result:
    pos = (start_row, start_col)

    direction: Direction = "north"
    seen: set[PositionAndDir] = {(pos, "north")}

    for _ in range(100_000):
        next_pos = (directions[direction][0] + pos[0], directions[direction][1] + pos[1])

        if outside(next_pos):
            return False, set([pos[0] for pos in seen])
        elif grid[next_pos[0]][next_pos[1]] == "#" or next_pos == obstruction:
            direction = clockwise[direction]
        elif (next_pos, direction) in seen:
            return True, set([pos[0] for pos in seen])
        else:
            pos = next_pos
            seen.add((pos, direction))


def part1():
    result = walk()
    print(len(result[1]))


def part2():
    count = 0

    for (row, col) in itertools.product(range(height), range(width)):
        if not (row == start_row and col == start_col) and walk((row, col))[0]:
            print(row, col)
            count += 1

    print(count)


part1()
part2()