with open('input', 'r') as f:
    floor = [list(l.strip()) for l in f]

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


def spiral():
    top = 0
    bottom = height-1
    left = 0
    right = width-1

    while top <= bottom and left <= right:
        for i in range(left, right + 1):
            yield (top, i)
        top += 1

        if left <= right:
            for i in range(top, bottom + 1):
                yield (i, right)
        right -= 1

        if top <= bottom:
            for i in range(right, left - 1, -1):
                yield (bottom, i)
        bottom -= 1

        if left <= right:
            for i in range(bottom, top - 1, -1):
                yield (i, left)
        left += 1


removed = 0
while True:
    accessible = 0
    for y, x in spiral():
        if floor[y][x] != '@':
            continue
        n = 0
        for c in adjacent(y, x):
            if c == '@':
                n += 1
            if n == 4:
                break
        else:
            floor[y][x] = '.'
            accessible += 1
            removed += 1
    if accessible == 0:
        break


print(removed)
