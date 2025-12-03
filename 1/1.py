dial = 50
total = 0
for rotation in open('input', 'r'):
    sign = 1 if rotation[0] == 'R' else -1
    amount = sign * int(rotation[1:])
    dial += amount
    while dial > 99:
        dial -= 100
    while dial < 0:
        dial += 100
    if dial == 0:
        total += 1

print('stopped at 0', total, 'times')
