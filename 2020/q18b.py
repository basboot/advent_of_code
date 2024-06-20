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

# https://runestone.academy/ns/books/published/pythonds/BasicDS/InfixPrefixandPostfixExpressions.html
def infixToPostfix(infixexpr):
    prec = {}
    prec["*"] = 2
    prec["/"] = 2
    prec["+"] = 3
    prec["-"] = 3
    prec["("] = 1 # TODO: it works but shouldn't this have highest precendence instead of lowest?
    opStack = []
    postfixList = []
    tokenList = infixexpr

    for token in tokenList:
        if token in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or token in "0123456789":
            postfixList.append(token)
        elif token == '(':
            opStack.append(token)
        elif token == ')':
            topToken = opStack.pop(-1)
            while topToken != '(':
                postfixList.append(topToken)
                topToken = opStack.pop(-1)
        else:
            while (len(opStack) > 0) and \
               (prec[opStack[-1]] >= prec[token]):
                  postfixList.append(opStack.pop(-1))
            opStack.append(token)

    while len(opStack) > 0:
        postfixList.append(opStack.pop())
    return postfixList

def process_postfix(postfix_problem):
    stack = []
    for token in postfix_problem:
        if token.isnumeric():
            stack.append(int(token))
        else:
            a = stack.pop(-1)
            b = stack.pop(-1)
            c = process_op(a, b, token)
            stack.append(c)
    assert len(stack) == 1, "Only the answer should be left on the stack"
    return stack[0]

total = 0
for problem in problems:
    total += process_postfix(infixToPostfix(problem))

print("Part 2", total)