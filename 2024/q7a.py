file1 = open('q7a.txt', 'r')
lines = file1.readlines()

def is_valid_calibration(target_value: int, current_value: int, current_equation: int, equations: [int], part: int) -> bool:
    # detect first value, and init search
    if current_equation == -1:
        return is_valid_calibration(target_value, equations[0], 1, equations, part)

    # end of list, calibration is correct if value is correct
    if current_equation == len(equations):
        return current_value == target_value

    # + and * (part2, and combining numbers) only make value higher, so break early when already too high
    if current_value > target_value:
        return False

    if is_valid_calibration(target_value, current_value + equations[current_equation], current_equation + 1, equations, part):
        return True
    if is_valid_calibration(target_value, current_value * equations[current_equation], current_equation + 1, equations, part):
        return True

    # perform operators (start with fastest growing to break earliest) to try to find a solution
    if part == 2:
        # also combine numbers for part 2
        if is_valid_calibration(target_value, int(str(current_value) + str(equations[current_equation])), current_equation + 1, equations, part):
            return True



    # all failed
    return False

calibration_result = 0

values: [int] = []
calbration_equations: [[int]] = []

for line in lines:
    value_str, equations_str = line.rstrip().split(": ")
    values.append(int(value_str))
    calbration_equations.append([int(x) for x in equations_str.split(" ")])

print("Part 1", sum([value for value, _ in filter(lambda value_equations: is_valid_calibration(value_equations[0], -1, -1, value_equations[1], 1), zip(values, calbration_equations))]))
print("Part 2", sum([value for value, _ in filter(lambda value_equations: is_valid_calibration(value_equations[0], -1, -1, value_equations[1], 2), zip(values, calbration_equations))]))


