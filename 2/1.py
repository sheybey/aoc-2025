def ranges():
    for r in open('input', 'r').read().strip().split(','):
        start, end = map(int, r.split('-'))
        yield range(start, end+1)

total = 0

for r in ranges():
    for n in r:
        dec = str(n)
        if len(dec) % 2 == 1:
            continue
        mid = len(dec)//2
        if dec[mid:] == dec[:mid]:
            total += n


print(total)
