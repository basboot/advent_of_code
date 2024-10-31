# To continue, please consult the code grid in the manual.  Enter the code at row 2947, column 3029.

row = 2947
column = 3029

first_value = 20151125
multiplier = 252533
modulus = 33554393


right_above = column + row - 1

# full left upper triangle
n = ((right_above + 1) // 2) * right_above

# go back to position
n -= (row - 1)

# print(n)

iterations = n - 1

code = (first_value * pow(multiplier, iterations, modulus)) % modulus

print(code)