ranges: list[range] = []

with open('input', 'r') as f:
    lines = iter(l.strip() for l in f)
    for line in lines:
        if not line: break
        start, stop = map(int, line.split('-'))
        ranges.append(range(start, stop+1))

    fresh = 0
    for line in lines:
        ingredient = int(line)
        if any(ingredient in r for r in ranges):
            fresh += 1

print(fresh)