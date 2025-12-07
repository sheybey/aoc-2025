from collections import defaultdict

with open('input', 'r') as f:
    start, *lines = f.read().splitlines()

total_splits = 0
paths: defaultdict[int, int] = defaultdict(lambda: 0, {start.index('S'): 1})
beams = set(paths.keys())

for line in lines:
    new_beams = set()
    new_paths = defaultdict(lambda: 0)
    for beam in beams:
        if line[beam] == '^':
            total_splits += 1
            left = beam-1
            right = beam+1
            if left >= 0:
                new_beams.add(left)
                new_paths[left] += paths[beam]
            if right < len(start):
                new_beams.add(right)
                new_paths[right] += paths[beam]
        else:
            new_beams.add(beam)
            new_paths[beam] += paths[beam]

    beams = new_beams
    paths = new_paths


print('part 1:', total_splits)
print('part 2:', sum(paths.values()))
