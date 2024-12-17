import dataclasses
import itertools
import re
from dataclasses import field


@dataclasses.dataclass
class Device:
    program: list[int]

    pointer: int = 0

    reg_a: int = 0
    reg_b: int = 0
    reg_c: int = 0

    output: list[int] = field(default_factory=list)

    def reset(self):
        self.pointer = 0

    def get_combo(self, operand: int):
        match operand:
            case 4:
                return self.reg_a
            case 5:
                return self.reg_b
            case 6:
                return self.reg_c
            case 7:
                raise ValueError("Invalid combo operand")

        return operand

    def get_instruction(self) -> (bool, int, int):
        if self.pointer <= len(self.program) - 2:
            return True, self.program[self.pointer], self.program[self.pointer + 1]
        else:
            return False, 0, 0



def load_file() -> Device:
    with open("inputs/17.txt") as f:
        s = f.read()
        reg_a = int(re.search("Register A: (\\d+)", s).group(1))
        reg_b = int(re.search("Register B: (\\d+)", s).group(1))
        reg_c = int(re.search("Register C: (\\d+)", s).group(1))

        program = [int(o) for o in re.search("Program: (\\d(,\\d)*)", s).group(1).split(",")]

    return Device(program, reg_a=reg_a, reg_b=reg_b, reg_c=reg_c)


def run_device(device: Device, a: int | None = None):
    device.pointer = 0
    if a:
        device.reg_a = a
    device.reg_b = 0
    device.reg_c = 0
    device.output.clear()

    while True:
        running, opcode, operand = device.get_instruction()

        if not running:
            break

        offset = 2

        match opcode:
            case 0: #adv
                device.reg_a = device.reg_a >> device.get_combo(operand)
            case 1: #bxl
                device.reg_b = device.reg_b ^ operand
            case 2: #bst
                device.reg_b = device.get_combo(operand) % 8
            case 3: #jnz
                if device.reg_a != 0:
                    device.pointer = operand
                    offset = 0
            case 4: #bxc
                device.reg_b = device.reg_b ^ device.reg_c
            case 5: #out
                device.output.append(device.reg_b % 8)
            case 6: #bdv
                device.reg_b = device.reg_a >> device.get_combo(operand)
            case 7: #cdv
                device.reg_c = device.reg_a >> device.get_combo(operand)
            case _:
                raise ValueError("Unknown opcode")

        device.pointer += offset


def part1():
    device = load_file()

    run_device(device)

    print(",".join(map(str, device.output)))


def part2_brute_force():
    device = load_file()
    start = 1 << (3 * len(device.program))

    for i in range(start, start + 1000000000):
        if i % 100_000 == 0:
            print(i)

        device.pointer = 0
        device.reg_a = i
        device.reg_b = 0
        device.reg_c = 0
        device.output.clear()

        while True:
            running, opcode, operand = device.get_instruction()

            if not running:
                break

            offset = 2

            match opcode:
                case 0: #adv
                    device.reg_a = device.reg_a >> device.get_combo(operand)
                case 1: #bxl
                    device.reg_b = device.reg_b ^ operand
                case 2: #bst
                    device.reg_b = device.get_combo(operand) % 8
                case 3: #jnz
                    if device.reg_a != 0:
                        device.pointer = operand
                        offset = 0
                case 4: #bxc
                    device.reg_b = device.reg_b ^ device.reg_c
                case 5: #out
                    out_len = len(device.output)
                    if out_len >= len(device.program):
                        break

                    value = device.get_combo(operand) % 8

                    if device.program[out_len] == value:
                        device.output.append(value)
                    else:
                        break
                case 6: #bdv
                    device.reg_b = device.reg_a >> device.get_combo(operand)
                case 7: #cdv
                    device.reg_c = device.reg_a >> device.get_combo(operand)
                case _:
                    raise ValueError("Unknown opcode")

            device.pointer += offset

        if device.output:
            print(i, device.output)

        if device.output == device.program:
            print(i)
            return

    print("too low")

# turns a list of numbers into an int
def build(n):
    total = 0

    for i in n:
        total <<= 3
        total += i

    return total

def part2():
    device = load_file()

    def try_make(current: list[int]):
        for next in range(8):
            new = current + [next]
            val = build(new)
            run_device(device, a=val)
            #print(device.output)
            if device.program[-len(device.output):] == device.output:
                if len(device.output) == len(device.program):
                    print(val)
                    raise ValueError("done")
                elif len(new) < len(device.program):
                    try_make(new)

    try:
        try_make([])
    except ValueError:
        pass


part1()
part2()
#part2_brute_force()