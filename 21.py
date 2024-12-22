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


def get_sequence(string: str, buttons) -> str:
    blocked = Point(-2, 0)

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


def part1():
    total = 0

    for code in codes:
        seq = code

        seq = get_sequence(seq, keypad)
        seq = get_sequence(seq, directional)
        seq = get_sequence(seq, directional)

        total += len(seq) * int(code[:3])

    print(total)

part1()

# v<<A^>>AvA^Av<<A^>>AAv<A<A^>>AA<Av>AA^Av<A^>AA<A>Av<A<A^>>AAA<Av>A^A
# <v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
