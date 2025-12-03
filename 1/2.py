dial = 50
total = 0

for rotation in open('input', 'r'):
    sign = 1 if rotation[0] == 'R' else -1
    amount = int(rotation[1:])

    # count full cycles
    while amount > 100:
        total += 1
        amount -= 100

    # remaining amount is now less than a full cycle
    amount *= sign
    dial += amount

    if dial == 0:  # stopped at zero
        total += 1

    elif dial > 99:  # passed zero going up
        total += 1
        dial -= 100

    elif dial < 0:  # passed zero going down
        if dial != amount:  
            total += 1
        dial += 100

print('stopped at 0', total, 'times')
