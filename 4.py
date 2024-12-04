import itertools


map: list[str] = []


with open("inputs/4.txt") as f:
    for line in f:
        map.append(line)


word = "XMAS"


offsets = [p for p in itertools.product([-1, 0, 1], repeat=2) if p != (0, 0)]


def check(col: int, row: int) -> int:
    count = 0

    for offset in offsets:
        try:
            for i in range(len(word)):
                checked_col = col + offset[0] * i
                checked_row = row + offset[1] * i

                if checked_row < 0 or checked_col < 0:
                    break

                if map[checked_row][checked_col] == word[i]:
                    if i == len(word) - 1:
                        count += 1
                else:
                    break
        except IndexError:
            pass

    return count


def part1():
    count = 0

    for row in range(len(map)):
        for col in range(len(map[row])):
            count += check(col, row)

    print(count)



part1()
