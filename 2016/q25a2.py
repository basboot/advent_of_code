
print(bin(4 * 643))
# 101000001100

a = int('101010101010', 2) - 4 * 643


print(a)



# cpy a d -- d = a
# d = a -> moved
# cpy 4 c -- c = 4
# c = 4
# cpy 643 b -- b = 643
# b = 643
# inc d -- d++
# dec b -- b--
# jnz b -2 -- naar 4 zolang b > 0
# dec c -- c--
# jnz c -5 -- naar 3 zolang c > 0, d = b * c + a, b = 0, c = 0
d = a + 4 * 643 # input regelt d indirect


while True:
    # cpy d a -- a = d
    a = d # input + 4 * 643
    while a != 0:
        # jnz 0 0 -- nop
        # cpy a b -- b = a
        # cpy 0 a -- a = 0
        # cpy 2 c -- c = 2
        c = 2


        # jnz b 2 -- naar 16 als b > 0
        # jnz 1 6 -- naar 21
        # dec b -- b--
        # dec c -- c--
        c = c - (a % 2)
        # jnz c -4 -- naar 14 zolang c > 0
        # inc a -- a++
        a = a // 2
        # jnz 1 -7 -- naar 13
        # cpy 2 b -- b = 2
        b = 2 - c
        # jnz c 2 -- naar 24 als b > 0
        # jnz 1 4 -- naar 27
        # dec b -- b--
        # dec c -- c--
        # jnz 1 -4 -- naar 22
        # jnz 0 0 -- nop

        # out b -- output b
        print(b)

    # jnz a -19 -- naar 10 als a > 0

# jnz 1 -21 -- naar 9