from collections import Counter

with open("inputs/11_test.txt") as f:
    initial_stones = [int(s) for s in f.read().split(" ")]


def part1():
    stones = initial_stones[::]

    for i in range(10):
        new_stones = []

        for stone in stones:
            if stone == 0:
                new_stones.append(1)
            else:
                as_str = str(stone)
                if len(as_str) % 2 == 0:
                    new_stones.append(int(as_str[:len(as_str)//2]))
                    new_stones.append(int(as_str[len(as_str)//2:]))
                else:
                    new_stones.append(stone * 2024)

        stones = new_stones

    print(len(stones))


def part2():
    stones = Counter(initial_stones)

    for i in range(75):
        update = Counter()

        for (stone, count) in stones.items():
            if stone == 0:
                update[1] += count
            else:
                as_str = str(stone)
                if len(as_str) % 2 == 0:
                    update[int(as_str[:len(as_str)//2])] += count
                    update[int(as_str[len(as_str)//2:])] += count
                else:
                    update[stone * 2024] += count

        stones = update

    print(stones.total())



part1()
part2()