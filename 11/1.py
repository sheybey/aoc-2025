outputs: dict[str, list[str]] = {}
with open('input', 'r') as f:
    for line in f:
        key, values = line.split(': ')
        outputs[key] = values.strip().split()


def paths_to(start, end):
    outs = 0
    paths = {dev: 1 for dev in outputs[start]}

    while len(paths) > 0:
        new_paths = {}
        for device in paths:
            for output in outputs.get(device, []):
                if output == end:
                    outs += paths[device]
                else:
                    new_paths[output] = new_paths.get(output, 0) + paths[device]
        paths = new_paths

    return outs


print('part 1:', paths_to('you', 'out'))

# svr -> fft -> dac -> out
svr_fft = paths_to('svr', 'fft')
fft_dac = paths_to('fft', 'dac')
dac_out = paths_to('dac', 'out');

# svr -> dac -> fft -> out
svr_dac = paths_to('svr', 'dac')
dac_fft = paths_to('dac', 'fft')
fft_out = paths_to('fft', 'out')

print(
    'part 2:',
    svr_fft * fft_dac * dac_out +
    svr_dac * dac_fft * fft_out
)
