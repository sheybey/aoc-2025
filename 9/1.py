from collections import namedtuple
from itertools import combinations

points = []
for line in open('input', 'r'):
    points.append(tuple(map(int, line.strip().split(','))))


class Rect(namedtuple('Rect', ['c1', 'c2'])):
    def area(self) -> int:
        x1, y1 = self.c1
        x2, y2 = self.c2
        xdiff = abs(x1-x2) + 1
        ydiff = abs(y1-y2) + 1
        return xdiff * ydiff


large_rect = max(
    (Rect(*p) for p in combinations(points, 2)),
    key=lambda r: r.area()
)
print(large_rect.area())
