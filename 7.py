import itertools
import operator
from collections.abc import Callable

equations: list[tuple[int, list[int]]] = []

with open("inputs/7.txt") as f:
    for line in f:
        (target_str, value_str) = line.split(": ")
        values = [int(s) for s in value_str.split(" ")]
        equations.append((int(target_str), values))


def run(ops: list[Callable[[int, int], int]]):
    sum = 0

    for (target, values) in equations:
        try:
            for ops_set in itertools.product(ops, repeat=len(values) - 1):
                total = values[0]

                for (value, op) in zip(values[1:], ops_set):
                    total = op(total, value)
                    if total > target:
                        break
                else:
                    if total == target:
                        sum += target
                        raise ValueError("complete")
        except ValueError:
            pass

    print(sum)


def part1():
    run([
        operator.mul,
        operator.add
    ])


def part2():
    run([
        operator.mul,
        operator.add,
        lambda a, b: int(str(a) + str(b)) # concat
    ])


part1()
part2()
