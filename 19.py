def load_file() -> (list[str], list[str]):
    with open("inputs/19.txt") as f:
        lines = f.read().strip().split("\n")
        patterns = lines[0].split(", ")

        return patterns, lines[2:]

(patterns, designs) = load_file()

impossible: set[str] = set()

def try_build(target: str) -> bool:
    if target in impossible:
        return False

    for pattern in patterns:
        if target.startswith(pattern):
            if len(target) == len(pattern):
                return True
            else:
                result = try_build(target[len(pattern):])
                if result:
                    return True

    impossible.add(target)
    return False


count_cache: dict[str, int] = dict()

def get_possible_count(target: str) -> int:
    if target in count_cache:
        return count_cache[target]

    total = 0

    for pattern in patterns:
        if target.startswith(pattern):
            if len(target) == len(pattern):
                total += 1
            else:
                total += get_possible_count(target[len(pattern):])

    count_cache[target] = total
    return total


def part1():
    total = 0

    for design in designs:
        if try_build(design):
            total += 1

    print(total)


def part2():
    print(sum([get_possible_count(p) for p in designs]))


part1()
part2()

