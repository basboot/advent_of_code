file1 = open('q18a.txt', 'r')
lines = file1.readlines()

import re

# ChatGPT
# Define the pattern to match numbers, parentheses, and operators
pattern = r'(\d+|\(|\)|\+|\*)'
# Use re.findall to find all matches

problems = [re.findall(pattern, expression.rstrip().replace(" ", "")) for expression in lines] #

def process_op(val1, val2, op):
    if op == "+":
        return val1 + val2
    else:
        if op == "*":
            return val1 * val2
        else:
            return val1

def process(problem, value):
    last_op = None
    while True:
        if len(problem) == 0:
            return value

        curr = problem.pop(0) # head / tail (destruct problem on purpose)

        match curr:
            case "+":
                last_op = "+"
            case "*":
                last_op = "*"
            case "(":
                new_value = process(problem, 0)
                value = process_op(new_value, value, last_op)
            case ")":
                return value
            case _:
                value = process_op(int(curr), value, last_op)


total = 0
for problem in problems:
    total += process(problem, 0)

print(total)

# ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2

# 159244466993 too low

