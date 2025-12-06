from functools import reduce
import operator


ops = {
    '+': operator.add,
    '*': operator.mul,
}


with open('input', 'r') as f:
    *lines, op_line = (l.strip().split() for l in f)


nums: list[list[int]] = []
for i in range(len(lines)):
    nums.append(list(map(int, lines[i])))


total = 0
for i in range(len(nums[0])):
    result = reduce(
        ops[op_line[i]],
        (nums[j][i] for j in range(len(nums)))
    )
    total += result


print(total)
