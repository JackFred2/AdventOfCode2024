from utils.points import Point


base_grid = dict()

with open("inputs/15.txt") as f:
    (tiles, instruction_str) = [s.strip() for s in f.read().split("\n\n")]

    for (row_index, row) in enumerate(tiles.split("\n")):
        for (col_index, char) in enumerate(row):

            if char == "@":
                start_pos = Point(col_index, row_index)
            elif char != ".":
                base_grid[Point(col_index, row_index)] = char

    instructions = []

    for instruction in instruction_str:
        match instruction:
            case "<":
                instructions.append(Point(-1, 0))
            case "v":
                instructions.append(Point(0, 1))
            case ">":
                instructions.append(Point(1, 0))
            case "^":
                instructions.append(Point(0, -1))

def print_grid(grid: dict[Point, chr], robot: Point | None = None):
    s = ""

    width = max([p.x for p in grid.keys()]) + 1
    height = max([p.y for p in grid.keys()]) + 1

    for row in range(height):
        for col in range(width):
            p = Point(col, row)
            if robot and p == robot:
                s += "@"
            elif p in grid:
                s += grid[p]
            else:
                s += " "
        s += "\n"

    print(s)

def part1():
    pos = start_pos
    grid = dict(base_grid)

    def can_move(from_pos: Point, direction: Point, affected: list[Point]) -> (bool, list[Point]) :
        offset = from_pos + direction
        if offset not in grid:
            affected.append(offset)
            return True, affected

        obstacle = grid[offset]
        if obstacle == "#":
            return False, []
        else: # == 'O'
            return can_move(offset, direction, affected)



    for instruction in instructions:
        movable, affected = can_move(pos, instruction, [])
        if movable:
            pos += instruction
            if affected[0] != pos:
                grid[affected[0]] = "O"
                del grid[pos]


    # print_grid(grid, pos)

    total = 0

    for (point, char) in grid.items():
        if char == "O":
            total += 100 * point.y + point.x

    print(total)

def part2():
    pos = start_pos * Point(2, 1)
    grid = dict()

    for (point, char) in base_grid.items():
        l = point * Point(2, 1)
        r = l + Point(1, 0)

        if char == "O":
            grid[l] = "["
            grid[r] = "]"
        else:
            grid[l] = char
            grid[r] = char

    grid[pos] = "@"

    def can_move(from_pos: Point, direction: Point, to_add: dict[Point, chr], to_remove: set[Point]) -> bool:
        me = dict()
        char = grid[from_pos]

        if grid[from_pos] in ["[", "]"] and abs(direction.y != 0):
            if char == "]":
                me[from_pos - Point(1, 0)] = "["
                me[from_pos] = "]"
            else:
                me[from_pos] = "["
                me[from_pos + Point(1, 0)] = "]"
        else:
            me[from_pos] = char

        for me_pos in me:
            offset = me_pos + direction
            if offset in grid:
                if grid[offset] == "#":
                    return False
                else:
                    if not can_move(offset, direction, to_add, to_remove):
                        return False

        for (me_pos, me_char) in me.items():
            to_add[me_pos + direction] = me_char
            to_remove.add(me_pos)

        return True

    for (i, instruction) in enumerate(instructions):
        to_add = dict()
        to_remove = set()

        if can_move(pos, instruction, to_add, to_remove):
            for pos2 in to_remove:
                if pos2 in grid:
                    del grid[pos2]

            for (pos2, char) in to_add.items():
                grid[pos2] = char
            pos += instruction

        #os.system("cls" if os.name == "nt" else "clear")
        #print(pos, instruction, f"{i}/{len(instructions)}")
        #print_grid(grid)

        #keyboard.wait("space")

    total = 0

    for (point, char) in grid.items():
        if char == "[":
            total += 100 * point.y + point.x

    print(total)


part1()
part2()