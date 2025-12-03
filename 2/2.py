import re

def ranges():
    for r in open('input', 'r').read().strip().split(','):
        start, end = map(int, r.split('-'))
        yield range(start, end+1)


total = 0

for r in ranges():
    for n in r:
        dec = str(n)
        if re.match(r'^(\d+)\1+$', dec):
            total += n


print(total)
