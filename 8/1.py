import itertools
import math

Point = tuple[int, ...]
points: list[Point] = []


with open('input', 'r') as f:
    for line in f:
        points.append(tuple(map(int, line.split(','))))


pairs = sorted(itertools.combinations(points, 2), key=lambda p: math.dist(*p))


def connect(connections: list[tuple[Point, Point]], circuits: list[set[Point]] = []):
    for (p1, p2) in connections:
        # find all circuits that contain either junction box
        contains = []
        others = []
        for circuit in circuits:
            if p1 in circuit or p2 in circuit:
                contains.append(circuit)
            else:
                others.append(circuit)

        # combine all circuits that contain either box into a new circuit
        circuits = others
        new_circuit = set(itertools.chain.from_iterable(contains))
        new_circuit.add(p1)
        new_circuit.add(p2)
        circuits.append(new_circuit)

        # part 2 check
        if len(circuits) == 1 and len(circuits[0]) == len(points):
            return circuits, (p1, p2)

    # exhausted all input connections, but there are boxes left unconnected
    return circuits, None


circuits, _ = connect(pairs[:1000])

lengths = sorted(map(len, circuits), reverse=True)
print('part 1:', lengths[0] * lengths[1] * lengths[2])

circuits, last = connect(pairs[1000:], circuits)
if last is None:
    print('failed to connect all circuits')
else:
    print('part 2:', last, last[0][0] * last[1][0])
