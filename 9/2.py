from collections import namedtuple, deque
from itertools import combinations, product, islice

Point = namedtuple('Point', ['x', 'y'])

max_x = 0
max_y = 0
points = []
for line in open('input', 'r'):
    point = Point(*map(int, line.strip().split(',')))
    points.append(point)
    max_x = max(max_x, point.x)
    max_y = max(max_y, point.y)


def sliding_window(iterable, n, wrap=False):
    '''Collect data into overlapping fixed-length chunks or blocks.'''
    # sliding_window('ABCDEFG', 4) → ABCD BCDE CDEF DEFG
    iterator = iter(iterable)
    first = list(islice(iterator, n - 1))
    window = deque(first, maxlen=n)
    for x in iterator:
        window.append(x)
        yield tuple(window)
    if wrap:
        for x in first:
            window.append(x)
            yield tuple(window)


class Line(namedtuple('Line', ['p1', 'p2'])):
    def vertical(self):
        return self.p1.x == self.p2.x

    def intersects(self, other: 'Line'):
        if self.vertical():
            if other.vertical():
                return False
            x1 = other.p1.x
            x2 = other.p2.x
            if x1 > x2:
                x2, x1 = x1, x2
            y1 = self.p1.y
            y2 = self.p2.y
            if y1 > y2:
                y2, y1 = y1, y2
            return (
                x1 < self.p1.x < x2 and
                y1 < other.p1.y < y2
            )
        else:
            if not other.vertical():
                return False
            y1 = other.p1.y
            y2 = other.p2.y
            if y1 > y1:
                y2, y1 = y1, y2
            x1 = self.p1.x
            x2 = self.p2.x
            if x1 > x2:
                x2, x1 = x1, x2
            return (
                x1 < other.p1.x < x2 and
                y1 < self.p1.y < y2
            )

class Rect(namedtuple('Rect', ['c1', 'c2'])):
    '''Rectangle, defined by opposite corners. c1.y must be <= c2.y'''
    def area(self) -> int:
        x1, y1 = self.c1
        x2, y2 = self.c2
        xdiff = abs(x1-x2) + 1
        ydiff = abs(y1-y2) + 1
        return xdiff * ydiff

    def contains(self, p: Point):
        '''True if point is inside this rect'''
        y_range = range(self.c1.y, self.c2.y+1)
        if not p.y in y_range:
            return False
        if self.c1.x <= self.c2.x:
            x_range = range(self.c1.x, self.c2.x+1)
        else:
            x_range = range(self.c2.x, self.c1.x+1)
        return p.x in x_range

    def corners(self):
        '''Yield all corners of this rect'''
        yield self.c1
        yield self.c2
        yield Point(self.c1.x, self.c2.y)
        yield Point(self.c2.x, self.c1.y)

    def sides(self):
        for p in sliding_window(self.corners(), 2, True):
            yield Line(*p)


def valid_rects():
    edges = [Line(*p) for p in sliding_window(points, 2, True)]
    for combo in combinations(points, 2):
        rect = Rect(*combo)
        intersects = any(
            l1.intersects(l2)
            for l1, l2 in product(rect.sides(), edges)
        )
        if not intersects:
            yield rect

def solve():
    largest_rect = max(valid_rects(), key=lambda r: r.area())
    print(largest_rect.area())
