from collections import namedtuple


class Range(namedtuple('Range', ['start', 'stop'])):
    def overlaps(self, other: 'Range'):
        return (
            self.start <= other.stop <= self.stop or
            other.start <= self.stop <= other.stop
        )

    def combine(self, other: 'Range'):
        return Range(
            min(self.start, other.start),
            max(self.stop, other.stop)
        )

    def __len__(self):
        return (self.stop - self.start) + 1


def parse():
    with open('input', 'r') as f:
        for line in f:
            line = line.strip()
            if not line: break
            yield Range(*map(int, line.split('-')))


first, *rest = sorted(parse())
merged = [first]

for r in rest:
    last = merged[-1]
    if r.overlaps(last):
        merged[-1] = r.combine(last)
    else:
        merged.append(r)

print(sum(len(r) for r in merged))
