with open('input', 'r') as f:
    floor = [l.strip() for l in f]

height = len(floor)
width = len(floor[0])


def adjacent_coords(y: int, x: int):
    yield y+1, x-1
    yield y+1, x
    yield y+1, x+1
    yield y, x+1
    yield y-1, x+1
    yield y-1, x
    yield y-1, x-1
    yield y, x-1


def adjacent(y: int, x: int):
    for y2, x2 in adjacent_coords(y, x):
        if 0 <= y2 < height and 0 <= x2 < width:
            yield floor[y2][x2]


accessible = 0
for y in range(len(floor)):
    for x in range(len(floor[0])):
        if floor[y][x] != '@':
            continue
        n = 0
        for c in adjacent(y, x):
            if c == '@':
                n += 1
            if n == 4:
                break
        else:
            accessible += 1


print(accessible)
