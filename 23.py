from collections import defaultdict


def read_input():
    comps = set()
    conns: defaultdict[str, set[str]] = defaultdict(set)

    with open("inputs/23.txt") as f:
        for line in f.read().strip().split("\n"):
            # noinspection PyTypeChecker
            (a, b) = line.split("-")
            comps.add(a)
            comps.add(b)
            conns[a].add(b)
            conns[b].add(a)

    return comps, conns

computers, connections = read_input()


def part1():
    seen = set()

    triples: set[tuple[str, str, str]] = set()

    for a in computers:
        for b in connections[a]:
            if b in seen:
                continue

            for c in connections[b]:
                if c in seen or c == a or c not in connections[a]:
                    continue

                if any([s.startswith("t") for s in [a, b, c]]):
                    # noinspection PyTypeChecker
                    triples.add(tuple(sorted([a, b, c])))

        seen.add(a)

    print(len(triples))


def part2():
    # given that there's only one
    maximum_cliques: list[set[str]] = list()

    def bron_kerbosch(r: set[str], p: set[str], x: set[str]):
        if not p and not x:
            maximum_cliques.append(set(r))
            return r

        for v in set(p):
            r2 = r.union([v])
            p2 = p.intersection(connections[v])
            x2 = x.intersection(connections[v])
            bron_kerbosch(r2, p2, x2)
            p.remove(v)
            x.add(v)

    bron_kerbosch(set(), set(computers), set())

    longest: list[str] = max(maximum_cliques, key=len)

    print(",".join(sorted(longest)))


part1()
part2()

