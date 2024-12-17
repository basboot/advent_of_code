program = [2,4,1,5,7,5,4,3,1,6,0,3,5,5,3,0]
program.reverse()
print(program)

def create_output(a):
    b = a % 8
    b = b ^ 5
    c = a >> b
    b = b ^ c
    b = b ^ 6
    return b % 8

def find_solution(solution, position, reversed_program):
    if position == len(reversed_program):
        return solution

    solution = solution << 3
    for i in range(8):
        print(solution + i, create_output(solution + i), " ==? ", reversed_program[position])
        if create_output(solution + i) == reversed_program[position]:
            print(":", solution)
            s = find_solution(solution + i, position + 1, reversed_program)
            if s is not None:
                print("yes")
                return s
            else:
                print("no")
    return None

print(">>", find_solution(0, 0, program))