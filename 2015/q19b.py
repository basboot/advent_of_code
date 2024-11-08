from mip import *

file1 = open('q19b.txt', 'r')
lines = file1.readlines()

replacements = defaultdict(list)

reversed_replacements = defaultdict(str)

medicine = None

for i in range(len(lines)):
    line = lines[i].rstrip()

    if line == "":
        medicine = lines[i + 1].rstrip()
        break

    in_molecule, out_molecule = line.split(" => ")
    replacements[in_molecule].append(out_molecule)
    reversed_replacements[out_molecule] = in_molecule

print(medicine)

print("Total elements", len(medicine))
print("Number of ( )", medicine.count('(') + medicine.count(')'))
print("Number of ,", medicine.count(','))

print("Solution", len(medicine) - (medicine.count('(') + medicine.count(')')) - 2*medicine.count(',') - 1)

# From solutions
# First insight
#
# There are only two types of productions:
#
# e => XX and X => XX (X is not Rn, Y, or Ar)
# X => X Rn X Ar | X Rn X Y X Ar | X Rn X Y X Y X Ar
# Second insight
#
# You can think of Rn Y Ar as the characters ( , ):
#
# X => X(X) | X(X,X) | X(X,X,X)
# Whenever there are two adjacent "elements" in your "molecule", you apply the first production. This reduces your molecule length by 1 each time.
#
# And whenever you have T(T) T(T,T) or T(T,T,T) (T is a literal token such as "Mg", i.e. not a nonterminal like "TiTiCaCa"), you apply the second production. This reduces your molecule length by 3, 5, or 7.
#
# Third insight
#
# Repeatedly applying X => XX until you arrive at a single token takes count(tokens) - 1 steps:
#
# ABCDE => XCDE => XDE => XE => X
# count("ABCDE") = 5
# 5 - 1 = 4 steps
# Applying X => X(X) is similar to X => XX, except you get the () for free. This can be expressed as count(tokens) - count("(" or ")") - 1.
#
# A(B(C(D(E)))) => A(B(C(X))) => A(B(X)) => A(X) => X
# count("A(B(C(D(E))))") = 13
# count("(((())))") = 8
# 13 - 8 - 1 = 4 steps
# You can generalize to X => X(X,X) by noting that each , reduces the length by two (,X). The new formula is count(tokens) - count("(" or ")") - 2*count(",") - 1.
#
# A(B(C,D),E(F,G)) => A(B(C,D),X) => A(X,X) => X
# count("A(B(C,D),E(F,G))") = 16
# count("(()())") = 6
# count(",,,") = 3
# 16 - 6 - 2*3 - 1 = 3 steps
# This final formula works for all of the production types (for X => XX, the (,) counts are zero by definition.)
#
# The solution
#
# My input file had:
#
# 295 elements in total
#  68 were Rn and Ar (the `(` and `)`)
#   7 were Y (the `,`)
# Plugging in the numbers:
#
# 295 - 68 - 2*7 - 1 = 212
# Like I said, no leaderboard position today, but this was a heck of a lot more interesting than writing yet another brute force script.