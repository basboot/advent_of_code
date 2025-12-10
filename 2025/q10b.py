import pulp as pl

machines = []

total_presses = 0

with open("q10a.txt") as f:
    for line in f:
        # [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
        _, temp_data = line.strip().split("] (")
        button_data, joltage_data = temp_data.split(") {")
        values = list(map(int, joltage_data.replace("}", "").split(",")))

        expressions = [0] * len(values)

        button_data = [tuple(map(int, b.split(","))) for b in button_data.replace("(", "").replace(")", "").split(" ")]
        button_variables = []
        for button in button_data:
            button_variable = pl.LpVariable(str(button), lowBound=0, cat="Integer")

            for b in button:
                expressions[b] += button_variable
            button_variables.append(button_variable)

        # print(values)

        model = pl.LpProblem("MILP button problem", pl.LpMinimize)

        # minimize total number of presses
        model += pl.lpSum(button_variables)

        # add constraints
        for expression, value in zip(expressions, values):
            model += expression >= value
            model += expression <= value

        # print(model)

        model.solve(pl.PULP_CBC_CMD(msg=False))

        # print("Status:", pl.LpStatus[model.status])
        solution = []
        for button_variable in button_variables:
            # print(f"{button_variable} =", button_variable.value())
            total_presses += button_variable.value()


print(f"Part 2: {total_presses}")








