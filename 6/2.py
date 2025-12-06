from functools import reduce
import operator


ops = {
    '+': operator.add,
    # '-': operator.sub,
    '*': operator.mul,
    # '/': operator.floordiv
}


with open('input', 'r') as f:
    *number_lines, op_line = f.read().split('\n')

numbers: list[list[int]] = []
problem_ops: list[str] = []

# this code will break if you strip the whitespace from the input. So, don't do
# that :)

# this list won't be touched, but it makes static analyzers happy
current_numbers: list[int] = []

for i in range(len(op_line)):
    # if there is an operator, this is the start of a new problem
    if op_line[i] != ' ':
        problem_ops.append(op_line[i])
        current_numbers = []
        numbers.append(current_numbers)

    # collect a number from the current column if there is one
    digits = [
        l[i]
        for l in number_lines
        if l[i].isdigit()
    ]

    # ignore empty columns - these are separators, but we just use the existence
    # of an operator to denote the start of a new problem
    if digits:
        n = int(''.join(digits))
        current_numbers.append(n)

total = 0
# strict is just to make sure I didn't screw up
for nums, op in zip(numbers, problem_ops, strict=True):
    total += reduce(ops[op], nums)

print(total)
