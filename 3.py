import re

with open("inputs/3.txt") as f:
    memory = f.read()


def part1():
    print(sum([int(match[0]) * int(match[1]) for match in re.findall("mul\((\d+),(\d+)\)", memory)]))


def part2():
    sum = 0
    active = True

    string = memory

    while True:
        match = re.search("do\(\)|don't\(\)|mul\((\d+),(\d+)\)", string)

        if match:
            if match.group(0) == "do()":
                active = True
            elif match.group(0) == "don't()":
                active = False
            else:
                if active:
                    sum += int(match.group(1)) * int(match.group(2))

            string = string[match.end():]
        else:
            break

    print(sum)


part1()
part2()