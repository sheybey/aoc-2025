banks: list[list[int]] = []

with open('input', 'r') as f:
    for line in f:
        banks.append(list(map(int, iter(line.strip()))))


def find_best(bank: list[int], n: int = 2):
    '''
    find the best possible joltage for a bank, picking n batteries.
    '''
    batteries: list[int] = []  # picked batteries
    end = n - 1                # batteries left to pick
    i = 0                      # start of available batteries
    while end > -1:
        # create the slice of available batteries. they must be to the right
        # of those already used (i), and there must be enough batteries left
        # to pick from for the rest of the loop (end)
        part = slice(i, None if end == 0 else -end)

        # find the index of the maximum battery in this slice
        i, bat = max(enumerate(bank[part]), key=lambda t: t[1])

        # save it and move to the next slice
        batteries.append(bat)
        i += 1 + part.start
        end -= 1

    # joltage is calculated by treating the batteries picked as the decimal
    # representation of a number
    return sum(n * (10 ** i) for i, n in enumerate(reversed(batteries)))


joltage = 0
for bank in banks:
    # part 1: n = 2, part 2: n = 12
    joltage += find_best(bank, 12)

print(joltage)
