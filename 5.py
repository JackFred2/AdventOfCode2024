rules: list[tuple[int, int]] = []
updates: list[list[int]] = []


with open("inputs/5.txt") as f:
    (rule_string, updates_string) = f.read().split("\n\n")

    for line in rule_string.split("\n"):
        (f, t) = line.split("|")
        rules.append((int(f), int(t)))

    for line in updates_string.split("\n"):
        if line:
            updates.append(list(map(int, line.split(","))))


def swap(l, fr, to):
    temp = l[fr]
    l[fr] = l[to]
    l[to] = temp


def run():
    valid_count = 0
    invalid_updates = []

    for update in updates:
        try:
            applicable_rules = [(f, t) for (f, t) in rules if f in update and t in update]

            for (index, page) in enumerate(update):
                for (fr, to) in applicable_rules:
                    if fr == page and index > update.index(to):
                        raise ValueError("invalid")

            valid_count += update[len(update)//2]
        except ValueError as e:
            if e.args[0] != "invalid":
                raise e
            else:
                invalid_updates.append(update)

    print(valid_count)

    invalid_count = 0

    for update in invalid_updates:
        applicable_rules = [(f, t) for (f, t) in rules if f in update and t in update]

        while True:
            changed_this_run = False

            for (index, page) in enumerate(update):
                for (fr, to) in applicable_rules:
                    if fr == page and index > update.index(to):
                        swap(update, index, update.index(to))
                        changed_this_run = True


            if not changed_this_run:
                invalid_count += update[len(update)//2]
                break

    print(invalid_count)


run()