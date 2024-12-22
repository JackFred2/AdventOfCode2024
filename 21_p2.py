import dataclasses
import itertools
import random
from functools import cache
from typing import Callable

from utils.points import Point

def read_input():
    codes = []

    with open("inputs/21.txt") as f:
        for line in f.read().strip().split("\n"):
            codes.append(line)

    return codes

codes = read_input()

keypad: dict[chr, Point] = dict([
    ('7', Point(-2, -3)),
    ('8', Point(-1, -3)),
    ('9', Point(0, -3)),
    ('4', Point(-2, -2)),
    ('5', Point(-1, -2)),
    ('6', Point(0, -2)),
    ('1', Point(-2, -1)),
    ('2', Point(-1, -1)),
    ('3', Point(0, -1)),
    ('0', Point(-1, 0)),
    ('A', Point(0, 0)),
])

directional: dict[chr, Point] = dict([
    ('^', Point(-1, 0)),
    ('A', Point(0, 0)),
    ('<', Point(-2, 1)),
    ('v', Point(-1, 1)),
    ('>', Point(0, 1)),
])


blocked = Point(-2, 0)


def get_sequence(string: str, buttons) -> str:

    seq = ""
    pos = Point(0, 0)

    for c in string:
        next = buttons[c]
        offset = next - pos

        if offset.x < 0:
            horizontal = "<" * -offset.x
        elif offset.x > 0:
            horizontal = ">" * offset.x
        else:
            horizontal = ""

        if offset.y < 0:
            vertical = "^" * -offset.y
        elif offset.y > 0:
            vertical = "v" * offset.y
        else:
            vertical = ""

        if pos + Point(offset.x, 0) == blocked or offset.x > 0:
            seq += vertical + horizontal
        else:
            seq += horizontal + vertical

        seq += "A"
        pos = next

    return seq


@dataclasses.dataclass
class Keypad:
    buttons: dict[chr, Point]
    parent: Callable[[str], int]
    cached: bool


    def get_length_for_sequence(self, sequence: str) -> int:
        length = 0

        for (fr, to) in itertools.pairwise("A" + sequence):
            if self.cached:
                length += self.get_presses_for_cached(fr, to)
            else:
                length += self.get_presses_for(fr, to)

        return length

    def __eq__(self, other):
        return id(self) == id(other)

    def __hash__(self):
        return hash(id(self))

    def get_presses_for(self, fr: chr, to: chr) -> int:
        from_pos = self.buttons[fr]
        to_pos = self.buttons[to]

        offset = to_pos - from_pos

        if from_pos == to_pos:
            result = "A"
        else:
            if offset.x < 0:
                horizontal = "<" * -offset.x
            elif offset.x > 0:
                horizontal = ">" * offset.x
            else:
                horizontal = ""

            if offset.y < 0:
                vertical = "^" * -offset.y
            elif offset.y > 0:
                vertical = "v" * offset.y
            else:
                vertical = ""

            if self.buttons == keypad:
                if from_pos.y == 0 and to_pos.x == -2:
                    result = vertical + horizontal
                elif from_pos.x == -2 and to_pos.y == 0:
                    result = horizontal + vertical
                elif offset.x > 0:
                    result = vertical + horizontal
                else:
                    result = horizontal + vertical
            else:
                if from_pos.x == -2:
                    result = horizontal + vertical
                elif to_pos.x == -2:
                    result = vertical + horizontal
                elif offset.x > 0:
                    result = vertical + horizontal
                else:
                    result = horizontal + vertical

            result += "A"

        return self.parent(result)

    @cache
    def get_presses_for_cached(self, fr: chr, to: chr) -> int:
        return self.get_presses_for(fr, to)


def part2():
    def base(s):
        return len(s)

    pad: Keypad = Keypad(directional, base, True)

    for i in range(24):
        pad = Keypad(directional, pad.get_length_for_sequence, True)

    key = Keypad(keypad, pad.get_length_for_sequence, False)

    total = 0

    for code in codes:
        numeric = int(code[:3])
        total += key.get_length_for_sequence(code) * numeric

    print(total)



part2()
