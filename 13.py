import re
from dataclasses import dataclass


@dataclass
class ClawMachine:
    button_a: tuple[int, int]
    button_b: tuple[int, int]
    prize: tuple[int, int]


machines: list[ClawMachine] = []

with open("inputs/13.txt") as f:
    for machine_str in f.read().strip().split("\n\n"):
        button_a = re.search("A: X\\+(\\d+), Y\\+(\\d+)", machine_str)
        button_b = re.search("B: X\\+(\\d+), Y\\+(\\d+)", machine_str)
        prize = re.search("Prize: X=(\\d+), Y=(\\d+)", machine_str)

        if button_a and button_b and prize:
            machines.append(ClawMachine(
                (int(button_a.group(1)), int(button_a.group(2))),
                (int(button_b.group(1)), int(button_b.group(2))),
                (int(prize.group(1)), int(prize.group(2))),
            ))
        else:
            raise ValueError("Invalid input", machine_str, button_a, button_b, prize)


def is_whole(value: float) -> bool:
    eps = 0.0001

    return abs(value - round(value)) < eps

# treat it as an eigenspace with the button A and button B offsets as eigenvalues (a skewed grid with the offsets as the base units)
# if the offsets aren't a factor of each other (thankfully they aren't) theres only 0 or 1 solutions
# we translate the goal from this space back to unit space (regular coordinates idk the correct term)
# if whole we get a direction solution from the x and y coords
# only worry about rounding issues because floats
def work(offset = 0):
    total = 0

    for machine in machines:
        (a, b), (c, d) = machine.button_a, machine.button_b
        det = 1 / (a * d - b * c)
        inverse_matrix = ((d * det, -b * det), (-c * det, a * det))
        prize_x = machine.prize[0] + offset
        prize_y = machine.prize[1] + offset
        x = prize_x * inverse_matrix[0][0] + prize_y * inverse_matrix[1][0]
        y = prize_x * inverse_matrix[0][1] + prize_y * inverse_matrix[1][1]

        if is_whole(x) and is_whole(y):
            total += 3 * round(x) + round(y)

    print(total)


def part1():
    work()


def part2():
    work(10_000_000_000_000)


part1()
part2()