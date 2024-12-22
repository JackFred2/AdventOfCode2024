# * 2^6
# ^ secret
# mod 2^24
# / 2^5
# ^ secret
# mod 2^24
# * 2^11
# ^ secret
# mod 2^11
import itertools
from collections import Counter


def load_input():
    secrets = []

    with open("inputs/22.txt") as f:
        for line in f.read().strip().split("\n"):
            secrets.append(int(line))

    return secrets


secrets = load_input()


prune = 2 ** 24 - 1


def next_secret(secret: int) -> int:
    secret = ((secret << 6) ^ secret) & prune
    secret = ((secret >> 5) ^ secret) & prune
    secret = ((secret << 11) ^ secret) & prune
    return secret


def part1():
    total = 0

    for secret in secrets:
        #print(secret, end="=")
        for i in range(2000):
            secret = next_secret(secret)
        #print(secret)

        total += secret

    print(total)


def part2():
    potential = Counter()

    for secret in secrets:
        prices = [secret % 10]
        price_diffs = []

        seen_sequences = set()

        for i in range(2000):
            secret = next_secret(secret)
            new_price = secret % 10
            price_diffs.append(new_price - prices[-1])
            prices.append(new_price)

            if i > 3:
                seq = (price_diffs[-4], price_diffs[-3], price_diffs[-2], price_diffs[-1])

                if seq not in seen_sequences:
                    seen_sequences.add(seq)
                    potential[seq] += prices[-1]

    print(max(potential.values()))

part1()
part2()


